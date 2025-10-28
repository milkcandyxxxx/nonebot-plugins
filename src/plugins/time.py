# 导入必要的库
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

# 注册命令"时间"，并设置别名"time"和"几点"
weather = on_command("时间",aliases={"time", "几点"})




# 处理命令的函数
@weather.handle()
async def handle_function():
    # 获取当前时间
    now = datetime.now()
    # 获取时间
    time_hm = now.strftime("%H:%M")
    # 12小时制（如：08:55）
    # time_hm = now.strftime("%I:%M")
    await weather.finish("时间是"+time_hm)
