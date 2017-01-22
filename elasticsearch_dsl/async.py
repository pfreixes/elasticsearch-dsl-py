import sys

if sys.version_info >= (3, 5):
    # since PY35 ElasticSearch-DSL support asynchronous clients
    import inspect
    from asyncio import Future, ensure_future
    isawaitable = inspect.isawaitable
else:
    Future = None
    ensure_future = None
    def isawaitable(*args, **kwargs):
        return False
