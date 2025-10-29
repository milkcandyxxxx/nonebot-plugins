import re
import pathlib
from nonebot.plugin import on_command
from nonebot.plugin import get_loaded_plugins, PluginMetadata
from nonebot.plugin import get_loaded_plugins

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


    for plugin in get_loaded_plugins():

        meta = getattr(plugin.module, "__plugin_meta__", None)
        if meta:

            name = meta.name or plugin.name

            desc = meta.description or "（无描述）"

            usage = meta.usage or "（无用法说明）"
        else:

            name = plugin.name

            desc = "（未定义）"
            usage = "（无说明）"


        plugin_list.append(f"插件名称：{name}\n插件描述：{desc}\n插件用法：{usage}\n")


    await menu.finish("\n".join(plugin_list))