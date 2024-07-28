# NoneBot-Plugin-GPT-SoVITS

## 介绍

**NoneBot-Plugin-GPT-SoVITS** 是一个用于对接 [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) 的 NoneBot2 插件，支持多平台适配，依赖 [nonebot-plugin-alconna](https://github.com/nonebot/plugin-alconna)。

## 功能

- 对接 GPT-SoVITS，实现 TTS（文本到语音），并发送语音消息

## 使用方法

使用指令：
- `{gpt_sovits_command} [text] [-e emotion] [-l language]` - 生成语音，可选情绪和语言
- `gptsovits帮助` - 显示帮助信息

使用示例：
- `{gpt_sovits_command} 你好` - 生成一段语音
- `{gpt_sovits_command} 你好 -e 1` - 以情绪编号 1 生成语音
- `{gpt_sovits_command} hello -e 1 -l en` - 以情绪编号 1 生成一段英文语音

可选语言：中文、英文、日文、中英混合、日英混合、多语种混合

> `gpt_sovits_command` 和 `emotion` 取决于你的配置文件设置

## 安装方法

<details open>
<summary>使用 nb-cli 安装</summary>

在 NoneBot2 项目的根目录下打开命令行，输入以下指令安装插件：

```sh
nb plugin install nonebot-plugin-gpt-sovits
```
</details>

<details>
<summary>使用包管理器安装</summary>

在 NoneBot2 项目的插件目录下，打开命令行，根据你使用的包管理器，输入相应的安装命令：

<details>
<summary>pip</summary>

```sh
pip install nonebot-plugin-gpt-sovits
```
</details>
<details>
<summary>pdm</summary>

```sh
pdm add nonebot-plugin-gpt-sovits
```
</details>
<details>
<summary>poetry</summary>

```sh
poetry add nonebot-plugin-gpt-sovits
```
</details>
<details>
<summary>conda</summary>

```sh
conda install nonebot-plugin-gpt-sovits
```
</details>

然后，打开 NoneBot2 项目根目录下的 `pyproject.toml` 文件，在 `[tool.nonebot]` 部分追加：

```toml
plugins = ["nonebot_plugin_gpt_sovits"]
```

</details>

## 配置

在 `.env` 文件中添加以下配置：

| 配置项 | 默认值 | 说明 |
| --- | --- | --- |
| GPT_SOVITS_API_BASE_URL | http://127.0.0.1:9880 | GPT-SoVITS API 的 URL |
| GPT_SOVITS_COMMAND | tts | 触发 TTS 的命令，可修改为你的 GPT-SoVITS 角色名 |
| GPT_SOVITS_CONVERT_TO_SILK | False | 是否将生成的音频转换为 SILK 格式发送，若设为 True，请进行额外配置 |
| GPT_SOVITS_EMOTION_MAP | 无默认值 | 情感映射配置，需要提供一个 Emotion 对象的列表 |
| GPT_SOVITS_CUT_PUNC | ，。 | 分割文本时使用的标点符号 |
| GPT_SOVITS_TOP_K | 10 | 采样时考虑的最高概率的标记数量 |
| GPT_SOVITS_TOP_P | 1.0 | 采样时的累积概率阈值 |
| GPT_SOVITS_TEMPERATURE | 1.0 | 生成文本的温度系数 |
| GPT_SOVITS_SPEED | 1.0 | 生成音频的速度系数 |

示例 `GPT_SOVITS_EMOTION_MAP` 配置：

```
gpt_sovits_emotion_map='[
    {
        "name": "平静",
        "sentences": [
            {
                "text": "那明镜止水给我咯，啊？",
                "language": "zh",
                "path": "D://slicer_opt/output.wav_0001036160_0001119360.wav"
            },
            {
                "text": "这火精灵真你妈傻逼。呵呵，哎呀我操我要笑死了。",
                "language": "zh",
                "path": "D://slicer_opt/output.wav_0003936960_0004098560.wav"
            },
            {
                "text": "我被连打三个三、我被连、连打三下我今天也是唐完了。",
                "language": "zh",
                "path": "D://slicer_opt/output.wav_0004921280_0005042240.wav"
            }
        ]
    },
    {
        "name": "激动",
        "sentences": [
            {
                "text": "别挂机了！你好唐，你闲着没事把自己卡在死角是吧。",
                "language": "zh",
                "path": "D://slicer_opt/output.wav_0010496000_0010624960.wav"
            },
            {
                "text": "要不是混沌历史啊，主要是，我们现在，打混沌历史那两把，boss怪全死了。",
                "language": "zh",
                "path": "D://slicer_opt/output.wav_0011990080_0012183360.wav"
            },
            {
                "text": "哼哼，第一万死绝了我操，太牛逼了！哦不是这一关了，这关，这关只有四个弓。",
                "language": "zh",
                "path": "D://slicer_opt/output.wav_0012335680_0012523200.wav"
            }
        ]
    },
    {
        "name": "生气",
        "sentences": [
            {
                "text": "你他妈下来啊，操你妈！他妈真轻容了这蜘蛛。",
                "language": "zh",
                "path": "D://slicer_opt/output.wav_0012710400_0012819520.wav"
            }
        ]    
    },
    {
        "name": "兴奋",
        "sentences": [
            {
                "text": "怎么会在我身上你跑什么！这个在，这个在。",
                "language": "zh",
                "path": "D://slicer_opt/output.wav_0013844800_0013958720.wav"
            }
        ]
    }
]'
```

## 额外配置

若你将 `GPT_SOVITS_CONVERT_TO_SILK` 设置为 `True`，请按照以下步骤进行额外配置：

1. 将 `ffmpeg` 添加到环境变量中
2. 下载 [silk_cli](https://github.com/idranme/silk-cli/releases) 的可执行文件到 Bot 的根目录，并重命名为 `cli.exe` (Windows) 或 `cli` (Linux)
3. 完成配置

