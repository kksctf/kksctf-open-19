#!/usr/bin/env python3

import binascii
import gmpy2

n = 208644129891836890527171768061301730329

c1 = 173743301171240370198046699578309731314
c2 = 18997024455485040483743919351219518166
c3 = 49337945995780286416188917529635194536

#from sympy.ntheory import factorint
#p, q = factorint(n).keys() # slow, but works

p, q = (13037609104445998727, 16003250919732396127)     # factorization from factordb (fast)

assert p*q == n

# since we don't know public exponent e, let's try all numbers
for e in range(2, 100000):
    try:
        d = gmpy2.invert(e, (p-1)*(q-1))                # there can be no inversion, so exception is thrown
        m1 = pow(c1, d, n)                              # that's how mafia works
        m1_text = binascii.unhexlify(hex(m1)[2:])
        if "kks" in m1_text.decode():                   # invalid text will throw decode error
            print(f"found e: {e}, text: {m1_text}")
            # we found e, and corresponding d, so we can decrypt c2 and c3
            break
    except:
        pass

m2, m3 = pow(c2, d, n), pow(c3, d, n)

ms = [m1, m2, m3]
for m in ms:
    print(binascii.unhexlify(hex(m)[2:]).decode(), end="")
print()

