import os
import io
import aiohttp
import tempfile
import subprocess
from nonebot.log import logger
from pydub import AudioSegment


async def generate(
    base_url: str,
    refer_wav_path: str = None,
    prompt_text: str = None,
    prompt_language: str = None,
    text: str = None,
    text_language: str = None,
    cut_punc: str = None,
    top_k: int = 10,
    top_p: float = 1.0,
    temperature: float = 1.0,
    speed: float = 1.0,
) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{base_url}/",
            json={
                "refer_wav_path": refer_wav_path,
                "prompt_text": prompt_text,
                "prompt_language": prompt_language,
                "text": text,
                "text_language": text_language,
                "cut_punc": cut_punc,
                "top_k": top_k,
                "top_p": top_p,
                "temperature": temperature,
                "speed": speed,
            },
        ) as response:
            if response.status == 400:
                logger.error(f"生成语音时出现错误：{await response.json()}")
                raise ValueError("生成语音时出现错误")
            return await response.read()


def get_wav_duration(wav_bytes: bytes) -> float:
    audio = AudioSegment.from_file(io.BytesIO(wav_bytes), format="wav")
    return len(audio) / 1000


def _encode(
    input_path: str, output_path: str, sampling_rate: str = "24000", cli: str = "./cli"
):
    subprocess.run([cli, "-i", input_path, "-o", output_path, "-s", sampling_rate])


def encode_to_silk(file: bytes, format: str = "wav") -> bytes:
    with tempfile.NamedTemporaryFile(
        suffix=f".{format}", delete=False
    ) as temp_input_file:
        temp_input_file.write(file)

    with tempfile.NamedTemporaryFile(suffix=".raw", delete=False) as temp_pcm_file:
        pass

    ffmpeg_cmd = f"ffmpeg -i {temp_input_file.name} -f s16le -acodec pcm_s16le -ar 24000 -ac 1 {temp_pcm_file.name}"
    subprocess.run(
        ffmpeg_cmd,
        input=b"y",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    os.unlink(temp_input_file.name)

    with tempfile.NamedTemporaryFile(suffix=".silk", delete=False) as temp_output_file:
        pass

    _encode(temp_pcm_file.name, temp_output_file.name)

    with open(temp_output_file.name, "rb") as encoded_file:
        encoded_data = encoded_file.read()

    os.unlink(temp_pcm_file.name)
    os.unlink(temp_output_file.name)

    return encoded_data
