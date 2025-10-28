
import requests
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Message
from nonebot.params import CommandArg

from src.key import weaather_api_key

key = weaather_api_key


def weather_def(area):
    url_area = f"https://ku5g7ckkg2.re.qweatherapi.com/geo/v2/city/lookup?location={area}"
    headers = {
        "X-QW-Api-Key": f"{weaather_api_key}",
        "Accept-Encoding": "gzip, deflate",
    }
    response = requests.get(
        url_area,
        headers=headers,
        allow_redirects=True
    )
    if response.status_code == 200:
        data = response.json()
        if data["code"] == "200":
            city_id = data["location"][0]["id"]
    else:
        weather = (f"请求地址失败，状态码：{response.status_code}")
    url_weather = f"https://ku5g7ckkg2.re.qweatherapi.com/v7/weather/now?location={city_id}"
    response = requests.get(
        url_weather,
        headers=headers,
        allow_redirects=True
    )
    if response.status_code == 200:
        data = response.json()
        if data["code"] == "200":
            weather = data["now"]["text"]
    else:
        weather = (f"请求天气失败，状态码：{response.status_code}")
    return weather
weather = on_command("天气")  # 创建命令处理器，支持多个别名


@weather.handle()
async def handle_function(bot, event: MessageEvent, args: Message = CommandArg()):
    area = args.extract_plain_text().strip()
    weather_text = weather_def(area)
    await weather.send(weather_text)
    # await matcher.finish(weather)