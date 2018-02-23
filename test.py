import asyncio

from elasticsearch_async import AsyncElasticsearch
from elasticsearch_dsl.search import Search



async def test_count():
    async_client = AsyncElasticsearch(hosts=['localhost'])
    s = Search(using=async_client).index('git')
    response = await s.count()
    assert 53 == response


loop = asyncio.get_event_loop()
loop.run_until_complete(test_count())
