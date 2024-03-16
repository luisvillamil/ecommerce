import asyncio
import time
from fastapi import Depends

CONCURRENT_REQUESTS = 10000
# Asynchronous timer decorator
def async_timer(func):
    async def wrapper(*args, **kwargs):
        start_time = time.time()  # Start time
        result = await func(*args, **kwargs)  # Await the function
        end_time = time.time()  # End time
        print(f"Function {func.__name__} took {end_time - start_time} seconds to complete.")
        return result
    return wrapper

# Example of an asynchronous function
@async_timer
async def example_function(n):
    await asyncio.sleep(n)  # Simulating a task
    return f"Completed after {n} seconds"
@async_timer
async def test_connection_old():
    from ecommerce.common.db_client import AsyncDatabaseClient
    from ecommerce.common.data_model import Test

    async def test_saves(db:AsyncDatabaseClient, i:int):
        async with db as client:
            client.session.add(Test(test=str(i)))

    async def test_get(db:AsyncDatabaseClient, i:int):
        async with db as client:
            client = await db.query(Test, (Test.id==i))

    db = AsyncDatabaseClient("postgresql+asyncpg://postgres:password@127.0.0.1/test_connection")
    await db.create_all_tables()

    await asyncio.gather(
        *(test_saves(db, i) for i in range(CONCURRENT_REQUESTS)))
    await asyncio.gather(
        *(test_get(db, i) for i in range(CONCURRENT_REQUESTS)))

@async_timer
async def test_connection_new():
    from sqlmodel import Session, SQLModel, Field
    from ecommerce.db import db_client

    class Test(SQLModel, table=True):

        id:int = Field(default=None, primary_key=True, index=True)
        test: str

    await db_client.run()

    async def test_saves(i:int):
        with Session(db_client.engine) as session:
            test = Test(test=str(i))
            session.add(test)
            session.commit()

    async def test_get(i:int):
        with Session(db_client.engine) as session:
            return session.get(Test, {"id": i})

    await asyncio.gather(
        *(test_saves(i) for i in range(CONCURRENT_REQUESTS)))
    await asyncio.gather(
        *(test_get(i) for i in range(CONCURRENT_REQUESTS)))


# Running the example
async def main():
    await test_connection_old()
    await test_connection_new()

asyncio.run(main())