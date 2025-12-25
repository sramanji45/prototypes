import logging
import asyncio
import pytest
from unittest.mock import AsyncMock
from cache import get_cached_data

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

@pytest.mark.asyncio
async def test_cache_stampede_protection():
    logging.info('test_cache_stampede_protection: Started')
    # Mock cache and database
    async def db_call():
        await asyncio.sleep(2)
        return "data"
    mock_db = AsyncMock(side_effect=db_call)

    # 1. Simulate 100 concurrent requests for the same key
    tasks = [get_cached_data("test_key", mock_db) for _ in range(100)]

    # 2. Run them all at once
    results = await asyncio.gather(*tasks)

    # 3. Assertions
    # All 10 requests should get the same data
    assert all(r == "data" for r in results)

    # CRITICAL: The expensive DB function should only have been called ONCE
    assert mock_db.call_count == 1
    logging.info('test_cache_stampede_protection: Completed')
