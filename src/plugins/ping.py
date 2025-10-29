from nonebot import on_command  # 导入nonebot的on_command函数，用于创建命令处理器
from nonebot.plugin import PluginMetadata  # 导入PluginMetadata类，用于定义插件元数据

# 定义插件元数据，包括插件名称、描述、用法等信息
__plugin_meta__ = PluginMetadata(
    name="ping",  # 插件名称
    description="测试连接",  # 插件描述
    usage="你好",  # 插件用法
    homepage=None,  # 插件主页
    type="application",  # 插件类型
    config=None,  # 插件配置
    supported_adapters=None,  # 支持的适配器
    extra={},  # 额外信息
)

# 创建命令处理器，监听"你好"命令，不设置权限限制，所有人都可以使用
cmd_ping = on_command("你好")  # 不设置 permission，所有人可用



# 定义命令处理函数，当收到"你好"命令时触发
@cmd_ping.handle()  # 装饰器，将函数注册为命令处理器
async def _(matcher, event):  # 异步处理函数，matcher用于响应消息，event包含消息事件信息
    await matcher.finish("你女子")  # 发送响应消息"你女子"，并结束当前会话
