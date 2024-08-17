import asyncio

from intellisearch.search_aggr.aggregator import SearchAggregator

if __name__ == "__main__":
    aggregator = SearchAggregator()
    search_results = asyncio.run(aggregator.search("Generative AI", 10, 7))
    for result in search_results:
        print(result)
        print("--------")
