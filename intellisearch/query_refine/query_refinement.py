from dataclasses import dataclass
import os
import pystache
import json
from openai import AsyncOpenAI, DefaultAsyncHttpxClient


@dataclass
class RefineQueryResponse:
    classification: str
    refine_emphasis: str
    refined_queries: list[str]


class QueryRefiner:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                                         http_client=DefaultAsyncHttpxClient(proxy=os.getenv("OPENAI_PROXY_URL")))
        with open('intellisearch/query_refine/template.txt', 'r') as file:
            self.template = file.read()

    async def refine_query(self, original_query: str) -> RefineQueryResponse:
        rendered_prompt = pystache.render(self.template, {'original_query': original_query})

        response = await self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": rendered_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
        )

        result = json.loads(response.choices[0].message.content)
        return RefineQueryResponse(**result)
