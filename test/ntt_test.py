import pytest

import nwc_ntt
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
    navRes = tool.naiveConvModQ(a, b, 8)
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


@pytest.mark.ParamterTest
def test_param():
    N = 512
    Q = 12289
    nwcParam12289 = nwc_tw.initTwParam(N, Q)
    print("fin")


@pytest.mark.NwcPolyMulTest
def test_NwcPolyMul():
    N = 512
    Q24 = 2**24 - 2**14 + 1
    Q14 = 2**14 - 2**12 + 1
    intgerMod8 = 1 << 8
    intgerMod2 = 1 << 2
    NwcParam24 = nwc_tw.initTwParam(N, Q24)
    NwcParam14 = nwc_tw.initTwParam(N, Q14)
    a = list(0 for _ in range(N))
    b = list(0 for _ in range(N))
    for i in range(N):
        (a[i], b[i]) = (1, 1)
    mulRes24 = nwc_ntt.NwcPolyMul(a, b, Q24, NwcParam24, intgerMod8)
    mulRes14 = nwc_ntt.NwcPolyMul(a, b, Q14, NwcParam14, intgerMod2)
    print()
    print(mulRes24)
    print(mulRes14)


@pytest.mark.PolyMul
def test_poly_mul():
    N = 512
    Q = 2**64 - 2**32 + 1
    intgerMod = 32
    NwcParam = nwc_tw.initTwParam(N, Q)
    a = list(0 for _ in range(N))
    b = list(0 for _ in range(N))
    for i in range(N):
        (a[i], b[i]) = (1, 1)
    mulRes14 = nwc_ntt.NwcPolyMul(a, b, Q, NwcParam, intgerMod)
    print()
    print(mulRes14)


@pytest.mark.PolyMul12289
def test_poly_mul_12289():
    N = 256
    Q = 12289
    intgerMod = 3
    NwcParam = nwc_tw.initTwParam(N, Q)
    a = list(0 for _ in range(N))
    b = list(0 for _ in range(N))
    for i in range(N):
        (a[i], b[i]) = (1, 1)
    mulRes14 = nwc_ntt.NwcPolyMul(a, b, Q, NwcParam, intgerMod)
    navRes = tool.naiveConvModQ(a, b, 3)
    print()
    print(mulRes14)
    print(navRes)
