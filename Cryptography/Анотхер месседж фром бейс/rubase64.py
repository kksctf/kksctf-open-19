#!/usr/bin/env python3


import sys
import base64


alphabet_eng = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
alphabet_rus = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩабвгдежзийклмнопрстуфхцчшщ0123456789+/"


def base64encode(input_bytes: bytes) -> str:
    original_encode = base64.b64encode(input_bytes).decode()
    for i, j in zip(alphabet_rus, alphabet_eng):
        original_encode = original_encode.replace(j, i)
    return original_encode


def base64decode(s: str) -> bytes:
    for i, j in zip(alphabet_eng, alphabet_rus):
        s = s.replace(j, i)
    return base64.b64decode(s.encode())


def main():
    print(base64encode(b"this is a secret message from kackers:\nWe are discovered, new base access password is kks{custom_b64_alphabet_c4nt_$t0p_y0u}"))


if __name__ == "__main__":
    main()

