# Message from base


**Category:** Cryptography

**Points:** 365

**Description:**

We captured some weird messages from _kackers group_ bots. We are not 100% sure this is encrypted, but we still can't read or decode the message. Help us!

`2bi4j2fcjli84edk07kbjj3cggg3k5ih0hcgg710260lak1ibead1gf15hflb5f41`

@anfinogenov

## WriteUp 

Message from `base`. That's the first hint. Text looks like base32/base64-encoded text.

`We are not sure this is encrypted, but we still can't decode` is the second hint. baseN encodings don't __encrypt__ text, but __encodes__ it

> I am a CTF player and I'll simply put this string to baseX solver. What? It does not work?? ~~WTF!~~

What we know about "base" encodings? [Here](http://core.ecu.edu/csci/wirthj/Basen/basen-c.html) is a good article about base-N encodings, such as `base2` (also known as binary), `base3`, `base8` (octal), `base10` (decimal), `base16` (hexadecimal) and so on.

Let's analyse the message with simple [script](analyser.py) (or by bare hands).

Here is what we see:
```
Unique letters: 21
0: 4
1: 5
2: 3
3: 2
4: 3
5: 3
6: 1
7: 2
8: 1
a: 2
b: 4
c: 3
d: 2
e: 2
f: 4
g: 6
h: 3
i: 4
j: 4
k: 4
l: 3
```

From [here](http://core.ecu.edu/csci/wirthj/Basen/basen-c.html) we know, that `base-N` (N > 10) alphabets consists of:  
1. `0-9` digits
2. `a-z` letters or `A-Z` letters
3. `A-Z` letters or `a-z` letters
4. other printables

And we only need to take `N-10` first letters, since there are 10 digits in alphabet by default. 

What we see in [script](analyser.py) output? At least, that's base21 (since there are 21 unique letters). But there is no `9` digit in encoded text. What does it mean? 

Short example:  
- `1101` is a valid `base2` encoded decimal number = 13
- `1101` is a valid `base3` encoded decimal number = 37, but there is no `2` in encoded text

This way, we'll not necessarily have the whole alphabet in encoded text. So it can be any `base` from `22` to `85` (highest printable base)

Decoding with base22 gives us flag: `kks{do_y0u_know_h0w_3nc0d1ng_w0rk$?}`

[Solve with task.py](task.py)  
[Solve with CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Base(22)To_Base(16)From_Hex('Auto')&input=MmJpNGoyZmNqbGk4NGVkazA3a2JqajNjZ2dnM2s1aWgwaGNnZzcxMDI2MGxhazFpYmVhZDFnZjE1aGZsYjVmNDE)
