import asyncio
import time
from typing import Dict, Any

# For Local optima, We can use semaphores within a API server
# In real world, the cache would be a proper store like Redis
cache: Dict[str, Any] = {}
cache_locks: Dict[str, asyncio.Semaphore] = {}


async def get_cached_data(key: str, data_fetch_func, ttl: int = 60):
    # 1. Check cache
    if key in cache:
        return cache[key]['data']

    # 2. Acquire a semaphore specific to the key
    if key not in cache_locks:
        cache_locks[key] = asyncio.Semaphore(1)  # Only 1 concurrent access to origin

    async with cache_locks[key]:
        # Double check cache after acquiring lock (another task might have populated it)
        if key in cache:
            return cache[key]['data']

        # 3. Cache miss: Regenerate data (simulate I/O)
        print(f"Cache miss for {key}, regenerating...")
        data = await data_fetch_func()

        # 4. Store the new data in cache
        cache[key] = {'data': data, 'expires': time.time() + ttl}
        print(f"Cache populated for {key}")

        # Lock is automatically released by the 'async with' context manager
        return data


# Example Usage in an API endpoint handler
async def simulate_expensive_db_call():
    # Simulate a database query time
    await asyncio.sleep(2)
    return {"value": "some expensive data", "timestamp": time.time()}


