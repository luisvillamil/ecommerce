import pytest
from pytest_mock import MockerFixture
from unittest.mock import AsyncMock, MagicMock
from ecommerce.common.db_client import AsyncDatabaseClient, Base
from ecommerce.common.data_model import User
from sqlalchemy import select, text

@pytest.fixture
def mock_db_client(mocker:MockerFixture):
    mock_engine = mocker.patch('sqlalchemy.ext.asyncio.create_async_engine', return_value=AsyncMock())
    client = AsyncDatabaseClient('postgresql+asyncpg://user:password@localhost/testdb')
    client.engine = mock_engine

    # mocking session
    call = mocker.Mock()
    begin = AsyncMock()
    transaction = mocker.Mock()
    transaction.rollback = AsyncMock()
    transaction.commit = AsyncMock()
    begin.return_value = transaction
    call.begin = AsyncMock()
    call.close = AsyncMock()
    client.SessionLocal.__call__ = call
    return client

@pytest.mark.asyncio
async def test_context_manager(mocker:MockerFixture, mock_db_client:mock_db_client):
    # with pytest.raises(Exception):
    async with mock_db_client as client:
        assert mock_db_client.session != None
        assert mock_db_client.transaction != None
        
    # test error being thrown
    with pytest.raises(Exception):
        async with mock_db_client as client:
            assert mock_db_client.transaction != None
            raise Exception("testing error")
    assert mock_db_client.session == None

@pytest.mark.asyncio
async def test_create_all_tables(mocker:MockerFixture, mock_db_client):
    run_sync_mock = AsyncMock()
    conn = mocker.Mock()
    conn.run_sync = run_sync_mock
    mock_db_client.engine.begin().__aenter__.return_value = conn
    await mock_db_client.create_all_tables()

    # Check if run_sync was called with the right argument
    run_sync_mock.assert_called_once_with(Base.metadata.create_all)

@pytest.mark.asyncio
async def test_get_db_session(mocker, mock_db_client:AsyncDatabaseClient):
    async for session in mock_db_client.get_db_session():
        assert session is not None
    assert mock_db_client.session == None


@pytest.mark.asyncio
async def test_add_list(mocker, mock_db_client):
    # Mock a Base instance
    mock_base = mocker.MagicMock(spec=Base)

    # Mock the session's add_all method
    mock_add_all = mocker.patch('sqlalchemy.orm.session.Session.add_all', new_callable=AsyncMock)

    # Test the add_list method
    async with mock_db_client as client:
        await client.add_list(mock_base)

    # Check if add_all was called with the correct argument
    mock_add_all.assert_called_once_with((mock_base, ))

@pytest.mark.asyncio
async def test_query(mocker, mock_db_client):

    # Mock a Column instance for order_by
    mock_column = User.username
    # Mock the where clause
    mock_where = User.username == "testuser"

    # Mock the session's execute method and its return value
    # mock_execute = mocker.patch('sqlalchemy.orm.session.Session.execute', new_callable=AsyncMock)
    result_proxy = MagicMock()
    result_proxy.scalars().all.return_value = ()
    # mock_execute.return_value = result_proxy

    # Test the query method
    async with mock_db_client as client:
        client.session.execute = AsyncMock()
        client.session.execute.return_value = result_proxy
        res = await client.query(User, mock_where, order_by=mock_column)

        assert res == ()
