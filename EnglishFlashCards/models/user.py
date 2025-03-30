from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
