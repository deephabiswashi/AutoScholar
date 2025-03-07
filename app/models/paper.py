from pydantic import BaseModel
from typing import List, Optional

class Paper(BaseModel):
    id: Optional[str]
    title: str
    abstract: Optional[str]
    full_text: str
    authors: List[str]
    publication_date: str
