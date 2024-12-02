from sqlalchemy import BigInteger, String, Text, TIMESTAMP, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import sqlite3
from datetime import datetime
from data import config


engine = create_async_engine(url=config.DATABASE_URL)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    link = mapped_column(Text, nullable=True)
    category = mapped_column(String, nullable=True)
    priority = mapped_column(Integer, nullable=True, default=1)
    joined_at = mapped_column(TIMESTAMP, default=datetime.utcnow)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)