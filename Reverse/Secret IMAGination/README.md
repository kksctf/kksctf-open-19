# Secret IMAGination


**Category:** Reverse

**Points:** 995

**Description:**

Here's a minimal system image. Evil kackers know a way to IMAGine secrets, so your task is to bring them to the real world.

You may need to surround flag with kks{}

https://drive.google.com/open?id=1GeXYdPdKDx2xeWaqd9_FxitWxkwpLlGY

@servidei9707

## WriteUp 

[mlinux.iso](mlinux.iso)

We have got image of filesystem. First of all, we try to run it in VirtualBox. After start the image demands password. Enter something string:

[![enter-something.png](https://i.postimg.cc/FKdRcPrZ/enter-something.png)](https://postimg.cc/TyxfvJWL)

We received:
> Wrong password!

Then, we should to unpack image to understand the logic of application.
For example, on Debian:

`$ 7z x mlinux.iso`

And we received:

[![ll-of-iso.png](https://i.postimg.cc/tCQMH7nC/ll-of-iso.png)](https://postimg.cc/w32VXqkS)

We are interested in ```kernel.gz``` and ```rootfs.gz```.
Unpack them:

+ ```kernel.gz``` use binwalk: `$ binwalk --extract kernel.gz`

The result will be one file ```43B1``` - ELF 64-bit, statically linked, stripped.

+  ```rootfs.gz``` is simple: `$ gunzip rootfs.gz`. The outcome file ```rootfs``` - ASCII cpio archive (SVR4 with no CRC). To get ```init``` we again make use of binwalk:

`$ binwalk --extract rootfs`. And got:

[![rootfs.png](https://i.postimg.cc/bw3GhDJ7/rootfs.png)](https://postimg.cc/SnYQLKcd)

After reading ```init``` we see ```/bin/task```.

Let`s begin reverse ```task``` - ELF 64-bit, statically linked, not stripped.

[![main-task.png](https://i.postimg.cc/Dy7wNnhJ/main-task.png)](https://postimg.cc/py1vhNpR)

In main function we can see, that program get from stdin 20 symbols and open file descriptor ```/pass``` to write our string, which we input. Then syscall is called.

[![syscall.png](https://i.postimg.cc/1zmTx7tK/syscall.png)](https://postimg.cc/VJh4nRXS)

As you can see, program calls custom syscall with id 1337.

Then we should reverse ```43B1``` . 
In ```task``` is called path ```/pass```. Try to find it in ```43B1```.
After call ```kernel_path``` proceed to the next call function. We see string ```md5```, suppose, that function generate md5 from our input string.
The next function is called with 3 parameters: 
+ edx - 16;
+ rsi   -  md5 from our input string;
+ rdi   - string, which is located in .rodata;

Reverse this function, we have found out, that it has compared two strings.

[![kernel-check.png](https://i.postimg.cc/J46FZ546/kernel-check.png)](https://postimg.cc/mt9VGM9C)

Therefore, string, which is located in .rodata - md5 from true password.

[![true-md5.png](https://i.postimg.cc/HLn3HrGr/true-md5.png)](https://postimg.cc/PLG1Qr5H)

Take advantage of <https://hashkiller.co.uk/Cracker> to decode hash.
We got `diviz_)(159$=*@`. Try to enter this string - you receive flag.

flag: `kks{Y0u_d0n7_n33D_70_p47ch_k3rn3l_by_y0r53lf}`
