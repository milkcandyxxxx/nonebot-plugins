# 导入所需的库和模块
import re  # 正则表达式库，用于文本匹配
import pathlib  # 路径处理库，用于文件系统操作
from nonebot.plugin import on_command  # 导入命令装饰器
from nonebot.plugin import get_loaded_plugins, PluginMetadata  # 导入插件相关功能
from nonebot.plugin import get_loaded_plugins  # 再次导入获取已加载插件的功能

# 定义插件的元数据，包含插件的基本信息
__plugin_meta__ = PluginMetadata(
    name="menu",  # 插件名称
    description="插件菜单查询功能",  # 插件描述
    usage="发送 '菜单' 或 '帮助' 查看所有插件信息",  # 使用说明
    homepage=None,  # 插件主页
    type="application",  # 插件类型
    config=None,  # 插件配置
    supported_adapters=None,  # 支持的适配器
    extra={},  # 额外信息
)
# 创建一个命令处理器，监听"菜单"命令，别名包括"帮助"，优先级为5，阻塞执行
menu = on_command("菜单", aliases={"帮助"}, priority=5, block=True)

# 定义菜单命令的处理函数
@menu.handle()
async def _(bot, event):
    # 初始化插件列表
    plugin_list = []

    # 遍历所有已加载的插件
    for plugin in get_loaded_plugins():
        # 获取插件的元数据，如果不存在则为None
        meta = getattr(plugin.module, "__plugin_meta__", None)
        if meta:
            # 如果有元数据，则使用元数据中的名称或插件的名称
            name = meta.name or plugin.name
            # 描述信息，如果没有则使用默认值
            desc = meta.description or "（无描述）"
            # 使用说明，如果没有则使用默认值
            usage = meta.usage or "（无用法说明）"
        else:
            # 如果没有元数据，则使用插件的名称
            name = plugin.name
            # 设置默认描述和用法说明
            desc = "（未定义）"
            usage = "（无说明）"

        # 将格式化的插件信息添加到列表中
        plugin_list.append(f"插件名称：{name}\n插件描述：{desc}\n插件用法：{usage}\n")

    # 将所有插件信息合并为一个字符串并发送
    await menu.finish("\n".join(plugin_list))