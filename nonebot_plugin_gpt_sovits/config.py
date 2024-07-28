import pydantic
from typing import Optional, Dict, List

from .models import Emotion


class Config(pydantic.BaseModel):
    gpt_sovits_api_base_url: Optional[str] = "http://127.0.0.1:9880"
    gpt_sovits_command: Optional[str] = "tts"
    gpt_sovits_convert_to_silk: Optional[bool] = False
    gpt_sovits_emotion_map: List[Emotion]
    gpt_sovits_cut_punc: Optional[str] = "，。"
    gpt_sovits_top_k: Optional[int] = 10
    gpt_sovits_top_p: Optional[float] = 1.0
    gpt_sovits_temperature: Optional[float] = 1.0
    gpt_sovits_speed: Optional[float] = 1.0
