# Анотхер месседж фром бейс


**Category:** Cryptography

**Points:** 698

**Description:**

New intercepted message: `гЖзпвшБпвшБзИЗНлШ3ЙлгВБуЩЧНщШЦглИЖЩшб20жа2Ейа2ХшвщоКХ2ФжШЧЙлИЖСпв2НхгмХшЩЦРтИЖ5лгшБиШЧНлИЖЕйШ2ХщвшБцШЧНщг29шЩВБпвшБса3Н7Ш3ХщгЖ9уЧ2И2НЕ9збЗБоШЦЙлгЕ9йНЖ50ЧшС0МЗБедУБ1еР==`

@anfinogenov

## WriteUp 

It's strictly recommended to read "Message from base" [writeup](../Message%20from%20base/README.md) before reading this one.

`Анотхер месседж фром бейс -> Another message from base`  
[Google translate](https://translate.google.ru/#view=home&op=translate&sl=ru&tl=en&text=%D0%90%D0%BD%D0%BE%D1%82%D1%85%D0%B5%D1%80%20%D0%BC%D0%B5%D1%81%D1%81%D0%B5%D0%B4%D0%B6%20%D1%84%D1%80%D0%BE%D0%BC%20%D0%B1%D0%B5%D0%B9%D1%81)

First note - there are two `==` in the end of message. This is good indicator of base64 encoding. 

We'll use the [analyser.py](../Message%20from%20base/analyser.py) from "Message from base" [writeup](../Message%20from%20base/README.md)

```
Unique letters: 48
0: 3
1: 1
2: 9
3: 3
5: 2
7: 1
9: 4
=: 2
Б: 10
В: 2
-- cut --
Ш: 8
Щ: 4
а: 3
б: 2
-- cut --
ш: 10
щ: 5
```

What do we see?
1. `Unique letters: 48`, so it's at least base `48`
    - `=` is used as padding, and must be excluded from final alphabet, so - `base47`
2. `4, 6, 8` are missing, but required, so it's at least base `50`
3. We see `щ` as maximum letter in lowercase alphabet, and `Щ` in uppercase.  
[Wiki: Russian alphabet](https://en.wikipedia.org/wiki/Russian_alphabet) - `Щ` has unicode value of `U+0429`, and `А` has value of `U+0410`, so `Щ` is 26th letter of russian alphabet, so it's at least `base62 (10+26+26)`
```python
>>> ord('Щ') - ord('А')
25
```
4. Don't forget about `+/`, although they do not meet in encoded text. We are approaching magic number of `64` 

It looks exactly like base64, but with another (russian) alphabet:
- `0-9`: 10 digits
- `A-Z (А-Щ)`: 26 letters
- `a-z (а-щ)`: 26 letters
- `+/=`: 2 letters + padding  
64 letters in total.

Let's write a simple [decoder](solve.py), that will convert cyrillic alphabet to latin, and then decode it as classic `base64`

```
$ ./solve.py гЖзпвшБпвшБзИЗНлШ3ЙлгВБуЩЧНщШЦглИЖЩшб20жа2Ейа2ХшвщоКХ2ФжШЧЙлИЖСпв2НхгмХшЩЦРтИЖ5лгшБиШЧНлИЖЕйШ2ХщвшБцШЧНщг29шЩВБпвшБса3Н7Ш3ХщгЖ9уЧ2И2НЕ9з
бЗБоШЦЙлгЕ9йНЖ50ЧшС0МЗБедУБ1еР==
this is a secret message from kackers:
We are discovered, new base access password is kks{custom_b64_alphabet_c4nt_$t0p_y0u}
```

Flag is `kks{custom_b64_alphabet_c4nt_$t0p_y0u}`