from dataclasses import dataclass
from typing import List


@dataclass
class PictureRaw:
    width: int
    height: int
    pic_url: str


@dataclass
class MangaRaw:
    name: str
    url: str
    next_chapter_url: str
    prev_chapter_url: str
    length: int
    pics_raw: List[PictureRaw]
