def order(command_str):

    """
    将输入的命令字符串转换为包含整数、浮点数和字符串的列表

    参数:
        command_str (str): 输入的命令字符串

    返回:
        list: 包含转换后的元素，可能是整数、浮点数或字符串
    """
    command_str=str(command_str)  # 确保输入为字符串类型
    parts = [p for p in command_str.strip().split(" ") if p]  # 分割字符串并去除空元素
    result = []
    for p in parts:
        try:
            result.append(int(p))      # 尝试整数
        except ValueError:
            try:
                result.append(float(p)) # 尝试浮点数
            except ValueError:
                result.append(p)        # 否则保留字符串
    return result