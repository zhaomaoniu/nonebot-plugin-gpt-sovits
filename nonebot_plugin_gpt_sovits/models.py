from typing import List
from pydantic import BaseModel


dict_language = {
    "中文": "all_zh",
    "英文": "en",
    "日文": "all_ja",
    "中英混合": "zh",
    "日英混合": "ja",
    "多语种混合": "auto",
    "all_zh": "all_zh",
    "en": "en",
    "all_ja": "all_ja",
    "zh": "zh",
    "ja": "ja",
    "auto": "auto",
}


class Sentence(BaseModel):
    text: str
    path: str
    language: str


class Emotion(BaseModel):
    name: str
    sentences: List[Sentence]
