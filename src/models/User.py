from database.db import db, Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from typing import List


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    firstname: Mapped[str] = mapped_column(String(50), nullable=True)
    lastname: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password: Mapped[str] = mapped_column(String(80))
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    favorites = relationship("Favorite", backref="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "favorites": [fav.serialize() for fav in self.favorites]
        }