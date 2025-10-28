def order(command_str):
    command_str=str(command_str)
    parts = [p for p in command_str.strip().split(" ") if p]
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