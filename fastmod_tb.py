import pathlib as path
import random

import param
import sympy as sym
import ntt_fun
import math
import tool

def gen_gold(tb_path, test_size):
    tool.create_folder(tb_path)
    tb_name = "./" + tb_path + "/tb.dat"
    gold_name = "./" + tb_path + "/gold.dat"
    N = test_size
    fp_tb = open(tb_name, "w+")
    fp_gold = open(gold_name, "w+")
    for i in range(N):
        a = random.randint(1, param.MOD)
        b = random.randint(1, param.MOD)
        mult = a*b
        ref = mult % param.MOD
        mult_str = tool.data_fix(mult, int(2*param.word_len / 4))
        ref_str = tool.data_fix(ref, int(param.word_len / 4))
        fp_tb.write(mult_str + "\n")
        fp_gold.write(ref_str + "\n")
    fp_tb.close()
    fp_gold.close()


def main():
    test_size = 4096
    tb_path = "fast_mod80"
    gen_gold(tb_path, test_size)


if __name__ == "__main__":
    main()





