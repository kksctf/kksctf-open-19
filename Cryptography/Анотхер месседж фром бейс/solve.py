#!/usr/bin/env python3

import base64
import sys


def solve(text: str) -> str:
    translated = ""
    for i in text:
        if i.isdigit() or i in ['+', '/', '=']:
            translated += i
        else:
            translated += chr(ord('A') + ord(i) - ord('А')) # Second A is cyrillic
    return base64.b64decode(translated).decode()


if __name__ == "__main__":
    print(solve(sys.argv[1])) if len(sys.argv) > 1 else None
