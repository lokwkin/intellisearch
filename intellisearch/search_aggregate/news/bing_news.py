from typing import List
import aiohttp
import feedparser
from urllib.parse import urlencode, urlparse, parse_qs
import logging

from intellisearch.search_aggregate.dataclasses import NewsSearchResultItem

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s [%(name)s] %(message)s'))
logger.addHandler(handler)


class BingNews:
    def __init__(self, proxy=None, base_url='https://www.bing.com/news'):
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
        for item in feed.entries[:num_results]:

            title = item.get('title')
            masked_link = item.get('link')
            link = parse_qs(urlparse(masked_link).query).get('url')[0]
            pub_date = item.get('pubDate')
            description = item.get('description')
            source = item.get('News:Source')
            news_list.append({
                'title': title,
                'url': link,
                'published_at': pub_date,
                'description': description,
                'source': source,
            })

        return news_list

    async def fetch_news(self, topic='', country='US', language='en', num_results=10, interval_date: int = None) -> List[NewsSearchResultItem]:
        params = {
            'format': 'rss',
            'setlang': language,
            'cc': country,
        }

        if interval_date:
            params['qft'] = f'interval="{interval_date}"'

        params['q'] = topic

        url = f"{self.base_url}/search?{urlencode(params)}"
        logger.info(f"Fetching news from {url}")

        try:
            xml_content = await self._fetch_xml_content(url)
            results = self._parse_xml_news(xml_content, num_results)
            result_dtos = [NewsSearchResultItem(
                **result,
                search_engine='bing_news',
                search_query=topic
            ) for result in results]
            return result_dtos
        except aiohttp.ClientError as e:
            print(f"Error fetching news: {e}")
            raise e
