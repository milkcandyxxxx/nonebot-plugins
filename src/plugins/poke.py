import os
import platform
import re
import subprocess
from datetime import datetime
from nonebot import on_command, on_notice
from nonebot.adapters.onebot.v11 import NoticeEvent, PokeNotifyEvent, MessageEvent
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.internal.rule import Rule
from nonebot.plugin import PluginMetadata
import psutil

__plugin_meta__ = PluginMetadata(
    name="system_info",
    description="命令或戳一戳查看系统信息",
    usage="发送「系统信息」「硬件信息」或戳一戳机器人",
    homepage=None,
    type="application",
    config=None,
    supported_adapters=None,
    extra={},
)

# 1. 自定义戳一戳规则：判断是否戳的是机器人自己
def is_poke_bot() -> Rule:
    async def _is_poke_bot(event: NoticeEvent) -> bool:
        if isinstance(event, PokeNotifyEvent):
            return event.target_id == event.self_id  # 仅戳机器人时触发
        return False
    return Rule(_is_poke_bot)

# 2. 定义两个触发器（命令+戳一戳）
# 命令触发器：响应“系统信息”“硬件信息”（支持带/或不带/前缀）
command_trigger = on_command(
    "系统信息",
    aliases={"硬件信息"},
    priority=5,
    block=True
)

# 戳一戳触发器：响应戳机器人事件
poke_trigger = on_notice(
    rule=is_poke_bot(),
    priority=5,
    block=True
)

# 3. 核心逻辑函数：提取所有系统信息（共用）
async def get_all_system_info():
    # 系统基本信息
    sys_basic = (
        f"💻 操作系统：{platform.system()} {platform.release()} {platform.version()}\n"
        f"🖥️ 计算机名称：{platform.node()}\n"
        f"🏗️ 系统架构：{platform.machine()}\n"
        f"🐍 Python版本：{platform.python_version()}\n"
    )

    # CPU信息
    def get_cpu():
        try:
            system = platform.system()
            if system == "Windows":
                out = subprocess.run(
                    "wmic cpu get name /format:list", shell=True, capture_output=True, text=True, encoding="gbk"
                ).stdout or ""
                for line in out.splitlines():
                    if line.startswith("Name=") and len(line) > 5:
                        return line.split("=", 1)[1].strip()
                return "未知型号"
            if system == "Linux":
                try:
                    with open("/proc/cpuinfo", "r", encoding="utf-8") as f:
                        for line in f:
                            if line.startswith("model name"):
                                return line.split(":", 1)[1].strip()
                except Exception:
                    pass
                return "未知型号"
            if system == "Darwin":
                out = subprocess.run(
                    "sysctl -n machdep.cpu.brand_string", shell=True, capture_output=True, text=True
                ).stdout.strip()
                return out or "未知型号"
            return "未知系统"
        except Exception as e:
            return f"获取失败：{str(e)[:20]}"

    cpu_model = get_cpu()
    cpu_info = (
        f"\n🔧 CPU型号：{cpu_model}\n"
        f"🔧 物理核心：{psutil.cpu_count(logical=False)}\n"
        f"🔧 逻辑核心：{psutil.cpu_count(logical=True)}\n"
        f"🔧 使用率：{psutil.cpu_percent(interval=1)}%\n"
    )

    # 内存信息
    mem = psutil.virtual_memory()
    mem_info = (
        f"\n🧠 总内存：{round(mem.total / (1024 ** 3), 2)}GB\n"
        f"🧠 已用内存：{round(mem.used / (1024 ** 3), 2)}GB\n"
        f"🧠 空闲内存：{round(mem.free / (1024 ** 3), 2)}GB\n"
        f"🧠 使用率：{mem.percent}%\n"
    )

    # 硬盘信息
    disk_info = "\n💽 硬盘信息：\n"
    for part in psutil.disk_partitions():
        try:
            if os.name == "nt" and hasattr(part, "opts") and "cdrom" in part.opts.lower():
                continue
            usage = psutil.disk_usage(part.mountpoint)
            disk_info += (
                f"  - {part.device}：总容量 {round(usage.total / (1024 ** 3), 2)}GB，"
                f"已用 {round(usage.used / (1024 ** 3), 2)}GB，"
                f"使用率 {usage.percent}%\n"
            )
        except Exception:
            continue

    # 显卡信息
    def get_gpu():
        gpu_list = []
        try:
            system = platform.system()
            if system == "Windows":
                nvidia_info = []
                try:
                    out = subprocess.run(
                        "nvidia-smi --query-gpu=name,utilization.gpu --format=csv,noheader,nounits",
                        shell=True, capture_output=True, text=True
                    ).stdout.strip()
                    for line in out.splitlines():
                        if line.strip():
                            parts = [p.strip() for p in line.split(",")]
                            if len(parts) >= 2:
                                nvidia_info.append({"name": parts[0], "usage": f"{parts[1]}%"})
                except Exception:
                    nvidia_info = []

                wmic_out = subprocess.run(
                    "wmic path win32_videocontroller get name", shell=True, capture_output=True, text=True, encoding="gbk"
                ).stdout or ""
                all_gpus = [
                    line.strip()
                    for line in wmic_out.splitlines()
                    if line.strip() and "Name" not in line
                ]
                for gpu_name in all_gpus:
                    usage = "未知"
                    for n in nvidia_info:
                        if n["name"] in gpu_name:
                            usage = n["usage"]
                            break
                    gpu_list.append({"name": gpu_name, "usage": usage})
                return gpu_list

            if system == "Linux":
                try:
                    lspci_out = subprocess.run(
                        "lspci | grep -i 'vga\\|3d\\|display'", shell=True, capture_output=True, text=True
                    ).stdout.strip()
                except Exception:
                    lspci_out = ""
                all_gpus = [line.split(": ", 1)[-1].strip() for line in lspci_out.splitlines() if line.strip()]

                nvidia_usage = {}
                try:
                    out = subprocess.run(
                        "nvidia-smi --query-gpu=name,utilization.gpu --format=csv,noheader,nounits",
                        shell=True, capture_output=True, text=True
                    ).stdout.strip()
                    for line in out.splitlines():
                        if line.strip():
                            parts = [p.strip() for p in line.split(",")]
                            if len(parts) >= 2:
                                nvidia_usage[parts[0]] = f"{parts[1]}%"
                except Exception:
                    pass

                for gpu_name in all_gpus:
                    usage = nvidia_usage.get(gpu_name, "未知（非NVIDIA或需安装工具）")
                    gpu_list.append({"name": gpu_name, "usage": usage})
                return gpu_list

            if system == "Darwin":
                out = subprocess.run(
                    "system_profiler SPDisplaysDataType", shell=True, capture_output=True, text=True
                ).stdout or ""
                matches = re.findall(r'Chipset Model: (.+)', out)
                for name in matches:
                    gpu_list.append({"name": name.strip(), "usage": "macOS暂不支持获取使用率"})
                return gpu_list

            return [{"name": "未知系统", "usage": "未知"}]
        except Exception as e:
            return [{"name": "获取失败", "usage": f"错误：{str(e)[:20]}"}]

    gpus = get_gpu()
    gpu_info = "\n🎮 显卡信息：\n"
    for i, gpu in enumerate(gpus, 1):
        gpu_info += f"  - 显卡{i}：{gpu['name']}（使用率：{gpu['usage']}）\n"

    # 网络信息
    net_io = psutil.net_io_counters()
    net_info = (
        f"\n📶 总发送流量：{round(net_io.bytes_sent / (1024 ** 2), 2)}MB\n"
        f"📶 总接收流量：{round(net_io.bytes_recv / (1024 ** 2), 2)}MB\n"
    )

    # 运行时间信息
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    days = uptime.days
    hours = int(uptime.seconds // 3600)
    minutes = int((uptime.seconds % 3600) // 60)
    seconds = int(uptime.seconds % 60)
    boot_info = (
        f"\n⏰ 系统启动时间：{boot_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"⏰ 系统运行时间：{days}天{hours}小时{minutes}分钟{seconds}秒\n"
    )

    # 组合所有信息
    return sys_basic + cpu_info + mem_info + disk_info + gpu_info + net_info + boot_info

# 4. 两个触发器绑定到同一个处理函数
@command_trigger.handle()
async def handle_command(bot: Bot, event: MessageEvent):
    all_info = await get_all_system_info()
    await command_trigger.finish(all_info)

@poke_trigger.handle()
async def handle_poke(bot: Bot, event: PokeNotifyEvent):
    all_info = await get_all_system_info()
    await poke_trigger.finish(all_info)