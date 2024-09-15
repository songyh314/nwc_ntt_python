import pytest
from nwc_ntt import applyNttSignedInput, applyInttSignedOutput
import nwc_tw
import ntt_fun
import tool
import math
import param
from param import MOD,HalfMod,PolyMax

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
    print(inttRes)