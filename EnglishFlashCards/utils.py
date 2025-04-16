from random import choices
from flask_login import current_user
from sqlalchemy import select
from models import db, FlashCard


def get_random_flashcard():
    stmt = select(FlashCard).where(FlashCard.user_id == current_user.id)
    flashcards_all = db.session.execute(stmt).all()

    flashcards = [flashcard[0] for flashcard in flashcards_all]
    flashcards_weights = [5.5 - flashcard[0].leitner_score for flashcard in flashcards_all]

    random_flashcard = choices(population=flashcards, weights=flashcards_weights, k=1)[0]
    return random_flashcard
