import os
import io
import aiohttp
import tempfile
import subprocess
from typing import Optional
from pydub import AudioSegment


async def generate(
    base_url: str,
    refer_wav_path: str = None,
    prompt_text: str = None,
    prompt_language: str = None,
    text: str = None,
    text_language: str = None,
    cut_punc: str = "，。",
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
                raise ValueError("生成语音时出现错误")
            return await response.read()


async def generate_v2(
    base_url: str,
    text: str,
    text_lang: str,
    ref_audio_path: str,
    aux_ref_audio_paths: Optional[list] = None,
    prompt_text: str = "",
    prompt_lang: str = "",
    top_k: int = 5,
    top_p: float = 1.0,
    temperature: float = 1.0,
    text_split_method: str = "cut3",
    batch_size: int = 1,
    batch_threshold: float = 0.75,
    split_bucket: bool = True,
    speed_factor: float = 1.0,
    fragment_interval: float = 0.3,
    streaming_mode: bool = False,
    seed: int = -1,
    parallel_infer: bool = True,
    repetition_penalty: float = 1.35,
    media_type: str = "wav",
) -> bytes:
    """Generate speech from text using GPT-SoVITS api_v2.py

    Args:
        base_url (str): Base url of the GPT-SoVITS API
        text (str): Text to be synthesized
        text_lang (str): Language of the text to be synthesized
        ref_audio_path (str): Reference audio path
        aux_ref_audio_paths (list, optional): Auxiliary reference audio paths for multi-speaker tone fusion. Defaults to None.
        prompt_text (str, optional): Prompt text for the reference audio. Defaults to "".
        prompt_lang (str, optional): Language of the prompt text for the reference audio. Defaults to "".
        top_k (int, optional): Top k sampling. Defaults to 5.
        top_p (float, optional): Top p sampling. Defaults to 1.0.
        temperature (float, optional): Temperature for sampling. Defaults to 1.0.
        text_split_method (str, optional): Text split method, "cut0": 不切, "cut1": 凑四句一切, "cut2": 凑50字一切, "cut3": 按中文句号。切, "cut4": 按英文句号.切, "cut5": 按标点符号切. Defaults to "cut3".
        batch_size (int, optional): Batch size for inference. Defaults to 1.
        batch_threshold (float, optional): Threshold for batch splitting. Defaults to 0.75.
        split_bucket (bool, optional): Whether to split the batch into multiple buckets. Defaults to True.
        speed_factor (float, optional): Control the speed of the synthesized audio. Defaults to 1.0.
        fragment_interval (float, optional): Interval between fragments in streaming mode. Defaults to 0.3.
        streaming_mode (bool, optional): Whether to return a streaming response. Defaults to False.
        seed (int, optional): Random seed for reproducibility. Defaults to -1.
        parallel_infer (bool, optional): Whether to use parallel inference. Defaults to True.
        repetition_penalty (float, optional): Repetition penalty for T2S model. Defaults to 1.35.
        media_type (str, optional): Media type of the response. Defaults to "wav".

    Raises:
        ValueError: If the response status code is 400

    Returns:
        bytes: Wav audio stream
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{base_url}/tts",
            json={
                "text": text,
                "text_lang": text_lang,
                "ref_audio_path": ref_audio_path,
                "aux_ref_audio_paths": aux_ref_audio_paths or [],
                "prompt_text": prompt_text,
                "prompt_lang": prompt_lang,
                "top_k": top_k,
                "top_p": top_p,
                "temperature": temperature,
                "text_split_method": text_split_method,
                "batch_size": batch_size,
                "batch_threshold": batch_threshold,
                "split_bucket": split_bucket,
                "speed_factor": speed_factor,
                "fragment_interval": fragment_interval,
                "streaming_mode": streaming_mode,
                "seed": seed,
                "parallel_infer": parallel_infer,
                "repetition_penalty": repetition_penalty,
                "media_type": media_type,
            },
        ) as response:
            if response.status == 400:
                raise ValueError(f"生成语音时出现错误: {await response.json()}")
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
