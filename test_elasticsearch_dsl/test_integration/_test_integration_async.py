import pytest

from datetime import datetime
from elasticsearch_async import AsyncElasticsearch

from elasticsearch_dsl.search import Search, MultiSearch
from elasticsearch_dsl.index import Index

from .utils import Repository, Commit
from .utils import COMMIT_DOCS_WITH_MISSING, COMMIT_DOCS_WITH_ERRORS


@pytest.mark.asyncio
async def test_count(data_client):
    async_client = AsyncElasticsearch(hosts=['localhost'])
    s = Search(using=async_client).index('git')
    response = await s.count()
    assert 53 == response

@pytest.mark.asyncio
async def test_search(data_client):
    async_client = AsyncElasticsearch(hosts=['localhost'])
    s = Search(using=async_client).index('git')
    response = await s.execute()
    assert response.success()

@pytest.mark.asyncio
async def test_suggest(data_client):
    async_client = AsyncElasticsearch(hosts=['localhost'])
    s = Search(using=async_client).index('git')
    response = await s.execute_suggest()
    assert response.success()

@pytest.mark.asyncio
async def test_msearch(data_client):
    async_client = AsyncElasticsearch(hosts=['localhost'])
    s = Search(using=async_client).index('git')
    ms = MultiSearch(using=async_client).index('git')
    ms = ms.add(s).add(s)
    r1, r2 = await ms.execute()
    assert all([r1.success(), r2.success()])

@pytest.mark.asyncio
async def test_index_exists(write_client):
    async_client = AsyncElasticsearch(hosts=['localhost'])
    assert await Index('git', using=async_client).exists()
    assert not await Index('not-there', using=async_client).exists()

@pytest.mark.asyncio
async def test_get(write_client):
    async_client = AsyncElasticsearch(hosts=['localhost'])
    elasticsearch_repo = await Repository.get('elasticsearch-dsl-py', using=async_client)
    assert isinstance(elasticsearch_repo, Repository)
    assert elasticsearch_repo.owner.name == 'elasticsearch'
    assert datetime(2014, 3, 3) == elasticsearch_repo.created_at

@pytest.mark.asyncio
async def test_mget(write_client):
    async_client = AsyncElasticsearch(hosts=['localhost'])
    commits = await Commit.mget(COMMIT_DOCS_WITH_MISSING, using=async_client)
    assert commits[0] is None
    assert commits[1]._id == '3ca6e1e73a071a705b4babd2f581c91a2a3e5037'
    assert commits[2] is None
    assert commits[3]._id == 'eb3e543323f189fd7b698e66295427204fff5755'

@pytest.mark.asyncio
async def test_update(write_client):
    async_client = AsyncElasticsearch(hosts=['localhost'])
    elasticsearch_repo = await Repository.get('elasticsearch-dsl-py', using=async_client)
    v = elasticsearch_repo.meta.version

    await elasticsearch_repo.update(
        owner={'new_name': 'elastic_async'},
        new_field='testing-update',
        using=async_client)

    assert 'elastic_async' == elasticsearch_repo.owner.new_name
    assert 'testing-update' == elasticsearch_repo.new_field

    # assert version has been updated
    assert elasticsearch_repo.meta.version == v + 1

    new_version = await Repository.get('elasticsearch-dsl-py', using=async_client)
    assert 'testing-update' == new_version.new_field
    assert 'elastic_async' == new_version.owner.new_name
    assert 'elasticsearch' == new_version.owner.name

@pytest.mark.asyncio
async def test_save(write_client):
    async_client = AsyncElasticsearch(hosts=['localhost'])
    elasticsearch_repo = await Repository.get('elasticsearch-dsl-py', using=async_client)

    elasticsearch_repo.new_field = 'testing-save'
    v = elasticsearch_repo.meta.version
    assert not (await elasticsearch_repo.save(using=async_client))

    # assert version has been updated
    assert elasticsearch_repo.meta.version == v + 1
