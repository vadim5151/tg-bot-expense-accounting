from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import  DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession



engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine, expire_on_commit=False, class_= AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    google_sheeps = relationship('GoogleSheets')
    data = relationship('Data')
    categories = relationship('Category')


class Data(Base):
    __tablename__ = 'data'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(8))
    category: Mapped[str] = mapped_column(String(25))
    amount: Mapped[int] = mapped_column()
    user_tg_id = mapped_column(BigInteger, ForeignKey('users.tg_id'))
    users = relationship('User')


class GoogleSheets(Base):
    __tablename__ = 'google_sheets'

    id: Mapped[int] = mapped_column(primary_key=True)
    name_table: Mapped[str] = mapped_column(String(25))
    id_google_sheets: Mapped[str] = mapped_column(String(50))
    user_tg_id = mapped_column(BigInteger, ForeignKey('users.tg_id'))
    users = relationship('User')


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(50))
    user_tg_id = mapped_column(BigInteger, ForeignKey('users.tg_id'))
    users = relationship('User')


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


