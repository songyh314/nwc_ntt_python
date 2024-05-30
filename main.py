# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import ntt_fun
import sympy as sym
import pathlib as path

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # folder_name = "test"
    # folder_path = path.Path(folder_name)
    # folder_path.mkdir()
    # ntt_fun.gen_tw(32, 20, 32, 1024)
    mod = 2**32 - 2**20 + 1
    print(mod)
    g = sym.primitive_root(mod)
    print(sym.primitive_root(mod))
    x = 0xfdb9ded3
    print(x)
    pow(g, int((mod-1)/4),mod)
    # print(int((4293918721*4293918719))%mod)
    a = 4256816851
    b = 4293918719
    c = 74203740
    print((a*b)%mod)
    print((b+c)%mod)
    print(b-c)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
