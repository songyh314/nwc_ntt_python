import sympy as sym
import math
import pathlib as path


def create_folder(folder_name):
    folder_path = path.Path(folder_name)
    if not folder_path.exists():
        folder_path.mkdir()
        print("mkdir success")
    else:
        print("folder already exists")


def data_fix(data, length):
    hex_string = hex(data)[2:]  # 将数据转换为十六进制字符串，去掉前缀 '0x'
    padded_hex = hex_string.rjust(length, '0')  # 使用 '0' 填充，确保输出是定长的
    return padded_hex



def bit_rev(vec):
    j = 0
    N = len(vec)
    for i in range(1, N):
        b = N >> 1  # Initialize b to half of N
        while j >= b:
            j -= b  # Perform bit-reversal
            b >>= 1
        j += b  # Move to the next position
        # Swap elements if the bit-reversed index is greater than the current index
        if j > i:
            temp = vec[j]
            vec[j] = vec[i]
            vec[i] = temp
