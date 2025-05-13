import datetime
import os
from sqlalchemy.orm import mapped_column, Mapped, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from dotenv import load_dotenv

load_dotenv()


class Base(DeclarativeBase):
    pass


DB_URL = os.getenv("DB_URL", 'postgresql+asyncpg://postgres:postgres@db:5432/postgres')

engine_async = create_async_engine(DB_URL)

session = async_sessionmaker(engine_async)


class Tournament(Base):
    __tablename__ = 'tournaments'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    max_players: Mapped[int] = mapped_column(nullable=True)
    start_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    players: Mapped[list['Participant']] = relationship(uselist=True, back_populates='tournament', cascade='all, delete-orphan',)

    def __init__(self, name, max_players, start_at):
        self.name = name
        self.max_players = max_players
        self.start_at = start_at

    def __repr__(self):
        return f'Tournament: {self.id=}, {self.name=}, {self.max_players=}, {self.start_at=}'


class Participant(Base):
    __tablename__ = 'players'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, )
    tournament_id: Mapped[int] = mapped_column(ForeignKey('tournaments.id', ondelete='CASCADE'))
    tournament: Mapped['Tournament'] = relationship(uselist=False, back_populates='players')

    def __init__(self, name, email, tournament_id):
        self.tournament_id = tournament_id
        self.name = name
        self.email = email
