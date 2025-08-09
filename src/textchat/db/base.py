"""db/base.py"""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.schema import MetaData

engine = create_async_engine(
    "sqlite+aiosqlite:///textchat.db",
    echo=False,
)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)
metadata = MetaData()


class Base(DeclarativeBase):
    pass


class Channels(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_name = Column(String, unique=True)

    def __init__(self, channel_name):
        self.channel_name = channel_name


class ServerInfo(Base):
    __tablename__ = "server"
    id = Column(Integer, primary_key=True, autoincrement=True)
    server_address = Column(String, unique=True)
    port = Column(Integer, unique=False)
    nickname = Column(String, unique=False)
    password = Column(String, unique=False)
    sasl_login = Column(Boolean, unique=False)

    def __init__(self, server_address, port, nickname, password, sasl_login):
        self.server_address = server_address
        self.port = port
        self.nickname = nickname
        self.password = password
        self.sasl_login = sasl_login


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
