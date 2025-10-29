import os

from nonebot.adapters.onebot.v11 import MessageEvent, Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.plugin import on_command

from src.pyfind import find

__plugin_meta__ = PluginMetadata(
    name="time",
    description="显示时间",
    usage="时间/time/几点",
    homepage=None,
    type="application",
    config=None,
    supported_adapters=None,
    extra={},
)

output_code = on_command("插件",permission=SUPERUSER)





@output_code.handle()
async def handle_function(bot, event: MessageEvent, args: Message = CommandArg()):
    content = args.extract_plain_text().strip()

    try:
        file_path = find(f"{content}.py", root_dir="src/plugins")
        if file_path is None:
            raise FileNotFoundError(f"未找到名为 {content}.py 的文件")
        with open(file_path.absolute(), 'r', encoding='utf-8') as f:
            file_content = f.read()
        await output_code.send(file_content)
    except FileNotFoundError as e:
        await output_code.send(f"{e}")

    except Exception as e:
        await output_code.send(f"读取文件时发生错误：{e}")

