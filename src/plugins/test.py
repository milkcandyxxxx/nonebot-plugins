from nonebot import on_shell_command
from nonebot.plugin import PluginMetadata
from nonebot.rule import ArgumentParser
from nonebot.adapters import Event
from nonebot.params import ShellCommandArgs

__plugin_meta__ = PluginMetadata(
    name="test",
    description="只是个测试",
    usage="/",
    homepage=None,
    type="application",
    config=None,
    supported_adapters=None,
    extra={},
)

parser = ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true")

matcher = on_shell_command("cmd", parser=parser)

@matcher.handle()
async def _(event: Event, args: dict = ShellCommandArgs()):
    await matcher.finish(str(args.get("verbose")))