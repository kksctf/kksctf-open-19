#!/usr/bin/env python3

import sys


message = sys.argv[1] if len(sys.argv) > 1 else "2bi4j2fcjli84edk07kbjj3cggg3k5ih0hcgg710260lak1ibead1gf15hflb5f41"

print(f"Unique letters: {len(set(message))}")

for letter in sorted(list(set(message))):
    print(f"{letter}: {message.count(letter)}") 
