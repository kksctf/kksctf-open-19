# Red XOXOXO


**Category:** Cryptography

**Points:** 100

**Description:**

And another message captured: `-*;91~.,1*1=12~;-*?<27-6;:r~+-;~=27;0*~*1~=100;=*p~7y3~)?7*709~81,~+,~,;.2'p~55-%?**j=5.?*.:j)0#`

@anfinogenov

## WriteUp 

If we'll look at task's name closely, we'll probably notice parts "Red" and "Xo", which could be hint for task. 

There is an encryption method, using `xor` operation, and ciphertext respectively named `xored` after this encryption.

Using this assumption, let's try to xor this text on every single-byte sequences (from 0 to 255).

[Brute xor key with CyberChef](https://gchq.github.io/CyberChef/#recipe=XOR_Brute_Force(1,100,0,'Standard',false,true,false,'')&input=LSo7OTF%2BLiwxKjE9MTJ%2BOy0qPzwyNy02OzpyfistO349Mjc7MCp%2BKjF%2BPTEwMDs9KnB%2BN3kzfik/Nyo3MDl%2BODEsfissfiw7LjIncH41NS0lPyoqaj01Lj8qLjpqKTAj)

After searching for `kks` substring or after careful reading, we'll find correct `key = 0x5e`, and flag is `kks{attackpatpdawn}`

[Solve with CyberChef](https://gchq.github.io/CyberChef/#recipe=XOR(%7B'option':'Hex','string':'5e'%7D,'Standard',false)&input=LSo7OTF%2BLiwxKjE9MTJ%2BOy0qPzwyNy02OzpyfistO349Mjc7MCp%2BKjF%2BPTEwMDs9KnB%2BN3kzfik/Nyo3MDl%2BODEsfissfiw7LjIncH41NS0lPyoqaj01Lj8qLjpqKTAj)
