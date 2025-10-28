from nonebot import on_command
from nonebot.plugin import PluginMetadata
from src.order import order

__plugin_meta__ = PluginMetadata(
    name="echo",
    description="模仿",
    usage="echo",
    homepage=None,
    type="application",
    config=None,
    supported_adapters=None,
    extra={},
)

echo = on_command("echo") # 不设置 permission，所有人可用

@echo.handle()
async def _(bot, event):
    echo_1 = order(event.get_message())  # 关键：用 str() 转换
    await echo.finish(echo_1[1])