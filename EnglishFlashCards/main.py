from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from sqlalchemy import select, func
from flask_bootstrap import Bootstrap5
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from models import init_app, db, User, FlashCard
from forms import RegisterForm, LoginForm
from flask_migrate import Migrate
import csv
from utils import get_random_flashcard

# CONFIGURING AND INITIALIZING THE APP
app = Flask(__name__)
foo = secrets.token_urlsafe(16)
app.secret_key = foo

bootstrap = Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
init_app(app)
migrate = Migrate(app, db)

# LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ROUTES CONFIGURATION
@app.route("/")
def main_page():
    return render_template("main-page.html")


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = db.session.execute(db.select(User).filter_by(username=form.username.data)).one_or_none()
        if existing_user:
            message = "This username is not available"
            return render_template("register-page.html", message=message, form=form)
        else:
            user = User(
                name=form.name.data,
                username=form.username.data,
                password=generate_password_hash(form.password.data)
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("main_page"))
    return render_template("register-page.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user_parsed = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar_one_or_none()
        if not user_parsed:
            message = "This user does not exist"
            return render_template("login-page.html", form=form, message=message)
        elif user_parsed:
            password_correct = check_password_hash(user_parsed.password, form.password.data)
            if not password_correct:
                message = "Wrong password"
                return render_template("login-page.html", form=form, message_password=message)
            else:
                logout_user()
                login_user(user_parsed)
                return redirect(url_for("home_page"))
    return render_template("login-page.html", form=form)


@app.route("/flashcard", methods=["GET", "POST"])
@login_required
def flashcard_page():
    is_correct = False

    # SUBMITTING USER'S TRANSLATION
    if request.method == "POST":
        user_translation = request.form.get("user_translation")
        flashcard_id = int(request.form.get("flashcard_id"))

        stmt = select(FlashCard).where(FlashCard.id == flashcard_id)
        flashcard = db.session.execute(stmt).scalar_one_or_none()

        # USER'S TRANSLATION IS CORRECT
        if user_translation.lower() == flashcard.english_word.lower():
            is_correct = 'correct'
            flashcard.correct_count += 1
            # TODO: Upgrade the leitner_score by 1 when consecutive reaches 5
            flashcard.consecutive += 1

            if flashcard.consecutive == 5:
                flashcard.leitner_score += 1
                flashcard.consecutive = 0
            db.session.commit()

            return render_template("flashcard-page.html", flashcard=flashcard,
                                   is_correct=is_correct)

        # USER'S TRANSLATION IS INCORRECT
        # TODO: Mark the word as hard when consecutive reaches -5
        elif user_translation.lower() != flashcard.english_word.lower():
            is_correct = 'incorrect'
            flashcard.wrong_count += 1
            if flashcard.consecutive > 0:
                flashcard.consecutive = 0
            else:
                flashcard.consecutive -= 1
                if flashcard.consecutive == -5:
                    flashcard.is_hard = True
            db.session.commit()

            return render_template("flashcard-page.html", flashcard=flashcard,
                                   is_correct=is_correct)

    random_flashcard = get_random_flashcard()
    return render_template("flashcard-page.html", flashcard=random_flashcard, is_correct=is_correct)


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_page():
    if request.method == "POST":
        file = request.files.get("csv_file")
        if not file or not file.filename:
            flash("Choose a file!", "no-file")

        elif file and not file.filename.endswith(".csv"):
            flash("Wrong format!", "wrong-format")

        else:
            content = file.read().decode("utf-8").splitlines()
            reader = csv.reader(content)
            next(reader, None)

            for row in reader:
                stmt = select(FlashCard).where(
                    (FlashCard.user_id == current_user.id) & (FlashCard.polish_word == row[0]))
                word_to_check = db.session.execute(stmt).scalar_one_or_none()
                if word_to_check and word_to_check.english_word == row[1]:
                    continue
                else:
                    if len(row) == 5:
                        flashcard = FlashCard(
                            polish_word=row[0],
                            english_word=row[1],
                            description_pl=row[2],
                            description_en=row[3],
                            category=row[4],
                            user_id=current_user.id
                        )
                        db.session.add(flashcard)
                    else:
                        continue
            db.session.commit()
            flash("Flashcards uploaded successfully!", "success")
    return render_template("upload-page.html")


@app.route("/home")
@login_required
def home_page():
    return render_template("home-page.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main_page"))


if __name__ == "__main__":
    app.run(debug=True)
