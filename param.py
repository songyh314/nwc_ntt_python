import sympy as sym

MOD = 2 ** 24 - 2 ** 14 + 1
HalfMod = (MOD + 1) >> 1
PolyMax = 1 << 7
IntMAX = (1 << 31) - 1
IntMIN = -(1 << 31)
g = sym.primitive_root(MOD)
# g = 1925

word_len = 24
print(MOD, g)
