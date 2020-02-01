#!/usr/bin/env python3


import binascii
flag = "kks{do_y0u_know_h0w_3nc0d1ng_w0rk$?}"
alphabet = "0123456789abcdefghijkl"
BASE = 22
assert BASE == len(alphabet)

def main():
    flag_as_int = int(binascii.hexlify(flag.encode()), 16)
    to_base = []
    while flag_as_int > 0:
        to_base.insert(0, alphabet[flag_as_int % BASE])
        flag_as_int //= BASE
    return "".join(to_base)


def solve(a):
    out = 0
    for i in a:
        out *= 22
        out += alphabet.find(i)
    return binascii.unhexlify(hex(out)[2:].encode())


if __name__ == "__main__":
    encoded_flag = main()
    print(solve(encoded_flag))
