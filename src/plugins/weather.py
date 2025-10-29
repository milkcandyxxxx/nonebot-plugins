# 导入必要的库和模块
import requests  # 用于发送HTTP请求
from nonebot import on_command  # 用于定义命令处理器
from nonebot.adapters.onebot.v11 import MessageEvent, Message  # 用于处理消息事件和消息对象
from nonebot.params import CommandArg  # 用于获取命令参数
from src.key import weaather_api_key  # 导入天气API密钥


# 定义天气图标映射表，根据天气代码显示对应的表情符号
WEATHER_EMOJI = {
    "100": "☀️",  # 晴
    "101": "🌤️",  # 晴间多云
    "102": "⛅",  # 多云
    "103": "🌥️",  # 阴
    "104": "☁️",  # 云
    "300": "🌧️",  # 雨
    "301": "🌦️",  # 阵雨
    "302": "🌧️",  # 雷雨
    "303": "⛈️",  # 雷阵雨
    "400": "🌨️",  # 雪
    "401": "❄️",  # 大雪
    "402": "🌨️",  # 雪
    "500": "🌫️",  # 雾
}


def weather_area(area):
    """
    根据城市名称获取城市ID
    :param area: 城市名称
    :return: 城市ID或错误信息
    """
    # 构建城市查询API的URL
    url_area = f"https://ku5g7ckkg2.re.qweatherapi.com/geo/v2/city/lookup?location={area}"
    # 设置请求头，包含API密钥
    headers = {
        "X-QW-Api-Key": f"{weaather_api_key}",
        "Accept-Encoding": "gzip, deflate",
    }

    # 发送GET请求
    response = requests.get(url_area, headers=headers, allow_redirects=True)
    # 检查响应状态码
    if response.status_code == 200:
        data = response.json()
        # 检查API返回状态码
        if data["code"] == "200":
            # 获取城市ID
            city_id = data["location"][0]["id"]
            return city_id
        else:
            return f"城市查询失败：{data.get('code')}"
    else:
        return f"请求地址失败，状态码：{response.status_code}"


def weather_def(city_id):
    """
    根据城市ID获取天气信息
    :param city_id: 城市ID
    :return: 天气信息字符串或错误信息
    """
    # 设置请求头，包含API密钥
    headers = {
        "X-QW-Api-Key": f"{weaather_api_key}",
        "Accept-Encoding": "gzip, deflate",
    }


    # 构建天气查询API的URL
    url_weather = f"https://ku5g7ckkg2.re.qweatherapi.com/v7/weather/now?location={city_id}"
    # 发送GET请求
    response = requests.get(url_weather, headers=headers, allow_redirects=True)
    # 检查响应状态码
    if response.status_code == 200:
        data = response.json()
        # 检查API返回状态码
        if data["code"] == "200":
            # 获取当前天气数据
            now = data["now"]
            # 根据天气代码获取对应的表情符号
            emoji = WEATHER_EMOJI.get(now["icon"], "🌈")
            # 构建天气信息字符串
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


# 定义天气命令
weather = on_command("天气")


@weather.handle()
async def handle_function(event: MessageEvent, args: Message = CommandArg()):
    """
    处理天气命令的函数
    :param event: 消息事件对象
    :param args: 命令参数
    """
    # 提取用户输入的城市名称
    city_name = args.extract_plain_text().strip()
    # 检查是否输入了城市名称
    if not city_name:
        await weather.send("请输入城市名称，例如：天气 北京")
        return

    # 获取城市ID
    city_id = weather_area(city_name)
    # 检查城市ID是否有效
    if not isinstance(city_id, str) or not city_id.isdigit():
        await weather.send(city_id)
        return

    # 获取天气信息
    weather_text = weather_def(city_id)
    # 发送天气信息
    await weather.send(weather_text)