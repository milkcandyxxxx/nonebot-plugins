import requests
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Message
from nonebot.params import CommandArg
from src.key import weaather_api_key

key = weaather_api_key

# 天气图标表情映射（可根据需要扩展）
WEATHER_EMOJI = {
    "100": "☀️",  # 晴
    "101": "🌤️",  # 多云
    "102": "⛅",   # 少云
    "103": "🌥️",  # 晴间多云
    "104": "☁️",  # 阴
    "300": "🌧️",  # 小雨
    "301": "🌦️",  # 中雨
    "302": "🌧️",  # 大雨
    "303": "⛈️",  # 暴雨
    "400": "🌨️",  # 小雪
    "401": "❄️",  # 中雪
    "402": "🌨️",  # 大雪
    "500": "🌫️",  # 雾
}

def weather_def(area):
    url_area = f"https://ku5g7ckkg2.re.qweatherapi.com/geo/v2/city/lookup?location={area}"
    headers = {
        "X-QW-Api-Key": f"{weaather_api_key}",
        "Accept-Encoding": "gzip, deflate",
    }

    response = requests.get(url_area, headers=headers, allow_redirects=True)
    if response.status_code == 200:
        data = response.json()
        if data["code"] == "200":
            city_id = data["location"][0]["id"]
        else:
            return f"城市查询失败：{data.get('code')}"
    else:
        return f"请求地址失败，状态码：{response.status_code}"

    url_weather = f"https://ku5g7ckkg2.re.qweatherapi.com/v7/weather/now?location={city_id}"
    response = requests.get(url_weather, headers=headers, allow_redirects=True)
    if response.status_code == 200:
        data = response.json()
        if data["code"] == "200":
            now = data["now"]
            emoji = WEATHER_EMOJI.get(now["icon"], "🌈")
            weather_info = (
                f"{emoji} {now['text']}\n"
                f"温度：{now['temp']}℃（体感 {now['feelsLike']}℃）\n"
                f"风向：{now['windDir']} {now['windScale']}级\n"
                f"湿度：{now['humidity']}%\n"
                f"气压：{now['pressure']} hPa\n"
                f"能见度：{now['vis']} km\n"
                f"云量：{now['cloud']}%\n"
                f"露点温度：{now['dew']}℃"
            )
            return weather_info
        else:
            return f"天气数据获取失败：{data.get('code')}"
    else:
        return f"请求天气失败，状态码：{response.status_code}"


weather = on_command("天气")


@weather.handle()
async def handle_function(bot, event: MessageEvent, args: Message = CommandArg()):
    area = args.extract_plain_text().strip()
    weather_text = weather_def(area)
    await weather.send(weather_text)
