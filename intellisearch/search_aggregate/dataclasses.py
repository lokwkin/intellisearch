from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class NewsSearchResultItem:
    title: str
    url: str
    published_at: datetime
    description: str
    source: str
    search_engine: str
    search_query: str


@dataclass
class NewsSearchResultOrigin:
    search_engine: str
    search_query: str


@dataclass
class NewsSearchResultAggregatedItem:
    title: str
    url: str
    published_at: datetime
    description: str
    source: str
    result_origins: List[NewsSearchResultOrigin]
