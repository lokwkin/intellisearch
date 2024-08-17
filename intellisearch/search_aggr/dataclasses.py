from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class NewsSearchResult:
    title: str
    url: str
    published_at: datetime
    description: str
    source: Optional[str]
    search_engine: List[str]
