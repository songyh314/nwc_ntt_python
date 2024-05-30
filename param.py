import sympy as sym

MOD = 65537

g = sym.primitive_root(MOD)
word_len = 20
print(MOD,g)