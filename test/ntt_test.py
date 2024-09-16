import pytest
from nwc_ntt import applyNttSignedInput, applyInttSignedOutput
import nwc_tw
import ntt_fun
import tool
import math
import param
from param import MOD, HalfMod, PolyMax


@pytest.mark.NttInttTest
def test_ntt_intt():
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
    assert a == inttRes
    print()
    print(inttRes)


@pytest.mark.ConvTest
def test_conv():
    N = 512
    lvl = int(math.log2(N))
    tw_rom = nwc_tw.TW_ROM(N)
    nwc_param = nwc_tw.NWC_PARAM(lvl)
    nwc_tw.gen_tw(tw_rom)
    nwc_tw.genNWC(tw_rom, nwc_param, "NWC-DIF-RN-INNT")
    nwc_tw.genNWC(tw_rom, nwc_param, "NWC-DIT-NR-NNT")
    a = list(0 for _ in range(N))
    b = list(0 for _ in range(N))
    for i in range(N):
        a[i] = 1
        b[i] = 1
    NttRes1 = applyNttSignedInput(a, nwc_param.w_rom, N)
    NttRes2 = applyNttSignedInput(b, nwc_param.w_rom, N)
    mulRes = list(0 for _ in range(N))
    for i in range(N):
        mulRes[i] = (NttRes1[i] * NttRes2[i]) % MOD
    InttRes = applyInttSignedOutput(mulRes, nwc_param.inv_w_rom, N)
    navRes = tool.naiveConvModQ(a, b, 1 << 7)
    # assert mulRes == navRes
    print()
    print("InttRes:", InttRes)
    print("navRes:", navRes)


@pytest.mark.bitslice
def test_bit_slice():
    a = -254
    print()
    print(bin(abs(a)))
    print(tool.genBinComplement(a, 16))
    print(tool.getLowBits(a, 8))
