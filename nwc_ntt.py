import random

import nwc_tw
import ntt_fun
import tool
import math
import param
import numpy as np


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
                if (temp_add%2 == 0):
                    temp_add = temp_add >> 1
                else:
                    temp_add = (temp_add >> 1) + ((param.MOD + 1)>>1)

                if (temp_sub % 2 == 0):
                    temp_sub = temp_sub >> 1
                else:
                    temp_sub = (temp_sub >> 1) + ((param.MOD + 1) >> 1)
                temp_mu = (temp_sub * tw_fac) % param.MOD
                dif_res[posa] = temp_add
                dif_res[posb] = temp_mu
    return dif_res


def main():
    N = 8
    lvl = int(math.log2(N))
    tw_rom = nwc_tw.TW_ROM(N)
    nwc_param = nwc_tw.NWC_PARAM(lvl)
    nwc_tw.gen_tw(tw_rom)
    nwc_tw.genNWC(tw_rom, nwc_param, "NWC-DIF-RN-INNT")
    nwc_tw.genNWC(tw_rom, nwc_param, "NWC-DIT-NR-NNT")
    a = list(range(N))
    for i in range(N):
        a[i] = 65536


    ntt_res = dit_nr(a, nwc_param.w_rom, N)
    intt_res = dif_rn(ntt_res, nwc_param.inv_w_rom, N)
    print(a)
    print("ntt:",ntt_res)
    print(intt_res)
    for i in range(N):
        if a[i] != int(intt_res[i]):
            print("error at %d", i)
            print("a = ", a[i]," res = ",intt_res[i])



if __name__ == '__main__':
    main()
