import sympy as sym
import math
import pathlib as path
import numpy as np
import param


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


def negacyclic_conv(a, b):
    """
    计算两个向量 a 和 b 的负环卷积
    :param a: 输入向量 1
    :param b: 输入向量 2
    :return: 负环卷积的结果
    """
    n = len(a)
    # 结果的初始化
    result = np.zeros(n)

    for k in range(n):
        for i in range(n):
            # 计算索引并处理负环效应
            j = (k - i) % n
            # 判断是否要引入负号
            sign = -1 if (k - i) >= n else 1
            result[k] += a[i] * b[j] * sign

    return result


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


def genBinComplement(num, bitLen):
    if num < 0:
        num = (1 << bitLen) + num
    else:
        num & ((1 << bitLen) - 1)
    str = format(num, f'0{bitLen}b')
    return str


def getLowBits(din, bitLen):
    """
        截取输入二进制的低bitLen位
        :param din: input unsigned/signed
        :param bitLen: 截取的位数
        :return: 低bitLen位结果
        """
    mask = (1 << bitLen) - 1
    lsb = din & mask
    return lsb


def main():
    din = -1
    bitLen = 4
    lsb = getLowBits(din, bitLen)
    print(genBinComplement(din, 8))
    print(lsb)
    print(format(lsb, '04b'))


def naiveConvModQ(a, b, q):
    N = len(a)
    res = list(0 for _ in range(N))
    for i in range(N):
        tmp = 0
        for j in range(N):
            if j <= i:
                tmp += (a[j] * b[i - j]) % q
            else:
                tmp -= (a[j] * b[N + i - j]) % q
        tmp = getLowBits(tmp, 8)
        if tmp >= q:
            res[i] = tmp - (q << 1)
        else:
            res[i] = tmp

    return res


if __name__ == '__main__':
    main()
