# from tokenize import group
#
# from nonebot import require, get_bot
#
# require("nonebot_plugin_apscheduler")
# from nonebot_plugin_apscheduler import scheduler
#
#
# async def noon_notice():
#     bot = get_bot()  # 获取一个已连接的 Bot 实例
#     group_id = 1064816676  # 目标 QQ 用户 ID
#     await bot.send_group_msg(group_id=group_id, message="🌞 2 秒过去了")
#
#
# scheduler.add_job(noon_notice, "interval", seconds = 11)
