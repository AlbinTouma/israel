import dataclasses as dc
from typing import Optional

@dc.dataclass
class WebPage:
    unique_id: Optional[str] = None
    website: Optional[str] = None
    url: Optional[str] = None
    link: Optional[str]  = None
    title: Optional[str]  = None
    media_type: Optional[str] = None
    date: Optional[str]  =None
    content: Optional[str]  = None
