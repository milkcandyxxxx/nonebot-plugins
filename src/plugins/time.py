from nonebot import on_command
from datetime import datetime
from nonebot.rule import to_me
from nonebot.plugin import on_command

from nonebot.plugin import PluginMetadata

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

weather = on_command("时间",aliases={"time", "几点"})




@weather.handle()
async def handle_function():
    now = datetime.now()
    time_hm = now.strftime("%H:%M")
    await weather.finish("时间是"+time_hm)
