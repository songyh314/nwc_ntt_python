import random

import nwc_tw
import ntt_fun
import tool
import math
import param
from param import MOD, HalfMod, PolyMax
import numpy as np
from scipy.signal import convolve


def dit_nr(dit_in, tw, N):
    dit_res = dit_in.copy()
    lvl = int(math.log2(N))
    gap = 0
    block = 0
    block_size = 0
    tw_index = 0
    for i in range(lvl):
        block = N >> (lvl - i)
        block_size = N >> i
        gap = block_size >> 1
        for j in range(block):
            tw_index = j
            for k in range(gap):
                posa = j * block_size + k
                posb = j * block_size + k + gap
                tw_fac = tw[i][tw_index]
                temp_mult = int(tw_fac * dit_res[posb]) % param.MOD
                temp_add = (dit_res[posa] + temp_mult) % param.MOD
                temp_sub = (dit_res[posa] - temp_mult) % param.MOD
                dit_res[posa] = temp_add
                dit_res[posb] = temp_sub
    return dit_res


def DitNrModQ(dit_in, tw, N, Q):
    dit_res = dit_in.copy()
    lvl = int(math.log2(N))
    gap = 0
    block = 0
    block_size = 0
    tw_index = 0
    for i in range(lvl):
        block = N >> (lvl - i)
        block_size = N >> i
        gap = block_size >> 1
        for j in range(block):
            tw_index = j
            for k in range(gap):
                posa = j * block_size + k
                posb = j * block_size + k + gap
                tw_fac = tw[i][tw_index]
                temp_mult = int(tw_fac * dit_res[posb]) % Q
                temp_add = (dit_res[posa] + temp_mult) % Q
                temp_sub = (dit_res[posa] - temp_mult) % Q
                dit_res[posa] = temp_add
                dit_res[posb] = temp_sub
    return dit_res


def dif_rn(dif_in, tw, N):
    lvl = int(math.log2(N))
    gap = 0
    block = 0
    block_size = 0
    tw_index = 0
    dif_res = dif_in.copy()
    for i in range(lvl):
        block = N >> (i + 1)
        block_size = 1 << (i + 1)
        gap = 1 << i
        for j in range(block):
            tw_index = j
            for k in range(gap):
                posa = j * block_size + k
                posb = j * block_size + k + gap
                tw_fac = tw[i][tw_index]
                temp_add = (dif_res[posa] + dif_res[posb]) % param.MOD
                temp_sub = (dif_res[posa] - dif_res[posb]) % param.MOD
                if (temp_add % 2 == 0):
                    temp_add = temp_add >> 1
                else:
                    temp_add = (temp_add >> 1) + ((param.MOD + 1) >> 1)

                if (temp_sub % 2 == 0):
                    temp_sub = temp_sub >> 1
                else:
                    temp_sub = (temp_sub >> 1) + ((param.MOD + 1) >> 1)
                temp_mu = (temp_sub * tw_fac) % param.MOD
                dif_res[posa] = temp_add
                dif_res[posb] = temp_mu
    return dif_res


def DifRnModQ(dif_in, tw, N, Q):
    lvl = int(math.log2(N))
    gap = 0
    block = 0
    block_size = 0
    tw_index = 0
    dif_res = dif_in.copy()
    for i in range(lvl):
        block = N >> (i + 1)
        block_size = 1 << (i + 1)
        gap = 1 << i
        for j in range(block):
            tw_index = j
            for k in range(gap):
                posa = j * block_size + k
                posb = j * block_size + k + gap
                tw_fac = tw[i][tw_index]
                temp_add = (dif_res[posa] + dif_res[posb]) % Q
                temp_sub = (dif_res[posa] - dif_res[posb]) % Q
                if (temp_add % 2 == 0):
                    temp_add = temp_add >> 1
                else:
                    temp_add = (temp_add >> 1) + ((Q + 1) >> 1)

                if (temp_sub % 2 == 0):
                    temp_sub = temp_sub >> 1
                else:
                    temp_sub = (temp_sub >> 1) + ((Q + 1) >> 1)
                temp_mu = (temp_sub * tw_fac) % Q
                dif_res[posa] = temp_add
                dif_res[posb] = temp_mu
    return dif_res


def NcConv(a, b, nwc_param):
    N = len(a)
    N2 = len(b)
    assert N == N2, "input array should be same in length"
    NttRes1 = dit_nr(a, nwc_param.w_rom, N)
    NttRes2 = dit_nr(b, nwc_param.w_rom, N)
    MulRes = list(0 for _ in range(N))
    for i in range(N):
        MulRes[i] = (NttRes1[i] * NttRes2[i]) % param.MOD
    InttRes = dif_rn(MulRes, nwc_param.inv_w_rom, N)
    for i in range(N):
        if InttRes[i] > (param.MOD - 1) >> 1:
            InttRes[i] -= param.MOD
    return InttRes


def applyNttSignedInput(SignedIn, tw, N):
    UnsignedIn = list(0 for _ in range(N))
    for i in range(N):
        if SignedIn[i] < 0:
            UnsignedIn[i] = SignedIn[i] + MOD
        else:
            UnsignedIn[i] = SignedIn[i]
    # NttRes = list(0 for _ in range(N))
    NttRes = dit_nr(UnsignedIn, tw, N)
    return NttRes


def applyNttSignedInputModQ(SignedIn, tw, N, Q):
    UnsignedIn = list(0 for _ in range(N))
    for i in range(N):
        if SignedIn[i] < 0:
            UnsignedIn[i] = SignedIn[i] + MOD
        else:
            UnsignedIn[i] = SignedIn[i]
    # NttRes = list(0 for _ in range(N))
    NttRes = DitNrModQ(UnsignedIn, tw, N, Q)
    return NttRes


def applyInttSignedOutput(UnsignedIn, tw, N):
    InttRes = dif_rn(UnsignedIn, tw, N)
    SignedInttRes = list(0 for _ in range(N))
    res = list(0 for _ in range(N))
    for i in range(N):
        flag = 0
        if InttRes[i] >= HalfMod:
            SignedInttRes[i] = InttRes[i] - MOD
        else:
            SignedInttRes[i] = InttRes[i]
        flag = (SignedInttRes[i] < 0)
        tmp = tool.getLowBits(SignedInttRes[i], 8)
        if tmp >= PolyMax:
            res[i] = tmp - (PolyMax << 1)
        else:
            res[i] = tmp
    return res


def applyInttSignedOutputModQP(UnsignedIn, tw, N, Q, P):
    InttRes = DifRnModQ(UnsignedIn, tw, N, Q)
    SignedInttRes = list(0 for _ in range(N))
    res = list(0 for _ in range(N))
    halfMod = (Q + 1) >> 1
    for i in range(N):
        if InttRes[i] >= halfMod:
            SignedInttRes[i] = InttRes[i] - Q
        else:
            SignedInttRes[i] = InttRes[i]
        tmp = tool.getLowBits(SignedInttRes[i], P)
        if tmp >= (1 << (P - 1)):
            res[i] = tmp - (1 << P)
        else:
            res[i] = tmp
    return res


def NwcPolyMul(a, b, Q, NwcParam, intger_mod):
    N = len(a)
    N_b = len(b)
    if N != N_b:
        raise ValueError("wrong poly len")
    NttResA = applyNttSignedInputModQ(a, NwcParam.w_rom, N, Q)
    NttResB = applyNttSignedInputModQ(b, NwcParam.w_rom, N, Q)
    tmp = list(0 for _ in range(N))
    for i in range(N):
        tmp[i] = (NttResA[i] * NttResB[i]) % Q
    InttRes = applyInttSignedOutputModQP(tmp, NwcParam.inv_w_rom, N, Q, intger_mod)
    return InttRes


def NttInttTest():
    N = 512
    lvl = int(math.log2(N))
    tw_rom = nwc_tw.TW_ROM(N)
    nwc_param = nwc_tw.NWC_PARAM(lvl)
    nwc_tw.gen_tw(tw_rom)
    nwc_tw.genNWC(tw_rom, nwc_param, "NWC-DIF-RN-INNT")
    nwc_tw.genNWC(tw_rom, nwc_param, "NWC-DIT-NR-NNT")
    a = list(0 for _ in range(N))
    for i in range(N):
        a[i] = -1
    nttRes = applyNttSignedInput(a, nwc_param.w_rom, N)
    inttRes = applyInttSignedOutput(nttRes, nwc_param.inv_w_rom, N)
    print(inttRes)
