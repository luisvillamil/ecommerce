"""main code for db_client"""

# base libraries
import logging

# external libraries
from sqlmodel import create_engine, Session, select, SQLModel

# internal libraries
from ecommerce.config import settings
from ecommerce.db.user import *
from ecommerce.db.category import *
from ecommerce.db.product import *
from ecommerce.db.item import *
from ecommerce.db.image import *

# constants
logger = logging.getLogger("uvicorn")

class DbClient:
    """Main interface to database"""
    def __init__(self, echo:bool=False):
        self.engine = create_engine(
            str(settings.SQLALCHEMY_DATABASE_URI),
            echo=echo)

    def _create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        """Creates session with engine.
        calling code must be responsible for session lifetime.

        Returns:
            Session: new session
        """
        with Session(self.engine) as session:
            yield session

    async def run(self):
        """Initializes database"""
        self._create_db_and_tables()
        # check if admin exists, otherwise create new one
        with Session(self.engine) as session:
            user_list = await get_user_list_internal(session, admin=True)
            if not user_list:
                # create new admin user
                logger.info("creating initial superuser")
                await create_superuser(session)

    async def cleanup(self):
        """Ensure transactions finish"""

db_client = DbClient(
    echo = True if settings.DEBUG else False)
