# Predictor


**Category:** Web

**Points:** 997

**Description:**

We found a login form to the kackers secret site. It seems to be using some kind of OTP, and we intercepted some strange file. I think evil kackers are keeping something important there, try to get it out!

http://tasks.open.kksctf.ru:20007/

@rubikoid

## WriteUp 

### crypto.py

The file [crypto.py](service/crypto.py) was given in the task. It contains an implementation of a simple algorithm for creating one-time passwords.

On registering a new user, taking number from __base random__ ([`context.basic_random.randint(0, 4294967294)`](service/crypto.py#L21)) and add it to crc32 as a user. The resulting number is used as a seed for the __user's random__, on which passwords are created.

In addition, there is a method to regenerate the __user's random__ seed from the current state of the __base random__. ([`def regen_seed(self)`](service/crypto.py#L38))

The file also contains the creation of the "admin" user when creating the context and a disallowed displaying the __user's random__ seed.

To create passwords, the standard python `random` library used. It based on the *Mersenne Twister*. It can be predicted by getting 624 32-bit numbers from the random. This is the first vulnerability.

### service

If you go to the service itself, you can see three forms: registration, authorization and re-creation of a __user's random__.

There was a second vulnerability in the method of re-generation of the __user's random__ - the password was not checked. Specifically, the regeneration was successful with any password except the correct one. (see [`if otp == context.users[login].gen_pass()`](service/deploy/app/__init__.py#L90))

It was also necessary to see that the server creates a session cookie during which [`class context'](service/crypto.py#L8) exists. This is done to ensure that two different exploits do not overlap, otherwise, it is impossible to solve the problem.

### exploit

To solve the task it is required somehow to get 624 values from the __base generator__, and then, having predicted the next value of the __base random__, get the seed of the admin's __user's random__, generate password and login under admin.

Intended solution: create 624 accounts, calculate the numbers taken from prng (i.e. subtract crc32 username), then, having predicted the next value of the __base random__, re-generate the admin's __user's random__ and login. The actual implementation is in the file [exploit.py](service/exploit.py).
