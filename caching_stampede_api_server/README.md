### Running Unit Tests
```aiignore
$python -m pytest -vv test_app.py --durations 0
========================================================================= test session starts =========================================================================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Users/#####/Projects/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/#####/Projects/prototypes/caching_stampede/src
plugins: asyncio-1.2.0, anyio-4.12.0, tornasync-0.6.0.post2, twisted-1.14.3, trio-0.8.0
asyncio: mode=strict, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 1 item                                                                                                                                                      

test_app.py::test_cache_stampede_protection PASSED                                                                                                              [100%]

========================================================================== slowest durations ==========================================================================
2.01s call     test_app.py::test_cache_stampede_protection
0.00s teardown test_app.py::test_cache_stampede_protection
0.00s setup    test_app.py::test_cache_stampede_protection
========================================================================== 1 passed in 2.01s ==========================================================================
``` 