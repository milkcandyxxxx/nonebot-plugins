import requests
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata

from src.key import ai_api_key


__plugin_meta__ = PluginMetadata(
    name="chat_with_ai",
    description="简单的ai聊天",
    usage="猫猫",
    type="application",
)



def ai(text):
    API_KEY = f"{ai_api_key}"
    MODEL = "doubao-seed-1-6-flash-250715"
    URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "system",
             "content": "你是一只可爱的猫咪助手，说话要活泼俏皮，每句话结尾要带「~喵~」，尽量多的使用颜文字，要耐心回答用户的问题喵~，不要输出空格(要十分简洁的回复哦！！！)"},
            {"role": "user", "content": f"{text}"}
        ],
        "thinking": {"type": "disabled"},
        "max_tokens": 100,
        "temperature": 0.7
    }

    response = requests.post(URL, headers=headers, json=body)
    response.raise_for_status()
    resp_json = response.json()
    return resp_json["choices"][0]["message"]["content"]


chat_with_ai = on_command("猫猫", priority=10, block=True, permission=GROUP_ADMIN | SUPERUSER)


@chat_with_ai.handle()
async def handle_function(bot, event: MessageEvent, args: Message = CommandArg()):

    content = args.extract_plain_text().strip()
    if not content:
        await chat_with_ai.finish("请在 /猫猫 后面输入内容哦~喵~")
    await chat_with_ai.finish(ai(content))
