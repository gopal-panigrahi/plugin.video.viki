from __future__ import unicode_literals
from resources.lib.utils import update_query_params
import urlquick
from resources.lib.constants import URLS, BASE_HEADERS, url_constructor
from codequick import Script
import requests


class VikiApi:
    def __init__(self):
        self.session = urlquick.Session()
        self.session.headers.update(BASE_HEADERS)

    def get_collection(self, country, page):
        url = url_constructor(URLS.get("CONTAINER"))
        params = {
            "page": page,
            "per_page": 24,
            "with_paging": False,
            "direction": "desc",
            "sort": "views_recent",
            "origin_country": country,
            "licensed": True,
            "app": "100000a",
        }
        url = update_query_params(url, params)
        resp = self.get(url)
        return resp

    def get_episodes(self, id, page):
        url = url_constructor(URLS.get("EPISODES")).format(id=id)
        params = {
            "page": page,
            "per_page": 10,
            "with_upcoming": False,
            "sort": "number",
            "direction": "asc",
            "blocked": False,
            "app": "100000a",
        }
        url = update_query_params(url, params)
        resp = self.get(url)
        return resp

    def get_movie(self, id):
        url = url_constructor(URLS.get("MOVIE")).format(id=id)
        url = update_query_params(url, {"app": "100000a"})
        resp = self.get(url)
        return resp.get("response")[0]

    def get_video(self, id):
        url = URLS.get("VIDEO").format(id=id)
        resp = self.get(url)
        return resp

    def raw_post(self, url, headers, payload):
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 401:
                Script.notify("Error", "")
            return response.json()
        except Exception as e:
            return self._handle_error(e, url, "post")

    def get(self, url, **kwargs):
        try:
            response = self.session.get(url, **kwargs)
            return response.json()
        except Exception as e:
            return self._handle_error(e, url, "get", **kwargs)

    def post(self, url, **kwargs):
        try:
            response = self.session.post(url, **kwargs)
            return response.json()
        except Exception as e:
            return self._handle_error(e, url, "post", **kwargs)

    def _handle_error(self, e, url, _rtype, **kwargs):
        Script.notify("Internal Error", "")

    def _get_play_headers(self):
        stream_headers = self.session.headers
        return stream_headers
