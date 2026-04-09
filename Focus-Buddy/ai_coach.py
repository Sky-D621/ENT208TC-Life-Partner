import os

import requests
from dotenv import load_dotenv


# 在程序启动时加载本地 .env 文件中的环境变量
load_dotenv()

# OpenAI 兼容接口配置
API_KEY = os.getenv("LLM_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL_NAME = "deepseek-chat"

# 接口调用失败时的备用返回
FALLBACK_TEXT = "深呼吸3次，然后闭眼休息2分钟。"


def build_system_prompt(emotion: str, mode: str) -> str:
    """
    根据干预模式，生成对应的 System Prompt。

    参数：
        emotion: 用户当前的分心状态
        mode: 干预模式，支持 empathetic 和 strict
    """
    if mode == "empathetic":
        return (
            "你是一个极具同理心的心理辅导教练。"
            f"用户目前由于【{emotion}】而感到焦虑。"
            "请在 40 个字以内，用极其温和、接纳的语气，给出一个简单的物理微动作建议"
            "（如喝水、深呼吸），帮助他们平复情绪并重新开始。"
        )

    if mode == "strict":
        return (
            "你是一个极其严厉的纪律教官。"
            f"用户目前由于【{emotion}】而试图逃避任务。"
            "你必须在 40 个字以内，用极其严厉、不留情面的命令式语气，"
            "下达一个必须立即执行的物理动作指令，打断他们的拖延行为。"
        )

    raise ValueError("mode 仅支持 'empathetic' 或 'strict'")


def get_micro_task(emotion: str, mode: str = "empathetic") -> str:
    """
    根据用户当前的分心情绪和干预模式，调用大模型生成微动作指令。

    参数：
        emotion: 用户当前的分心状态，例如“😰 焦虑”“🥱 枯燥”
        mode: 干预模式，默认值为 'empathetic'，支持 'strict'

    返回：
        模型生成的微动作指令；如果接口调用失败，则返回备用字符串。
    """
    # 如果没有读取到 API Key，直接抛出明确错误
    if not API_KEY:
        raise ValueError("未找到 LLM_API_KEY，请检查 .env 文件配置")

    system_prompt = build_system_prompt(emotion, mode)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"我的分心情绪是：{emotion}。请直接给我一个微动作指令。",
            },
        ],
        "temperature": 0.3,
        "max_tokens": 60,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()

        if content:
            return content
        return FALLBACK_TEXT

    except (requests.RequestException, KeyError, IndexError, ValueError, TypeError):
        return FALLBACK_TEXT


if __name__ == "__main__":
    # 简单本地测试：默认使用同理心模式
    test_emotion = "😰 焦虑"
    print(get_micro_task(test_emotion))
