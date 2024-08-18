import asyncio
from typing import Dict, List
from intellisearch.search_aggregate.dataclasses import NewsSearchResultAggregatedItem, NewsSearchResultItem, NewsSearchResultOrigin
from intellisearch.search_aggregate.news.google_news import GoogleNews
from intellisearch.search_aggregate.news.bing_news import BingNews


class SearchAggregator:
    def __init__(self, num_results_per_engine: int = 10, proxy: str = None):
        self.google_news = GoogleNews(proxy=proxy)
        self.bing_news = BingNews(proxy=proxy)
        self.num_results_per_engine = num_results_per_engine

    async def search(self, query: str | List[str], interval_date: int) -> List[NewsSearchResultAggregatedItem]:
        """
        Search for news articles using the Google News and Bing News APIs. You may provide a single query or a list of
        queries. The results are deduplicated by URL.

        Args:
            query (str | List[str]): The search query or queries to search for. Can be a single query or a list of
                                     queries.
            interval_date (int): The number of days to search for news articles.

        Returns:
            List[NewsSearchResult]: A list of news search results.
        """

        if isinstance(query, str):
            query = [query]

        tasks = []
        for q in query:
            google_task = self.google_news.fetch_news(
                topic=q, num_results=self.num_results_per_engine, time_range=f'{interval_date}d')
            bing_task = self.bing_news.fetch_news(
                topic=q, num_results=self.num_results_per_engine, interval_date=interval_date)
            tasks.extend([google_task, bing_task])

        task_results: List[List[NewsSearchResultItem]] = await asyncio.gather(*tasks)
        results = [result for task_result in task_results for result in task_result]

        # Deduplicate by URL
        deduplication: Dict[str, NewsSearchResultAggregatedItem] = {}
        for result in results:
            if result.url not in deduplication:
                deduplication[result.url] = NewsSearchResultAggregatedItem(
                    url=result.url,
                    title=result.title,
                    description=result.description,
                    published_at=result.published_at,
                    source=result.source,
                    result_origins=[NewsSearchResultOrigin(
                        search_engine=result.search_engine, search_query=result.search_query)]
                )
            else:
                deduplication[result.url].result_origins.append(NewsSearchResultOrigin(
                    search_engine=result.search_engine, search_query=result.search_query))

        deduplicated_results = list(deduplication.values())

        # Sort by the number of search engines referenced
        deduplicated_results.sort(key=lambda x: len(x.result_origins), reverse=True)
        return deduplicated_results
