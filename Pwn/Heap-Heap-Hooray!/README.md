# Heap-Heap-Hooray!


**Category:** Pwn

**Points:** 988

**Description:**

<img src="https://i.imgur.com/9oagyn3.png" width="100%">

P.S. glibc2.27 is the greatest version of glibc!

`nc tasks.open.kksctf.ru 10000`

lib: https://drive.google.com/open?id=1cpyWT_cRu2szV2u4lpp5ESgMMXUP3IMu  
heap: https://drive.google.com/open?id=1Cnx-VBufgdowFXvE7iIPc6mBZRbnZc7W  
df: https://drive.google.com/open?id=1TRfyx8-5DZrQ70ah8eKLTCbxFT4vBAWj

@oldwayfarer

## WriteUp 

### Main idea
The main idea is to get control over chunks controlling structure (witch represented with a bit map) via exploiting format string vulnerability and then perform a double free atack twice to execute shellcode

On the first double free, we put shell code with `\bin\sh` on `bss` section (Array with 32 chunk addresses is located there, so we have more then enough place for shellcode).
On the second double free, we rewrite the GOT entry for `exit()` function with the address of shellcode. And then calling exit to get shell

### Exploitation
Step 1, Exploit double free to get able to write shellcode into bss. bss address can be obtained from binary. Use after free is possible becouse it said that glibc 2.27 is used and in this version a tcatch is already exists and have not got any protection mechanisms included by default. We will use following function to perform the double free atack:

	def exploit_double_free(c, payload, address, chunk_size, final_chunk):
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
	#!/usr/bin/env python2

What hapening here. First of all allocating 2 chunks of the same size and then `free()` them. Then exploiting format string bug in "list chunk" option, get control over chunks control structure to be able perform double free and finaly getting to double free and writing payload to given address. For the first step: payload is our shell code, address - is a bss adress, chunk_size must be big enough to fit payload.

step 2, Explot double free again to rewrite GOT entry of `exit()` to shellcode. This time payload wold be an address of the shellcode, address - GOT entry for `exit()`, chunk_size should differ by 16, becouse corresponding tcache entry for previouse buffer size has already been poisoned, so we can not use it any longer. 

step 3, simply call `exit()` and get shell. 

flag: `kks{w311_m4y_b3_in_@_c0upl3_m0r3_pl4c35}`

Example: [break.py](break.py)
