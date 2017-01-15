# -*- coding: utf-8 -*-
import pytest
import asyncio
import asynctest

from mock import Mock

from elasticsearch_dsl import search

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
