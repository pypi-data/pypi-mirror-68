import re
from typing import List

import requests

from .endpoints import GAME_UPDATES_ENDPOINT, INDIVIDUAL_GAME_UPDATE_ENDPOINT
from .scraper import parse


def get_game_updates(locale='en-us'):
    patch_list_request = requests.get(GAME_UPDATES_ENDPOINT.format(locale=locale))
    return GameUpdatesPage(patch_list_request.json()['result']['pageContext'])


def get_game_update(url, locale='en-us', parser=None):
    patch_request = requests.get(INDIVIDUAL_GAME_UPDATE_ENDPOINT.format(url=url, locale=locale))
    return Patch(patch_request.json()['result']['pageContext'], parser)


class Section:
    def __init__(self, data, parser):
        self._scraper = parser
        self.title = data.get('title')
        self.content = data['content']

    def parse_content(self):
        if self._scraper is None:
            raise RuntimeError('Scraper not installed')
        try:
            return self._scraper(self.content)
        except Exception:
            raise RuntimeError('Error while scraping the page data')


class Category:
    def __init__(self, data):
        self.name = data['name']
        self.slug = data['slug']
        self.url = data['url']


class PatchSummary:
    def __init__(self, data, *, main_instance):
        self._data = data
        self._main_instance = main_instance
        self._cache = None

        self.id = data['id']
        self.url = data['link']['url']
        self.category = data['category']
        self.title = data['title']
        self.authors = data['authors']
        self.date = data['date']
        self.image_url = data['imageUrl']
        self.term_ids = data['termIds']

    def clear_cache(self):
        self._cache = None

    def get_full_data(self):
        if self._cache is None:
            self._cache = get_game_update(self.url, self._main_instance.url_locale, self._main_instance.scraper)
        return self._cache


class Patch:
    def __init__(self, data, parser):
        self.locale = data['locale']
        self.uid = data['data']['uid']
        self.title = data['data']['title']
        self.description = data['data']['description']
        self.category = Category(data['data']['category'])
        self.authors = data['data']['authors']
        self.image_url = data['data']['imageUrl']
        self.related_articles = data['data']['relatedArticles']
        self.patch = Section(data['data']['sections'][0]['props'], parser)


class GameUpdatesManager:
    def __init__(self, summaries: List[PatchSummary]):
        self._updates = summaries

    @staticmethod
    def from_response(data, main_instance):
        updates = []
        for article in data:
            updates.append(PatchSummary(article, main_instance=main_instance))
        return updates

    def by_title_names(self, names: List[str]):
        return GameUpdatesManager([update for update in self._updates for name in names
                                   if name in update.title])

    def by_title_name_re(self, pattern: str):
        return GameUpdatesManager([update for update in self._updates if re.match(pattern, update.title)])

    def __getitem__(self, item):
        return self._updates[item]

    def most_recent(self):
        if len(self._updates) > 0:
            return None
        return self._updates[0]


class GameUpdatesPage:
    def __init__(self, data):
        self._data = data
        self.scraper = None

        self.locale = data['locale']
        self.uid = data['data']['uid']
        self.title = data['data']['title']
        self.description = data['data']['description']
        self.image_url = data['data']['image']['url']
        self.updates = GameUpdatesManager(
            GameUpdatesManager.from_response(data['data']['sections'][0]['props']['articles'], main_instance=self)
        )
        self.install_scrapper(parse)

    @property
    def url_locale(self):
        return self.locale.replace('_', '-').lower()

    def install_scrapper(self, interface):
        self.scraper = interface
