import argparse
import asyncio
import dotenv
from intellisearch.query_refine.query_refinement import QueryRefiner
from intellisearch.search_aggregate.aggregator import SearchAggregator


dotenv.load_dotenv()


async def main(query: str, date_interval: int):
    query_refiner = QueryRefiner()
    aggregator = SearchAggregator(num_results_per_engine=10)

    refine = await query_refiner.refine_query(query)

    refined_queries = refine.refined_queries

    search_results = await aggregator.search(refined_queries, date_interval)

    for result in search_results:
        print(result.title, result.url, result.result_origins)
        print("--------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for news articles")
    parser.add_argument("query", type=str, help="The search query")
    parser.add_argument("--date_interval", type=int, default=7,
                        help="The number of days to search for news articles (default: 7)")
    args = parser.parse_args()

    asyncio.run(main(args.query, args.date_interval))
