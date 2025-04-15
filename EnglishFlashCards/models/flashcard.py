from sqlalchemy.orm import Mapped, mapped_column
from . import db


class FlashCard(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    polish_word: Mapped[str] = mapped_column(nullable=False)
    english_word: Mapped[str] = mapped_column(nullable=False)
    description_pl: Mapped[str] = mapped_column(nullable=True)
    description_en: Mapped[str] = mapped_column(nullable=True)
    category: Mapped[str] = mapped_column(nullable=False)
    leitner_score: Mapped[int] = mapped_column(default=0, nullable=False)
    is_hard: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_known: Mapped[bool] = mapped_column(default=False, nullable=False)
    correct_count: Mapped[int] = mapped_column(default=0, nullable=False)
    wrong_count: Mapped[int] = mapped_column(default=0, nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=True)
    consecutive: Mapped[int] = mapped_column(default=0, nullable=False)
