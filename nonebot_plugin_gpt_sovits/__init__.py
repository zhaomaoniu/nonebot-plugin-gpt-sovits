import random
import nonebot
from nonebot.log import logger
from nonebot import require, on_command
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import (
    Args,
    Field,
    Voice,
    Option,
    Arparma,
    Alconna,
    on_alconna,
)

from .config import Config
from .utils import generate, generate_v2, get_wav_duration, encode_to_silk


if hasattr(nonebot, "get_plugin_config"):
    plugin_config = nonebot.get_plugin_config(Config)
else:
    from nonebot import get_driver

    plugin_config = Config.parse_obj(get_driver().config)


__plugin_meta__ = PluginMetadata(
    name="GPT-SoVITS 语音合成",
    description="调用 GPT-SoVITS 的 API 生成语音",
    usage=f"{plugin_config.gpt_sovits_command} [text] [-e emotion] [-l language]",
    type="application",
    homepage="https://github.com/zhaomaoniu/nonebot-plugin-gpt-sovits",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
)


emotion_map = {
    index: emotion.name
    for index, emotion in enumerate(plugin_config.gpt_sovits_emotion_map)
}
emotion_options = "\n".join(
    [f"{index}: {emotion}" for index, emotion in emotion_map.items()]
)


tts = on_alconna(
    Alconna(
        plugin_config.gpt_sovits_command,
        Args["text", str, Field(completion=lambda: "请输入要转换的文本")],
        Option(
            "-e",
            alias=["--emotion"],
            args=Args[
                "emotion",
                str,
                Field(
                    completion=lambda: f"请输入要转换的情绪，可选情绪：\n{emotion_options}"
                ),
            ],
            default="0",
            help_text=f"可选情绪：\n{emotion_options}",
        ),
        Option(
            "-l",
            alias=["--language"],
            args=Args[
                "language",
                str,
                Field(
                    completion=lambda: "请输入要转换的语言，可选语言：中文、英文、日文、中英混合、日英混合、多语种混合"
                ),
            ],
            default="auto",
            help_text="可选语言：中文、英文、日文、中英混合、日英混合、多语种混合",
        ),
    ),
    use_cmd_start=True,
    auto_send_output=True,
    comp_config={"lite": True},
    skip_for_unmatch=False,
    priority=10,
)
help_matcher = on_command(
    "gptsovits帮助", priority=10, block=True, aliases={"gsv帮助", "gsvhelp"}
)


@tts.handle()
async def handle_tts(arp: Arparma):
    text: str = arp.main_args["text"]
    emotion_index: str = arp.options["e"].args["emotion"] or arp.other_args["emotion"]
    text_language: str = arp.options["l"].args["language"] or arp.other_args["language"]

    emotion = plugin_config.gpt_sovits_emotion_map[int(emotion_index)]
    sentence = random.choice(emotion.sentences)

    refer_wav_path = sentence.path
    prompt_text = sentence.text
    prompt_language = sentence.language
    base_url = plugin_config.gpt_sovits_api_base_url

    if plugin_config.gpt_sovits_api_v2:
        try:
            wav_file = await generate_v2(
                base_url,
                text,
                text_language,
                refer_wav_path,
                prompt_text=prompt_text,
                prompt_lang=prompt_language,
                **{
                    k: v
                    for k, v in plugin_config.gpt_sovits_args.items()
                    if k
                    in [
                        "aux_ref_audio_paths",
                        "top_k",
                        "top_p",
                        "temperature",
                        "text_split_method",
                        "batch_size",
                        "batch_threshold",
                        "split_bucket",
                        "speed_factor",
                        "fragment_interval",
                        "streaming_mode",
                        "seed",
                        "parallel_infer",
                        "repetition_penalty",
                    ]
                },
            )
        except ValueError as e:
            logger.error(f"生成语音时出现错误：{e}")
            await tts.finish("生成语音时出现错误，请联系 Bot 维护者查看日志")
    else:

        try:
            wav_file = await generate(
                base_url,
                refer_wav_path=refer_wav_path,
                prompt_text=prompt_text,
                prompt_language=prompt_language,
                text=text,
                text_language=text_language,
                **{
                    k: v
                    for k, v in plugin_config.gpt_sovits_args.items()
                    if k in ["cut_punc", "top_k", "top_p", "temperature", "speed"]
                },
            )
        except ValueError as e:
            logger.error(f"生成语音时出现错误：{e}")
            await tts.finish("生成语音时出现错误，请联系 Bot 维护者查看日志")

    duration = int(get_wav_duration(wav_file))
    silk_file = encode_to_silk(wav_file)
    await tts.finish(Voice(raw=silk_file, mimetype="audio/silk", duration=duration))


@help_matcher.handle()
async def handle_help():
    await help_matcher.finish(
        "GPT-SoVITS 插件帮助\n"
        "使用方法：\n"
        f"   {plugin_config.gpt_sovits_command} [text] [-e emotion] [-l language] - 生成语音，可选情绪和语言\n"
        "   gptsovits帮助 - 显示本帮助\n"
        "使用示例：\n"
        f"   {plugin_config.gpt_sovits_command} 你好 - 生成一段语音\n"
        f"   {plugin_config.gpt_sovits_command} 你好 -e 1 - 以序号为 1 的情绪生成一段语音\n"
        f"   {plugin_config.gpt_sovits_command} hello -e 1 -l en - 以序号为 1 的情绪生成一段英文语音\n"
        f"可选情绪：\n{emotion_options}\n"
        f"可选语言：中文、英文、日文、中英混合、日英混合、多语种混合\n"
        f"(记得加上命令头，可用命令头: {nonebot.get_driver().config.command_start})"
    )
