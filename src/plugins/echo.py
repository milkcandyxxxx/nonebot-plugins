from nonebot import on_command  # 导入 nonebot 的 on_command 命令装饰器
from nonebot.plugin import PluginMetadata  # 导入 nonebot 的 PluginMetadata 类，用于插件元数据
from src.order import order  # 导入 src.order 模块中的 order 函数

__plugin_meta__ = PluginMetadata(  # 定义插件元数据
    name="echo",  # 插件名称
    description="模仿",  # 插件描述
    usage="echo",  # 插件使用方法
    type="application",  # 插件类型
)

echo = on_command("echo")  # 所有人可用

@echo.handle()
async def _(bot, event):
    echo_1 = order(event.get_message())  # order 返回可能是 int
    await echo.finish(str(echo_1[1]))   # 转成字符串再发送
