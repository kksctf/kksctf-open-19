# Every day i'm shuffling


**Category:** Cryptography

**Points:** 481

**Description:**

![Imgur](https://i.imgur.com/W7nTKED.jpg)

@anfinogenov

https://drive.google.com/open?id=16excnDOhaQUaSVlwrzT8Sk69eboB7p-K  
https://drive.google.com/open?id=1tQfED8-ULWK2mcjodmiUPlMOK161p2Mv

## WriteUp 
We've got a file titled "fsegovs_meaoerbma_.txt", whose content and name were encrypted with the use of program *shufflin.py*. Let's inspect it first.

Python's *random.shuffle* method generates a random permutation based on a current state of pseudorandom generator and then applies it to a given list. The *random.seed* method is used to initialize a generator, meaning that its output would be very determined if we knew what exact seed had been used for encryption. Since we know the file name before ("message_from_above.txt") and after encryption ("fsegovs_meaoerbma_.txt"), we can easily brute force this seed using *shuffle*:

    from random import *
    file_name = 'fsegovs_meaoerbma_'
    s = 1
    while s <= len(file_name):
        name = list('message_from_above')
        seed(s)
        shuffle(name)
        if ''.join(name) == file_name:
            break
        s += 1

There is another *Shuffle* method (with capital 'S') in the program, which takes a constant permutation and a string as arguments and returns shuffled string. It was applied to the plain text a bunch of times, and now, to reconstruct the initial order, we need to find the permutation which has been used for encryption and then use it to generate inverse permutation and apply it just as many times as before. Note that if we used *random.shuffle* once, its next call would produce a different permutation, and since it was used twice -- to shuffle the file name and then to generate permutation to shuffle the entire text -- we don't need to call the *seed* method again.

To find an inverse permutation, use this:

    data = open(file_name + '.txt', 'r').read()
    t = list(range(len(data)))
    shuffle(t)
    p = list(range(len(data)))
    for i, j in enumerate(t):
        p[j] = i

To decrypt a file, use this:

    def Shuffle(p, data):
        buf = list(data)
        for i in range(len(data)):
            buf[i] = data[p[i]]
        return ''.join(buf)

    data = Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,Shuffle(p,data))))))))))))))))))))))))))))))))))))))))
    print(data)

The original text is an extract which comes from the poem "The Raven" by Alan Poe with the raven's quote replaced by a flag.

flag: `kks{5h4ffl3_5h4ffl3_5h4ffl3}`

Solver: [solver.py](solver.py)
