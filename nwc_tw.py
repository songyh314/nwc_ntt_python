import numpy as np
import math
import sympy as sym
import ntt_fun
import param
import pathlib as path
import tool


class NWC_PARAM:
    def __init__(self, lvl):
        self.lvl = lvl
        self.w_rom = []
        self.inv_w_rom = []


class TW_ROM:
    def __init__(self, N):
        self.N = N
        self.w_n = N >> 1
        self.phi_n = N
        self.tw_factor = []
        self.inv_tw_factor = []
        self.phi_factor = []
        self.inv_phi_factor = []


def gen_tw(tw_rom):
    w_n = tw_rom.w_n
    phi_n = tw_rom.phi_n
    w_q = int((param.MOD - 1) / (w_n << 1))
    phi_q = int((param.MOD - 1) / (phi_n << 1))
    for i in range(w_n):
        w_exp_index = i * w_q
        temp = int(pow(param.g, w_exp_index, param.MOD))
        tw_rom.tw_factor.append(temp)
        tw_rom.inv_tw_factor.append(ntt_fun.modInv(temp, param.MOD))
    for j in range(phi_n):
        phi_exp_index = j * phi_q
        temp_phi = int(pow(param.g, phi_exp_index, param.MOD))
        tw_rom.phi_factor.append(temp_phi)
        tw_rom.inv_phi_factor.append(ntt_fun.modInv(temp_phi, param.MOD))


def genTwModQ(tw_rom, MOD):
    w_n = tw_rom.w_n
    phi_n = tw_rom.phi_n
    g = sym.primitive_root(MOD)
    w_q = int((MOD - 1) / (w_n << 1))
    phi_q = int((MOD - 1) / (phi_n << 1))
    for i in range(w_n):
        w_exp_index = i * w_q
        temp = int(pow(g, w_exp_index, MOD))
        tw_rom.tw_factor.append(temp)
        tw_rom.inv_tw_factor.append(ntt_fun.modInv(temp, MOD))
    for j in range(phi_n):
        phi_exp_index = j * phi_q
        temp_phi = int(pow(g, phi_exp_index, MOD))
        tw_rom.phi_factor.append(temp_phi)
        tw_rom.inv_phi_factor.append(ntt_fun.modInv(temp_phi, MOD))


def genNWC(tw_rom, nwc_param, nwc_str):
    (scale, tw_size, phi_probe) = (0, 0, 0)
    (tw_temp, phi_temp, nwc_temp) = (0, 0, 0)
    lvl = nwc_param.lvl
    n = tw_rom.N
    w_n = tw_rom.w_n
    phi_n = tw_rom.phi_n
    if nwc_str == "NWC-DIT-NR-NNT":
        for i in range(lvl):
            tw_size = n >> (lvl - i)
            phi_probe = n >> (i + 1)
            scale = w_n >> i
            tw_vec = []
            for j in range(tw_size):
                tw_temp = tw_rom.tw_factor[j * scale]
                phi_temp = tw_rom.phi_factor[phi_probe]
                nwc_temp = (tw_temp * phi_temp) % param.MOD
                tw_vec.append(nwc_temp)
            tool.bit_rev(tw_vec)
            nwc_param.w_rom.append(tw_vec)
    if nwc_str == "DIT-NR-NNT":
        for i in range(lvl):
            tw_size = n >> (lvl - i)
            phi_probe = n >> (i + 1)
            scale = w_n >> i
            tw_vec = []
            for j in range(tw_size):
                tw_temp = tw_rom.tw_factor[j * scale]
                # phi_temp = tw_rom.phi_factor[phi_probe]
                # nwc_temp = (tw_temp * phi_temp) % param.MOD
                tw_vec.append(tw_temp)
            tool.bit_rev(tw_vec)
            nwc_param.w_rom.append(tw_vec)
    if nwc_str == "NWC-DIF-RN-INNT":
        for i in range(lvl):
            tw_size = 1 << (lvl - i - 1)
            phi_probe = 1 << i
            scale = 1 << i
            inv_tw_vec = []
            for k in range(tw_size):
                tw_temp = tw_rom.inv_tw_factor[k * scale]
                phi_temp = tw_rom.inv_phi_factor[phi_probe]
                nwc_temp = (tw_temp * phi_temp) % param.MOD
                inv_tw_vec.append(nwc_temp)
            tool.bit_rev(inv_tw_vec)
            nwc_param.inv_w_rom.append(inv_tw_vec)
    if nwc_str == "DIF-RN-INNT":
        for i in range(lvl):
            tw_size = 1 << (lvl - i - 1)
            phi_probe = 1 << i
            scale = 1 << i
            inv_tw_vec = []
            for k in range(tw_size):
                tw_temp = tw_rom.inv_tw_factor[k * scale]
                # phi_temp = tw_rom.inv_phi_factor[phi_probe]
                # nwc_temp = (tw_temp * phi_temp) % param.MOD
                inv_tw_vec.append(tw_temp)
            tool.bit_rev(inv_tw_vec)
            nwc_param.inv_w_rom.append(inv_tw_vec)


def genNwcModQ(tw_rom, nwc_param, nwc_str, Q):
    (scale, tw_size, phi_probe) = (0, 0, 0)
    (tw_temp, phi_temp, nwc_temp) = (0, 0, 0)
    lvl = nwc_param.lvl
    n = tw_rom.N
    w_n = tw_rom.w_n
    phi_n = tw_rom.phi_n
    if nwc_str == "NWC-DIT-NR-NNT":
        for i in range(lvl):
            tw_size = n >> (lvl - i)
            phi_probe = n >> (i + 1)
            scale = w_n >> i
            tw_vec = []
            for j in range(tw_size):
                tw_temp = tw_rom.tw_factor[j * scale]
                phi_temp = tw_rom.phi_factor[phi_probe]
                nwc_temp = (tw_temp * phi_temp) % Q
                tw_vec.append(nwc_temp)
            tool.bit_rev(tw_vec)
            nwc_param.w_rom.append(tw_vec)
    if nwc_str == "DIT-NR-NNT":
        for i in range(lvl):
            tw_size = n >> (lvl - i)
            phi_probe = n >> (i + 1)
            scale = w_n >> i
            tw_vec = []
            for j in range(tw_size):
                tw_temp = tw_rom.tw_factor[j * scale]
                # phi_temp = tw_rom.phi_factor[phi_probe]
                # nwc_temp = (tw_temp * phi_temp) % param.MOD
                tw_vec.append(tw_temp)
            tool.bit_rev(tw_vec)
            nwc_param.w_rom.append(tw_vec)
    if nwc_str == "NWC-DIF-RN-INNT":
        for i in range(lvl):
            tw_size = 1 << (lvl - i - 1)
            phi_probe = 1 << i
            scale = 1 << i
            inv_tw_vec = []
            for k in range(tw_size):
                tw_temp = tw_rom.inv_tw_factor[k * scale]
                phi_temp = tw_rom.inv_phi_factor[phi_probe]
                nwc_temp = (tw_temp * phi_temp) % Q
                inv_tw_vec.append(nwc_temp)
            tool.bit_rev(inv_tw_vec)
            nwc_param.inv_w_rom.append(inv_tw_vec)
    if nwc_str == "DIF-RN-INNT":
        for i in range(lvl):
            tw_size = 1 << (lvl - i - 1)
            phi_probe = 1 << i
            scale = 1 << i
            inv_tw_vec = []
            for k in range(tw_size):
                tw_temp = tw_rom.inv_tw_factor[k * scale]
                # phi_temp = tw_rom.inv_phi_factor[phi_probe]
                # nwc_temp = (tw_temp * phi_temp) % param.MOD
                inv_tw_vec.append(tw_temp)
            tool.bit_rev(inv_tw_vec)
            nwc_param.inv_w_rom.append(inv_tw_vec)


def initTwParam(N, Q, NwcFlag = True):
    lvl = int(math.log2(N))
    twRom = TW_ROM(N)
    nwcParam = NWC_PARAM(lvl)
    genTwModQ(twRom, Q)
    if NwcFlag == True:
        genNwcModQ(twRom, nwcParam, "NWC-DIF-RN-INNT", Q)
        genNwcModQ(twRom, nwcParam, "NWC-DIT-NR-NNT", Q)
    else:
        genNwcModQ(twRom, nwcParam, "DIF-RN-INNT", Q)
        genNwcModQ(twRom, nwcParam, "DIT-NR-NNT", Q)
    return nwcParam





def gen_dat(f_name, nwc_param):
    tool.create_folder(f_name)
    path = "./" + f_name + "/"

    for i in range(nwc_param.lvl):
        f_str = path + "tw" + str(len(nwc_param.w_rom[i]) * 2) + ".dat"
        with open(f_str, 'w+') as fp:
            for factor in nwc_param.w_rom[i]:
                tw_str = ntt_fun.data_fix(factor, int(param.word_len / 4))
                fp.write(tw_str + "\n")
    for i in range(nwc_param.lvl):
        if_str = path + "inv_tw" + str(len(nwc_param.inv_w_rom[i]) * 2) + ".dat"
        with open(if_str, 'w+') as ifp:
            for inv_factor in nwc_param.inv_w_rom[i]:
                inv_tw_str = ntt_fun.data_fix(inv_factor, int(param.word_len / 4))
                ifp.write(inv_tw_str + "\n")


def main():
    N = int(512)
    lvl = int(math.log2(N))
    tw_rom = TW_ROM(N)
    nwc_param = NWC_PARAM(lvl)
    gen_tw(tw_rom)
    genNWC(tw_rom, nwc_param, "NWC-DIF-RN-INNT")
    genNWC(tw_rom, nwc_param, "NWC-DIT-NR-NNT")
    print("breakpoint")
    gen_dat("nwc_rom", nwc_param)


if __name__ == '__main__':
    main()
