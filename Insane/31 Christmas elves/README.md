# 31 Christmas elves


**Category:** Insane

**Points:** 1000

**Description:**

33 Christmas elves from _kackers group_ have played nasty trick with this executable and stored their secret in it. We know that these elves like stego and addition modulo 2, and don't like brute force. Can you get the flag?

https://drive.google.com/open?id=1OKnC5T1mDd3aYlFdxPdheGOyIemosFkP

@servidei9707

## WriteUp 

### Solution:
We have a difference in task name and description, and a statically linked x64 executable. Executable prints a string and waits for a password. If we try to give something to it, the answer will be `Wrong password length!`. It accepts only password with length 69 and then prints some escaped data.

If we open it with with hteditor we will see whole libc. Function `main()` looks secure, with scanf for input. Also there is some data called 'flag', some printable string with control characters.Seems like it is flag xored with some string (password?), but description says there are no bruteforce needed. If this is steganography task, there must be some data hidden in another place.

Let's look at main(). In edit mode we can see that xor eax,eax at the beginning of main() has two different opcodes, `31c0` and `33c0`. And description and task name contains same values!

If we google for it, we can find some [link](https://stackoverflow.com/questions/50336269/x86-xor-opcode-differences) that says there are really two different opcodes.

So we need to find all `31c0` and `33c0` and decode it, maybe as bits. And there can be xors for another registers.

Next problem: data in sections other than .text can contain this sequences too, and changing it can crash the program. So changes should be done only in section .text, and our decoder should find it (or it can be done manually, with hteditor).

Hteditor can show soction offset, currently it is `0x10f0` and size `0x9af80`. So if we get this data and parse all `31c0` and `33c0` opcodes, we should get correct text.

`xor ecx,ecx` in main has opcode `33c9`, but compiler generates only `31c9`, so not only `xor eax,eax` used.
If we try to decode only two found opcodes, we get some binary data, exactly not ascii.
But if we try four registers -- eax, ebx, ecx, edx, we will get text:
```password:
*^_S0m3_L0n9_p4S5w0rd_w17h_$ym&0l5_7h4t_c0n741n5_m4ny_num&3r5_192=_*@

Now go and get the flag!

```
Program asks password so let's do it. And here is output:
`5.. 4.. 3.. 2.. 1.. Your flag: kks{d0_y0u_l1k3_57360_1n_3x3cu74bl3s?}`

### Solver (with finding .text section):
[solver.py](solver.py)
