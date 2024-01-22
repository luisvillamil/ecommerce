from typing import Iterable
from typing import List, Type, Union, Coroutine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import Column, ClauseElement
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import select

Base = declarative_base()

class AsyncDatabaseClient:
    def __init__(self, database_url):
        self.engine = create_async_engine(database_url, future=True, echo=True)
        self.SessionLocal = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession)
        self.session = None # defined in context manager

    async def __aenter__(self):
        # Open a new session and begin a transaction when entering the context
        self.session = self.SessionLocal()
        self.transaction = await self.session.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # If exception occurs, roll back the transaction. Otherwise, commit it
        if exc_type is not None:
            await self.transaction.rollback()
        else:
            await self.transaction.commit()
        # Close the session when exiting the context
        await self.session.close()
        self.session = None

    async def get_db_session(self):
        """ Get new db session """
        async with self.SessionLocal() as session:
            yield session

    async def add_list(self, *args:Iterable[Base]):
        """ Adds objects to database """
        await self.session.add_all(args)

    async def query(
            self, model_class:Type[DeclarativeMeta],
            *where: Iterable[ClauseElement],
            order_by:Union[Column, str, None]=None
        ) -> Coroutine[None, None, List[DeclarativeMeta]]:
        """ Query objects based on model class and criteria. 
        where can be any column clause
        and order by can be any column of the model
        """
        stmt = select(model_class)
        if where:
            stmt = stmt.where(*where)
        if order_by:
            stmt = stmt.order_by(order_by)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_all_tables(self):
        """ Create all tables in the database. """
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
