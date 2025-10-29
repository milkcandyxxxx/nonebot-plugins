from email.message import Message
import base64
import aiohttp
import aiofiles
from pathlib import Path
from datetime import datetime
from nonebot import on_command
from nonebot.adapters.onebot.v11 import ActionFailed, MessageSegment
from nonebot.permission import SUPERUSER
from nonebot.exception import FinishedException


user_information_acquisition = on_command(
    "获取用户信息",
    aliases={"获取用户信息"},
    permission=SUPERUSER
)


AVATAR_CACHE_DIR = Path(__file__).parent.parent / "avatar_cache"


@user_information_acquisition.handle()
async def _(bot, event):

    content = event.get_plaintext().strip().replace(".获取用户信息", "").strip()
    if not content.isdigit() or len(content) < 5 or len(content) > 13:
        await user_information_acquisition.finish("请输入合法的QQ号")

    try:

        AVATAR_CACHE_DIR.mkdir(exist_ok=True, parents=True)


        user_info = await bot.get_stranger_info(user_id=content)

        qq = content
        nickname = user_info.get("nickname", user_info.get("nick", "未知昵称"))
        long_nick = user_info.get("long_nick", user_info.get("longNick", "无"))
        qid = user_info.get("qid", "无")

        sex = user_info.get("sex", "未知")
        sex = "男" if sex == "male" else "女" if sex == "female" else sex
        country = user_info.get("country", "无")
        city = user_info.get("city", "无")

        reg_time = user_info.get("reg_time", user_info.get("regTime", 0))
        reg_time = datetime.fromtimestamp(reg_time).strftime("%Y") if reg_time else "未知"

        qq_level = user_info.get("qqLevel", 0)
        is_vip = "是" if user_info.get("is_vip", False) else "否"
        vip_level = user_info.get("vip_level", 0)


        avatar_url = f"https://q1.qlogo.cn/g?b=qq&nk={content}&s=100"
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url, timeout=5) as resp:
                if resp.status != 200:
                    await user_information_acquisition.finish(f"昵称：{nickname}\n头像获取失败")
                img_data = await resp.read()


        img_save_path = AVATAR_CACHE_DIR / f"{content}.jpg"
        async with aiofiles.open(img_save_path, "wb") as f:
            await f.write(img_data)


        info_text = (
            f"QQ号：{qq}\n"
            f"昵称：{nickname}\n"
            f"个性签名：{long_nick}\n"
            f"QID：{qid}\n"
            f"性别：{sex}\n"
            f"国家：{country}\n"
            f"城市：{city}\n"
            f"注册时间：{reg_time}\n"
            f"QQ等级：{qq_level}\n"
            f"是否VIP：{is_vip}\n"
            f"VIP等级：{vip_level}\n"
        )


        img_base64 = base64.b64encode(img_data).decode()
        image_msg = MessageSegment.image(f"base64://{img_base64}")
        await user_information_acquisition.finish(info_text + image_msg)

    except FinishedException:
        pass
    except ActionFailed as e:
        await user_information_acquisition.finish(f"查询失败：{str(e)}")
    except aiohttp.ClientError as e:
        await user_information_acquisition.finish(f"图片下载失败：{str(e)}")
    except aiofiles.os.OSError as e:
        await user_information_acquisition.finish(f"目录创建/文件保存失败：{str(e)}")
    except Exception as e:
        await user_information_acquisition.finish(f"程序异常：{str(e)}")