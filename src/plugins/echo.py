from nonebot import on_command
from nonebot.plugin import PluginMetadata
from src.order import order

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
    await echo.finish(str(echo_1[1]))
