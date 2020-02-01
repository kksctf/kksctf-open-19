# Xmas Tree 2


**Category:** Reverse

**Points:** 100

**Description:**

Looks like another kackers's intrusion artifact. Find password for this program and it'll tell you its secrets.

@anfinogenov

## WriteUp 

[Task](task_tree.c)

It's absolutely valid C code, and we can compile it. But for any input strings (through command-line arguments) program simply returns 0 and closes.

Let's do a quick refactoring: do the "preprocessor" stage.

```sh
$ gcc -E task_tree.c >> preprocessed.txt
```

Compiler `gcc` will process all "defines" and "includes" to [preprocessed.txt](preprocessed.txt).

Then we can "beautify" the tree to understand the structure of program's checks. I used [format.krzaq.cc](format.krzaq.cc) online beautifier.

Here is what we [get](beautified.c):
```c
void

p(char* a,
    int i)
{
  printf("%c", a[i]);
}
int main

    (int i, char** c) {
  char _1[19] =
      "_a"
      "cd"
      "eh"
      "ik"
      "lm"
      "no"
      "pr"
      "su"
      "wy"
      "\0";
  if (i < 2) return 1;
  int _2 = atoi(c[1]);
  if (((unsigned char*)&_2)[0] == 0xAF) {
    if (((short*)&_2)[1] == 0x3174) {
      if (((_2 >> 22) & 0xFF) == 0xC5) {
        if (*(((char*)((&_2) + 2)) - 7) == 0x19) {
          if (((((short*)(((char*)(&_2)) + 13) - 5)[0] >> 0) & 0xff) == 0x31) {
            printf("kks{");
            p(_1, 2);
            p(_1, _2 >> 24 & 0xFF00);
            p(_1, ((_2 & 1) << 2) | 2);
            p(_1, ((_2 >> 24) & 0xF) * 10 + ((_2 >> 16) & 0xF));
            p(_1, _2 >> 31);
            p(_1, ((char*)&_2)[1] - 11);
            p(_1, 6);
            p(_1, (_2 + 10) & 0x0000000f);
            p(_1, 014);
            p(_1, i << 2);
            p(_1, i << 2 >> 1);
            p(_1, 000 * 003);
            p(_1, "P"[0] - 69);
            p(_1, (_2 >> 4) % 16);
            p(_1, 2147483648l >> 28);
            p(_1, (*(unsigned char*)&_2) - 0x9e);
            p(_1, 000);
            int n = 2 << 5, m = 5;
            while ((m < 11) && (n >>= 2)) {
              p(_1, n);
              p(_1, m);
              m *= 2;
            }
            p(_1, '_' - '_');
            printf("%c", 0x76 + (_2 >> 28));
            p(_1, 10 + ((_2 >> 24) & 0xf));
            p(_1, *(((char*)&_2) + 3) % 16 + 14);
            p(_1, 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 - 45);
            p(_1, (printf("%s", "") + 1) % 16), p(_1, 13),
                p(_1, ((char*)(&_2))[2] % 16), printf("_");
            p(_1, 5 - 02);
            p(_1, 0x4 - (-9));
            p(_1, 003 - (-12));
            p(_1, 2 - (-010));
            printf("%c", _1[7]);
            printf("}\n");
          }
        }
      }
    }
  }
  return 0;
}
```

It's easy to see progrom logic there:
1. Check for `argc` (`i`), if it's less than 2, then return 1
2. Get integer from `argv[1]` (`atoi(c[1])`)
3. Perform some magic checks (lines 27-31 of [beautified.c](beautified.c))
4. Decrypt and print flag (since it starts from `kks{` and ends with `}`).

Let's reverse this check.

---
## Magic check of `_2` variable (`argv[1]`)
```c
((unsigned char*)&_2)[0] == 0xAF
```
1. Get address of `_2`
2. Convert pointer to `unsigned char *` type (`uint8_t`)
3. Dereference 0-th byte of bytearray `(unsigned char*)&_2` 
4. Compare it with `0xAF`

In short, first `if` checks for `0xAF` in 0-th byte of `DWORD  _2`, and, since we are working with little-endian numbers, we can rewrite this check as:
```c
_2 & 0xFF == 0xAF
```

At this moment we know that `_2 == 0x??????AF`

OK, next.
```c
((short*)&_2)[1] == 0x3174
```
1. Get address of `_2`
2. Convert pointer to `short *` type (`int16_t`)
3. Dereference 1-th word of array `(short*)&_2`
4. Compare it with `0x3174`

It can be rewritten as:
```c
_2 >> 16 == 0x3174
```

At this moment we know that `_2 == 0x3174??AF`

OK, next.

```c
((_2 >> 22) & 0xFF) == 0xC5
```
1. Shift `_2` to the right on 22 bits
2. Get last 8 bits
3. Compare with `0xC5`

It can be rewritten as:
```c
_2 & 0x3fc00000 == 0x31400000
```

But at this moment we already know first 16 bits (`0x3174`) of `_2`, so this check gives no valuable info. Let's go to the final one.

```c
*(((char*)((&_2) + 2)) - 7) == 0x19
```

Complex one.
1. Get address of `_2`
2. Add to this pointer `2`, so, in terms of bytes, shift to the right on `8 == (2*sizeof(int))` bytes
3. Convert this shifted pointer to `char*` pointer, or `int8_t*`
4. Subtract `7` from this pointer (1st byte of `_2`)
5. Dereference pointer and compare with `0x19`

It can be rewritten as:
```c
(_2 >> 8) & 0xFF == 0x19
```

After all of this checks `_2` can only be one number:  
```
_2 == 0x317419AF
```
or `829692335`

Let's try this number as input for program.

```sh
$ gcc task_tree.c -o task && ./task 829692335
kks{c_is_simple_only_when_you_are_drunk}
```

Here is our flag: `kks{c_is_simple_only_when_you_are_drunk}`