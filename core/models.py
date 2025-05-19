import dataclasses as dc

@dc.dataclass
class WebPage:
    website: str = None
    url: str = None
    link: str = None
    title: str = None
    media_type: str = None
    date: str =None
    content: str = None