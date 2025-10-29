import os

from nonebot import on_command
from nonebot.adapters.onebot.v11 import GROUP_ADMIN, MessageEvent, Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

# 获取当前脚本所在目录的上级目录下的code_test.py
fuck_u_code = on_command("fuckcode",permission=GROUP_ADMIN | SUPERUSER)  # 创建命令处理器，支持多个别名


def fuckcode_code(code):
    with open('src/code_test.py', 'w', encoding='utf-8') as f:
        f.write(f'{code}')
    import subprocess

    try:
        # 执行命令并获取输出
        result = subprocess.run(
            ["src/fuck-u-code-windows-amd64.exe", "analyze","src/code_test.py"],
            encoding="utf-8",  # 强制用UTF-8解码
            capture_output=True,
            text=True,
            check=True
        )
        # 打印标准输出
        print("标准输出:")
        return result.stdout
    except :
        return  "执行失败"
# 处理命令的函数
@fuck_u_code.handle()  # 使用装饰器将handle_function函数注册为命令处理函数
async def handle_function(bot, event: MessageEvent, args: Message = CommandArg()):
    # 正确区分事件（event）和命令参数（args）
    content = args.extract_plain_text().strip()
    if not content:
        await fuck_u_code.finish("请在 /fuckcode 后面输入内容哦~喵~😺")
    await fuck_u_code.finish(fuckcode_code(content))

