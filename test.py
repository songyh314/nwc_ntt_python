import sympy as sym
import param


def find_sol_prime(L, H):
    for i in range(L, H + 1):
        for j in range(int(L >> 1), H):
            p = 2 ** i - 2 ** j + 1
            if sym.isprime(p):
                print(i, j, p)


def main():
    p = 65537
    print(sym.primitive_root(p))
    a = 255
    b = 65280
    tw = 256
    add = addsacle(a,b)
    sub = subsacle(a,b)
    mu = (sub*tw)%param.MOD
    print("a = ",a," b = ",b," tw = ",tw)
    print("add = ", add)
    print("sub = ", sub)
    print("mult = ", mu)


def addsacle(a, b):
    c = (a + b) % param.MOD
    if c % 2 == 0:
        c = c >> 1
    else:
        c = (c >> 1) + ((param.MOD + 1) >> 1)
    return c


def subsacle(a, b):
    c = (a - b) % param.MOD
    if c % 2 == 0:
        c = c >> 1
    else:
        c = (c >> 1) + ((param.MOD + 1) >> 1)
    return c


if __name__ == '__main__':
    main()
