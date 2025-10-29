from nonebot import on_command
from nonebot.plugin import PluginMetadata
from src.order import order
''' 
使用我的很傻的命令解释器写的echo...qwq
'''
__plugin_meta__ = PluginMetadata(
    name="echo",
    description="模仿",
    usage="echo",
    type="application",
)

echo = on_command("echo")

@echo.handle()
async def _(bot, event):
    echo_1 = order(event.get_message())
    #输出第一个参数，实际后面有shell_on_command来解析参数，当时写的时候没注意
    await echo.finish(str(echo_1[1]))
