import shlex

def order(command_str):
    """
    将输入的命令字符串转换为包含整数、浮点数和字符串的列表
    支持用引号包裹的参数（如 "New York"）

    参数:
        command_str (str): 输入的命令字符串

    返回:
        list: 包含转换后的元素，可能是整数、浮点数或字符串
    """
    command_str = str(command_str)
    # 使用 shlex.split 支持引号包裹的字符串
    try:
        parts = shlex.split(command_str)
    except ValueError:
        # 解析失败就按普通空格拆分
        parts = [p for p in command_str.strip().split(" ") if p]

    result = []
    for p in parts:
        try:
            result.append(int(p))
        except ValueError:
            try:
                result.append(float(p))
            except ValueError:
                result.append(p)
    return result
