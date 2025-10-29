import subprocess
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GROUP_ADMIN, MessageEvent, Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
''' 
使用的https://github.com/Done-0/fuck-u-code项目做的代码检测器
简易版
'''
__plugin_meta__ = PluginMetadata(
    name="fuck-u-code",
    description="代码分析",
    usage="fuckcode",
    homepage=None,
    type="application",
    config=None,
    supported_adapters=None,
    extra={},
)

fuck_u_code = on_command("fuckcode",permission=GROUP_ADMIN | SUPERUSER)


def fuckcode_code(code):
    #这里写法就比较史了，因为这个工具只能读取文件，所以这里把用户输入存到文件里在读取
    with open('../code_test.py', 'w', encoding='utf-8') as f:
        f.write(f'{code}')
    try:

        result = subprocess.run(
            ["src/fuck-u-code-windows-amd64.exe", "analyze","../code_test.py"],
            #return输出，而不是在终端
            capture_output=True,
            #以utf-8字符输出
            text=True,
            #检测是否运行成功，用于抛出subprocess.CalledProcessError
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        #输出运行报错，而不是捕获的e
        return  f"执行失败{result.stderr}"
    except FileNotFoundError as e:
        return  f"找不到文件{e}"
    except PermissionError as e:
        return  f"没有权限{e}"
    except OSError as e:
        return f"系统错误{e}"
    except UnicodeError as e:
        return f"编码错误{e}"
@fuck_u_code.handle()
async def handle_function(bot, event: MessageEvent, args: Message = CommandArg()):

    content = args.extract_plain_text().strip()
    if not content:
        await fuck_u_code.finish(".fuckcode 要跟东西喵")
    await fuck_u_code.finish(fuckcode_code(content))

