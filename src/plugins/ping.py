from nonebot import on_command
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="ping",
    description="测试连接",
    usage="你好",
    homepage=None,
    type="application",
    config=None,
    supported_adapters=None,
    extra={},
)

cmd_ping = on_command("你好")  # 不设置 permission，所有人可用

@cmd_ping.handle()
async def _(matcher, event):
    await matcher.finish("你女子")
