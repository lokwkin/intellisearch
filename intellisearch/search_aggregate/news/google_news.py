import unicodedata
from bs4 import BeautifulSoup
from googlenewsdecoder import decoderv2
from typing import List
import aiohttp
import feedparser
from urllib.parse import urlencode
import re
import logging
from intellisearch.search_aggregate.dataclasses import NewsSearchResultItem

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s [%(name)s] %(message)s'))
logger.addHandler(handler)


class GoogleNews:
    def __init__(self, proxy=None, base_url='https://news.google.com/rss'):
        self.proxy = proxy
        self.base_url = base_url

    async def _fetch_xml_content(self, url) -> str:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url, proxy=self.proxy) as response:
                response.raise_for_status()
                return await response.text()

    def _parse_xml_news(self, xml_content, num_results) -> List[NewsSearchResultItem]:
        feed = feedparser.parse(xml_content)
        news_list = []

        def parse_description(html_text):
            soup = BeautifulSoup(html_text, 'html.parser')
            return unicodedata.normalize("NFKD", soup.text)

        for item in feed.entries[:num_results]:
            title = item.get('title')
            link = item.get('link')
            pub_date = item.get('pubDate')
            description = parse_description(item.get('description'))
            source = item.get('source')
            news_list.append({
                'title': title,
                'url': link,
                'published_at': pub_date,
                'description': description,
                'source': source,
            })

        return news_list

    def _parse_time_range(self, time_range) -> str:
        if not time_range:
            return None

        match = re.match(r'^(\d+)([hdy])$', time_range)
        if not match:
            raise ValueError("Invalid time range format. Use format like '1h', '2d', '1y'.")

        # value, unit = match.groups()
        # unit_map = {'h': 'hour', 'd': 'day', 'w': 'week', 'm': 'month', 'y': 'year'}
        # return f"{value}{unit_map[unit][0]}"

        return time_range

    async def fetch_news(self, topic='', country='US', language='en', num_results=10, time_range=None) -> List[NewsSearchResultItem]:
        params = {
            'hl': language,
            'gl': country,
            'ceid': f'{country}:{language}'
        }

        if time_range:
            topic += f' when:{self._parse_time_range(time_range)}'

        params['q'] = topic

        url = f"{self.base_url}/search?{urlencode(params)}"
        logger.info(f"Fetching news from {url}")

        try:
            xml_content = await self._fetch_xml_content(url)
            results = self._parse_xml_news(xml_content, num_results)
            result_dtos = []
            for result in results:
                try:
                    result_dtos.append(NewsSearchResultItem(
                        **result,
                        url=decoderv2(result['url']),
                        search_engine='google_news',
                        search_query=topic
                    ))
                except Exception:
                    logger.error(f"Failed to decode URL: {result['url']}")
            return result_dtos
        except aiohttp.ClientError as e:
            print(f"Error fetching news: {e}")
            raise e
