# Not Quick Enough


**Category:** Misc

**Points:** 971

**Description:**

To: Me my_mail123@mirea.ru  
From: Chandler thegreatchad@example.com  
Subject: work stuff  

Hey buddy,

How's it going? I was wondering if you could help our team out with a test case of sorts. We wrote a prototype service which is meant for sorting arrays but we haven't had enough time to test it through.

Do you mind helping out with some testing? Just going through the motions and seeing that everything runs OK without crashing on the user's side would be fine. Feel free to tell me if you're too busy and won't have time for it, too.

You can find it here:
`nc tasks.open.kksctf.ru 8009`

Thank you in advance!

https://drive.google.com/open?id=1wmUifOkBGOlFFrVuODoXFzF84oWcSDn2

## WriteUp 
The *main* function calls *sort* which can sometimes cause a *RecursionError*. Looking closer at the *sort* function can prove useful to make out similarities to the *quicksort* algorithm. The effectiveness of the latter is heavily dependent on the input as well as on the way the *pivot* element is selected. If an element is not selected optimally, it's possible to make the number of recursive calls match the inputted array size. For example, if the leftmost element is the *pivot* one and the inputted array has already been sorted, then *qsort* will be called recursively every step for the left partition with size 1 and for the right partition with size *n* - 1, where *n* is the size of a subarray at a certain step of the recursion. Since the program makes sure the array size doesn't exceed the recursion depth, the high end of recursion depth can be estimated by passing the algorithm multiple arrays of different lengths. In Python, the default value for this is 1000.

As we can see from the following line, a median from the left, the right and a randomly chosen subarray elements is chosen as the *pivot* element:

    pivot = median(a[l], a[r], a[Random.rand(l, r)])

The median for numbers *a*, *b* and *c* is a single number which is located "between" the lowest and the highest number, i. e., if *a* <= *b* <= *c*, *b* is the median. Note two things here: in any case with three differing numbers any one of them can turn out to be the median, and in case where two numbers out of three are identical, the median will always be the repeating number (e. g. median(1, 1, -100) = 1 and median(1, 1, 100000) = 1). If we can guarantee that the number obtained when *Random.rand(l, r)* is called is always equal to *l*, then this particular occasion is an instance of a poor choice of the *pivot* element.

Let's now take a closer look at the *Random* class:

	class Random:
		seed = 0

   		@staticmethod
   		def srand(array):
        		Random.seed = array[0]
        		i = 1
        		while Random.seed <= 0 and  i < len(array):
            			Random.seed = array[i]
            			i += 1
       		 	if Random.seed <= 0:

    		@staticmethod
    		def rand(x, y):
       			Random.seed += 1
       		 	return x + Random.seed % (y - x + 1)

The *Random* class consists of two static methods, one of which initializes *seed* using first non-negative number in an array and another one returns a number between *x* and *y* that depends on *seed* and increments *seed* by one. To make *rand* always match the left end of the array, we need for the *seed mod (y - x + 1)* to always equate to 0. Let's find such *seed* value. Assume the starting array length equals 1000, *l = 0* and *r = 999*. Then *seed + 1* must be divisible by 1000, *seed + 2* by 999, *seed + 3* by 998, etc. A number that could satisfy these conditions is 1000! - 1001. Now we need to create an array sorted in ascending order whose first positive number will be the *seed* value we calculated. This one, for example:

	array = [math.factorial(1000) - 1001 + i for i in range(1000)]

By generating and then passing the array above into the program (e. g., using Python's pwntools), a file *emergency_instructions.txt* containing the desired flag can be obtained.

flag: 'kks{63773r_u53_5746!3_50r7_n3x7_71m3}'
