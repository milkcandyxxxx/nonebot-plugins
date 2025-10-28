# 导入必要的库
from nonebot import on_command  # 导入nonebot库中的on_command函数，用于注册命令
from datetime import datetime    # 导入datetime模块，用于处理时间相关操作
from nonebot.rule import to_me  # 导入to_me规则，用于判断消息是否发送给机器人
from nonebot.plugin import on_command  # 再次导入on_command，可能是为了代码清晰或后续扩展

from nonebot.plugin import PluginMetadata  # 导入PluginMetadata类，用于定义插件元信息

# 定义插件元信息，包含插件的基本描述和使用说明
__plugin_meta__ = PluginMetadata(
    name="time",                    # 插件名称
    description="显示时间",         # 插件功能描述
    usage="时间/time/几点",         # 插件命令使用方法
    homepage=None,                 # 插件主页，设为None表示无
    type="application",            # 插件类型
    config=None,                   # 插件配置，设为None表示无
    supported_adapters=None,       # 支持的适配器，设为None表示无限制
    extra={},                      # 额外信息，空字典表示无
)

# 注册命令"时间"，并设置别名"time"和"几点"
weather = on_command("时间",aliases={"time", "几点"})  # 创建命令处理器，支持多个别名




# 处理命令的函数
@weather.handle()  # 使用装饰器将handle_function函数注册为命令处理函数
async def handle_function():  # 定义异步处理函数
    # 获取当前时间
    now = datetime.now()  # 获取当前系统时间
    # 获取时间
    time_hm = now.strftime("%H:%M")  # 将时间格式化为24小时制（如：20:55）
    # 12小时制（如：08:55）
    # time_hm = now.strftime("%I:%M")  # 注释掉的代码，用于实现12小时制时间格式
    await weather.finish("时间是"+time_hm)  # 发送格式化后的时间文本
