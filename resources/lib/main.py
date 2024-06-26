# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from resources.lib.api import VikiApi
from resources.lib.builder import Builder
import urlquick
from codequick import Route, run, Script, Resolver, Listitem


@Route.register
def root(_):
    yield Listitem.search(
        Route.ref("/resources/lib/main:list_collection"), url="search"
    )
    yield from builder.build_menu()


@Route.register
def list_collection(_, **kwargs):
    if kwargs.get("search_query", False):
        keyword = kwargs.get("search_query")
        page = api.get_search_response(keyword, kwargs.get("page", 1))
        yield from builder.build_collection(page.get("response"))

        if page.get("more"):
            kwargs["page"] = kwargs.get("page", 1) + 1
            yield Listitem.next_page(**kwargs)
    else:
        if "country" in kwargs:
            page = api.get_collection(kwargs.get("country"), kwargs.get("page", 1))
            yield from builder.build_collection(page.get("response"))
            if page.get("more"):
                kwargs["page"] = kwargs.get("page", 1) + 1
                yield Listitem.next_page(**kwargs)
        else:
            return False


@Route.register
def list_episodes(_, **kwargs):
    if "id" in kwargs:
        page = api.get_episodes(kwargs.get("id"), kwargs.get("page", 1))
        yield from builder.build_episodes(page.get("response"))

        if page.get("more"):
            kwargs["page"] = kwargs.get("page", 1) + 1
            yield Listitem.next_page(**kwargs)
    else:
        return False


@Resolver.register
def play_video(_, **kwargs):
    if "id" in kwargs:
        video = api.get_video(kwargs.get("id"))
        stream_headers = api._get_play_headers()
        return builder.build_play(video, kwargs.get("title"), stream_headers)


@Script.register
def cleanup(_):
    urlquick.cache_cleanup(-1)
    Script.notify("Cache Cleaned", "")


api = VikiApi()
builder = Builder()
