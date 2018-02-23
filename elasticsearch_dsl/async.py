import sys

ASYNC_SUPPORTED = sys.version_info >= (3, 5)

if ASYNC_SUPPORTED:
    # since PY35 ElasticSearch-DSL support asynchronous clients
    import inspect
    from functools import partial
    from asyncio import Future, ensure_future

    isawaitable = inspect.isawaitable

    def future_response(response, response_handler):
        f_response = ensure_future(response)
        f = Future()
        f_response.add_done_callback(
            partial(_result_or_exception, f_response, f, response_handler)
        )
        return f

    def _result_or_exception(f_response, f, response_handler, task):
        try:
            f.set_result(response_handler(f_response.result()))
        except Exception as e:
            f.set_exception(e)
else:
    Future = None
    future_response = None
    def isawaitable(*args, **kwargs):
        return False
