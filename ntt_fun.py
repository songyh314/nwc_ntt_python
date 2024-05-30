import sympy as sym
import math
import pathlib as path


def modExponent(base, power, M):
    result = 1
    power = int(power)
    base = base % M
    while power > 0:
        if power & 1:
            result = (result * base) % M
        base = (base * base) % M
        power = power >> 1
    return result


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


def modInv(x, M):
    t, new_t, r, new_r = 0, 1, M, x
    while new_r != 0:
        quotient = int(r / new_r)
        # tmp_new_t = new_t
        # tmp_t = t
        # tmp_new_r = new_r
        # tmp_r = r
        t, new_t = new_t, (t - quotient * new_t)
        r, new_r = new_r, (r % new_r)
    if r > 1:
        return "x is not invertible."
    if t < 0:
        t = t + M
    return int(t)


def gen_tw(base1, base2, tw_len, ntt_points):
    bas1 = base1
    bas2 = base2
    tw_len = tw_len
    p = (2 ** bas1 - 2 ** bas2 + 1)
    g = sym.primitive_root(p)

    N = int(ntt_points)
    path = "./rom"
    # os.mkdir(path)
    folder_name = "rom"
    create_folder(folder_name)
    n_arry = [str(N)]
    f_str = path + "/tw" + str(int(N)) + ".coe"
    f_arry = [f_str]
    if_str = path + "/inv_tw" + str(int(N)) + ".coe"
    if_arry = [if_str]
    cnt = int(math.log2(N))
    while 1:
        N /= 2
        f_str = path + "/tw" + str(int(N)) + ".coe"
        if_str = path + "/inv_tw" + str(int(N)) + ".coe"
        if N == 2:
            break
        n_arry.append(str(int(N)))
        f_arry.append(f_str)
        if_arry.append(if_str)
    # print(f_arry, if_arry, n_arry)

    for i in range(cnt - 1):
        with open(f_arry[i], 'w+') as fp:
            # print(int(n_arry[i]))
            fp.write("memory_initialization_radix = 16;\n")
            fp.write("memory_initialization_vector =\n")
            q = int((p - 1) / int(n_arry[i]))
            # print(q,n_arry[i])
            for k in range(int(int(n_arry[i]) / 2)):
                km = int(k * q)
                w = pow(g, km, p)
                tw_str = data_fix(w, int(tw_len / 4))
                if k == (int(int(n_arry[i]) / 2) - 1):
                    fp.write(tw_str + "\n")
                else:
                    fp.write(tw_str + "," + "\n")
        pass
    pass

    for i in range(cnt - 1):
        with open(if_arry[i], 'w+') as ifp:
            # print(int(n_arry[i]))
            ifp.write("memory_initialization_radix = 16;\n")
            ifp.write("memory_initialization_vector =\n")
            q = int((p - 1) / int(n_arry[i]))
            # print(q,n_arry[i])
            for j in range(int(int(n_arry[i]) / 2)):
                kn = int(j * q)
                w_t = pow(g, kn, p)
                iw = modInv(w_t, p)
                inv_tw_str = data_fix(iw, int(tw_len / 4))
                if j == (int(int(n_arry[i]) / 2) - 1):
                    ifp.write(inv_tw_str + "\n")
                else:
                    ifp.write(inv_tw_str + "," + "\n")
        pass
    pass


def get_param(mod):
    g = sym.primitive_root(mod)
