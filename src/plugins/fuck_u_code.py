import subprocess

from nonebot import on_command
from nonebot.adapters.onebot.v11 import GROUP_ADMIN, MessageEvent, Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="fuck-u-code",
    description="代码分析",
    usage="fuckcode",
    homepage=None,
    type="application",
    config=None,
    supported_adapters=None,
    extra={},
)

fuck_u_code = on_command("fuckcode",permission=GROUP_ADMIN | SUPERUSER)


def fuckcode_code(code):
    with open('../code_test.py', 'w', encoding='utf-8') as f:
        f.write(f'{code}')


    try:

        result = subprocess.run(
            ["src/fuck-u-code-windows-amd64.exe", "analyze","../code_test.py"],
            encoding="utf-8",
            capture_output=True,
            text=True,
            check=True
        )

        print("标准输出:")
        return result.stdout
    except :
        return  "执行失败"
@fuck_u_code.handle()
async def handle_function(bot, event: MessageEvent, args: Message = CommandArg()):

    content = args.extract_plain_text().strip()
    if not content:
        await fuck_u_code.finish(".fuckcode 要跟东西喵")
    await fuck_u_code.finish(fuckcode_code(content))

