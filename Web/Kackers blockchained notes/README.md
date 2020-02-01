# Kackers blockchained notes


**Category:** Web

**Points:** 919

**Description:**

We found a strange service with secrets that use blockchain-like technology. Evil kackers use it to store their secrets, maybe u can find something interesting.

http://tasks.open.kksctf.ru:20005/

@thunderstorm8

## WriteUp 

Honestly, category of this task was PPC:)

Even we open a task, we see an input field and self-made catpcha.

Site asks us to pass a value, which MD5 ends with chars from capcha 

For example: capcha `d055` `md5(1234) => 81dc9bdb52d04dc20036dbd8313ed055` => `1234` will be solve for this capcha

There was hidden input with an md5(`number in captcha`) and all of them were in rainbow tables;)

There were two steps of getting capcha's value:
- OCR
- reverting hashes

My way was second way, it's easer!

After getting the vlalue we have some different ways again:
 - build a dictionary with all md5 of 4 chars words in alph `a-z0-9`
 - hashing and incrimenting (in solver)
 
 Next step is `md5(current_hash_from_link + secret) + .php`
 
 Do the same ~ 430 times 
 
 
