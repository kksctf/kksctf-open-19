# kacker Bob and kacker Alice


**Category:** Cryptography

**Points:** 100

**Description:**

```
n = 208644129891836890527171768061301730329

c1 = 173743301171240370198046699578309731314
c2 = 18997024455485040483743919351219518166
c3 = 49337945995780286416188917529635194536
```

@anfinogenov

## WriteUp 

Bob and Alice in task's name should help to figure out that this task is a crypto task.

`c, n` are usually used as `ciphertext` and `modulus` in RSA, but where is `e` (open exponent)? Since all `c`'s are smaller than `n`, that's another indicator of RSA scheme. We can go further and try to factor `n`. 

For further solution see comments in [solve.py](solve.py).

> Funny fact: there was another line in task, "`e = 65537`" above the "`n = ...`" line, but it was missed, when task was copied to CTFd. But task is still solveable, so `¯\_(ツ)_/¯`
