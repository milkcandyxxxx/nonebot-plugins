import os
import requests
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent  # 正确导入事件和消息类型
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN  # 从适配器导入群管权限
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.permission import Permission, SUPERUSER  # 超级用户权限
from src.key import api_key

__plugin_meta__ = PluginMetadata(
    name="chat_with_ai",
    description="简单的ai聊天",
    usage="/猫猫 +说的话（例如：/猫猫 你好呀）",
    type="application",
)

def ai(text):
    API_KEY = f"{api_key}"
    MODEL = "doubao-seed-1-6-flash-250715"
    URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "你是一只可爱的猫咪助手，说话要活泼俏皮，每句话结尾要带「~喵~」，尽量多的使用颜文字，要耐心回答用户的问题喵~，不要输出空格(要十分简洁的回复哦！！！)"},
            {"role": "user", "content": f"{text}"}
        ],
        "thinking": {"type": "disabled"},
        "max_tokens": 100,
        "temperature": 0.7
    }

    # 增加响应状态码检查，避免报错
    response = requests.post(URL, headers=headers, json=body)
    response.raise_for_status()  # 若 API 报错直接抛出异常
    resp_json = response.json()
    return resp_json["choices"][0]["message"]["content"]

# 组合权限：超级用户 + 群管理员
# perm = SUPERUSER | GROUP_ADMIN  # 简化写法，无需套 Permission()
chat_with_ai = on_command("猫猫", priority=10, block=True, permission=GROUP_ADMIN | SUPERUSER)

@chat_with_ai.handle()
async def handle_function(bot, event: MessageEvent, args: Message = CommandArg()):
    # 正确区分事件（event）和命令参数（args）
    content = args.extract_plain_text().strip()
    if not content:
        await chat_with_ai.finish("请在 /猫猫 后面输入内容哦~喵~😺")
    await chat_with_ai.finish(ai(content))