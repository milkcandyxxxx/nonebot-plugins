# 导入必要的库
import os

from nonebot import on_command  # 导入nonebot库中的on_command函数，用于注册命令
from datetime import datetime    # 导入datetime模块，用于处理时间相关操作

from nonebot.adapters.onebot.v11 import GROUP_ADMIN, MessageEvent, Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
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
output_code = on_command("插件",permission=SUPERUSER)  # 创建命令处理器，支持多个别名




# 处理命令的函数
@output_code.handle()
async def handle_function(bot, event: MessageEvent, args: Message = CommandArg()):
    content = args.extract_plain_text().strip()

    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, f"{content}.py")
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        await output_code.send(file_content)
    except Exception as e:
        await output_code.send(f"读取文件时发生错误：{str(e)}")

    # except Exception as e:
    #     await output_code.send(f"读取文件时发生错误：{str(e)}")