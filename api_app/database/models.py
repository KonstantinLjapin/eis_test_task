from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Column, String


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    """модель пользователя"""
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

