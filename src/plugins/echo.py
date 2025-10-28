from nonebot import on_command
from nonebot.plugin import PluginMetadata
from src.order import order

__plugin_meta__ = PluginMetadata(
    name="echo",
    description="模仿",
    usage="echo",
    type="application",
)

echo = on_command("echo")  # 所有人可用

@echo.handle()
async def _(bot, event):
    echo_1 = order(event.get_message())  # order 返回可能是 int
    await echo.finish(str(echo_1[1]))   # 转成字符串再发送
