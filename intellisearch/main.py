import asyncio

from intellisearch.search_aggregate.aggregator import SearchAggregator

if __name__ == "__main__":
    aggregator = SearchAggregator(num_results_per_engine=10)
    search_results = asyncio.run(aggregator.search("Generative AI", 7))
    for result in search_results:
        print(result)
        print("--------")
