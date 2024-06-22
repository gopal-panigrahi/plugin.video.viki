# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from resources.lib.utils import get_images, deep_get
from resources.lib.constants import MAIN_MENU, GENRES
from codequick import Listitem, Resolver, Route
import inputstreamhelper
from urllib.parse import urlencode
import base64
import json


class Builder:
    def build_menu(self):
        for item_name, country, image in MAIN_MENU:
            item_data = {
                "callback": Route.ref("/resources/lib/main:list_collection"),
                "label": item_name,
                "params": {"country": country, "page": 1},
            }
            item = Listitem.from_dict(**item_data)
            item.art.local_thumb(image)
            yield item

    def build_collection(self, items):
        for each in items:
            match (each.get("type")):
                case "series":
                    yield from self.build_series(each)
                case "film":
                    yield from self.build_movie(each)

    def build_series(self, item):
        thumb, fanart = get_images(item)
        item_data = {
            "callback": Route.ref("/resources/lib/main:list_episodes"),
            "label": deep_get(item, "titles.en"),
            "art": {"thumb": thumb, "fanart": fanart},
            "info": {
                "mpaa": item.get("rating"),
                "genre": [GENRES[k] for k in item.get("genres")],
                "plot": deep_get(item, "descriptions.en"),
                "plotoutline": deep_get(item, "blurbs_general.en"),
                "country": deep_get(item, "origin.country"),
                "aired": item.get("created_at"),
            },
            "params": {"id": item.get("id"), "page": 1},
        }
        yield Listitem.from_dict(**item_data)

    def build_movie(self, item):
        thumb, fanart = get_images(item)
        item_data = {
            "callback": Resolver.ref("/resources/lib/main:play_video"),
            "label": deep_get(item, "titles.en"),
            "art": {"thumb": thumb, "fanart": fanart},
            "info": {
                "mpaa": item.get("rating"),
                "genre": [GENRES[k] for k in item.get("genres")],
                "plot": deep_get(item, "descriptions.en"),
                "plotoutline": deep_get(item, "blurbs_general.en"),
                "country": deep_get(item, "origin.country"),
                "aired": item.get("created_at"),
            },
            "params": {
                "id": deep_get(item, "watch_now.id"),
                "title": deep_get(item, "titles.en"),
            },
        }
        yield Listitem.from_dict(**item_data)

    def build_episodes(self, items):
        for each in items:
            thumb, _ = get_images(each)
            item_data = {
                "callback": Resolver.ref("/resources/lib/main:play_video"),
                "label": f"Episode {each.get('number')}",
                "art": {"thumb": thumb},
                "info": {
                    "mpaa": each.get("rating"),
                    "genre": [GENRES[k] for k in deep_get(each, "container.genres")],
                    "plot": deep_get(each, "descriptions.en"),
                    "plotoutline": deep_get(each, "descriptions.en"),
                    "episode": each.get("number"),
                    "duration": each.get("duration"),
                    "country": deep_get(each, "container.origin.country"),
                    "aired": each.get("stream_created_at"),
                },
                "params": {
                    "id": each.get("id"),
                    "title": f"Episode {each.get('number')}",
                },
            }
            yield Listitem.from_dict(**item_data)

    def build_play(self, video, title, stream_headers):
        url = next(i for i in video["queue"] if i["type"] == "video").get("url")
        lic_server = json.loads(base64.b64decode(video.get("drm"))).get("dt3")

        license_key = lic_server + "|%s&Content-Type=application/octet-stream|R{SSM}|"

        is_helper = inputstreamhelper.Helper("mpd", drm="com.widevine.alpha")

        if is_helper.check_inputstream():
            item_data = {
                "callback": url,
                "label": title,
                "properties": {
                    "IsPlayable": True,
                    "inputstream": is_helper.inputstream_addon,
                    "inputstream.adaptive.manifest_type": "mpd",
                    "inputstream.adaptive.license_type": "com.widevine.alpha",
                    "inputstream.adaptive.stream_headers": urlencode(stream_headers),
                    "inputstream.adaptive.license_key": license_key,
                },
            }
            return Listitem(content_type="video").from_dict(**item_data)
