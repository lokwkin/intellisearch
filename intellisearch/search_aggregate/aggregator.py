import asyncio
from intellisearch.search_aggregate.news.google_news import GoogleNews
from intellisearch.search_aggregate.news.bing_news import BingNews


class SearchAggregator:
    def __init__(self, num_results_per_engine: int = 10):
        self.google_news = GoogleNews()
        self.bing_news = BingNews()
        self.num_results_per_engine = num_results_per_engine

    async def search(self, topic: str, interval_date: int):
        google_task = asyncio.create_task(self.google_news.fetch_news(
            topic=topic, num_results=self.num_results_per_engine, time_range=f'{interval_date}d'))
        bing_task = asyncio.create_task(self.bing_news.fetch_news(
            topic=topic, num_results=self.num_results_per_engine, interval_date=interval_date))

        google_results, bing_results = await asyncio.gather(google_task, bing_task)

        # Combine results from both sources
        all_results = google_results + bing_results

        # Deduplicate by URL, updating the search_engine list
        unique_results = {}
        for result in all_results:
            if result.url not in unique_results:
                unique_results[result.url] = result
            else:
                unique_results[result.url].search_engine.extend(
                    engine for engine in result.search_engine
                    if engine not in unique_results[result.url].search_engine
                )

        unique_results = list(unique_results.values())
        return unique_results
