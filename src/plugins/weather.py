import requests
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from src.key import weaather_api_key

__plugin_meta__ = PluginMetadata(
    name="weather",
    description="获取天气信息",
    usage="天气+地区",
    homepage=None,
    type="application",
    config=None,
    supported_adapters=None,
    extra={},
)



WEATHER_EMOJI = {
    "100": "☀️",
    "101": "🌤️",
    "102": "⛅",
    "103": "🌥️",
    "104": "☁️",
    "300": "🌧️",
    "301": "🌦️",
    "302": "🌧️",
    "303": "⛈️",
    "400": "🌨️",
    "401": "❄️",
    "402": "🌨️",
    "500": "🌫️",
}


def weather_area(area):


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
            return city_id
        else:
            return "城市查询失败"
    else:
        return "请求地址失败"


def weather_def(city_id):

    headers = {
        "X-QW-Api-Key": f"{weaather_api_key}",
        "Accept-Encoding": "gzip, deflate",
    }


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
async def handle_function(event: MessageEvent, args: Message = CommandArg()):

    city_name = args.extract_plain_text().strip()
    if not city_name:
        await weather.send("请输入城市名称，例如：天气 北京")
        return

    city_id = weather_area(city_name)
    if not isinstance(city_id, str) or not city_id.isdigit():
        await weather.send(city_id)
        return

    weather_text = weather_def(city_id)
    await weather.send(weather_text)