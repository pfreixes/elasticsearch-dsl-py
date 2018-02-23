# -*- coding: utf-8 -*-
import pytest
import asyncio
import asynctest

from mock import Mock

from elasticsearch_dsl import search, utils

@pytest.mark.asyncio
async def test_search_execute(dummy_response):
    client = asynctest.CoroutineMock()
    client.search.return_value = dummy_response
    s = search.Search(using=client)
    res = await s.execute()
    assert res.success()


@pytest.mark.asyncio
async def test_search_execute_uses_cache():
    o = object()
    client = Mock()
    s = search.Search(using=client)
    s._response = o
    s._response_async = True
    res = await s.execute()
    assert res == o
    client.search.assert_not_called()


@pytest.mark.asyncio
async def test_multi_search_execute(dummy_response_msearch):
    client = asynctest.CoroutineMock()
    client.msearch.return_value = dummy_response_msearch
    s = search.MultiSearch(using=client)
    results = await s.execute()
    assert all(map(lambda res: res.success(), results))


@pytest.mark.asyncio
async def test_multi_search_execute_uses_cache():
    o = object()
    client = Mock()
    ms = search.MultiSearch(using=client)
    ms._response = o
    ms._response_async = True
    res = await ms.execute()
    assert res == o
    client.search.assert_not_called()


@pytest.mark.asyncio
async def test_count_uses_cache():
    s = search.Search()
    s._response_async = True
    s._response = utils.AttrDict({'hits': {'total': 42}})

    assert 42 == await s.count() 
