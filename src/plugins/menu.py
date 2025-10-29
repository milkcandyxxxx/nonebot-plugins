import re
import pathlib
from nonebot.plugin import on_command
from nonebot.plugin import get_loaded_plugins, PluginMetadata
from nonebot.plugin import get_loaded_plugins

'''
利用PluginMetadata读取插件信息，
'''
__plugin_meta__ = PluginMetadata(
    name="menu",
    description="插件菜单查询功能",
    usage="菜单/帮助",
    homepage=None,
    type="application",
    config=None,
    supported_adapters=None,
    extra={},
)
menu = on_command("菜单", aliases={"帮助"}, priority=5, block=True)


@menu.handle()
async def _(bot, event):
    plugin_list = []
    #遍历每个插件的描述
    for plugin in get_loaded_plugins():

        meta = getattr(plugin.module, "__plugin_meta__", None)
        if meta:
            #优先使用描述中的名字，再使用插件名，类似于src/menu
            name = meta.name or plugin.name
            description = meta.description or "（无描述）"
            usage = meta.usage or "（无用法说明）"
            plugin_list.append(f"插件名称：{name}\n插件描述：{description}\n插件用法：{usage}\n")
        else:
            #如果没写插件信息，仅输出插件名字
            name = plugin.name
            description = "（未定义）"
            usage = "（无说明）"
            plugin_list.append(f"插件名称：{name}\n")

    await menu.finish("\n".join(plugin_list))
