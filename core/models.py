import dataclasses as dc

@dc.dataclass
class WebPage:
    unique_id: str = None
    website: str = None
    url: str = None
    link: str = None
    title: str = None
    media_type: str = None
    date: str =None
    content: str = None
