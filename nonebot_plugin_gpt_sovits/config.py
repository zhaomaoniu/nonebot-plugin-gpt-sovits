import pydantic
from typing import Optional, List

from .models import Emotion


class Config(pydantic.BaseModel):
    gpt_sovits_api_base_url: Optional[str] = "http://127.0.0.1:9880"
    gpt_sovits_api_v2: Optional[bool] = True
    gpt_sovits_command: Optional[str] = "tts"
    gpt_sovits_emotion_map: List[Emotion]
    gpt_sovits_args: Optional[dict] = {}
