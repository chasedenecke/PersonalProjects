# This program finds the first triangle number with more than 'N' divisors.
# A triangle number is any number than can be written as the sum of all integers from 1 to M for some integer M.

import math
import itertools

# This program relies on factoring each triangle number into its constituent primes to function.
# As such, it needs a list of all primes. But since we do not know ahead of time how many primes we
# need to find, the below function can take a list of primes as the second argument, and it will
# append primes to the list until it reaches n.
# This function uses a modified version of the Sieve of Eratothsenes.
def findPrimesUpToN(n, listOfPrimes):
	if listOfPrimes == []: # If listOfPrimes is empty, replace it with a list containing the first prime (2)
		listOfPrimes = [2] # Then set the starting range (the next number whose primacy it will check) to 3
		startingRange = 3
	if listOfPrimes != []: # If listOfPrimes is not empty, set the starting range to 1 higher than the largest prime in the list
		startingRange = listOfPrimes[len(listOfPrimes)-1] + 1 
	for x in range(startingRange, math.floor(n*2)): # This *2 part is a crappy hack to fix a "list index out of range" error I was getting
		isPrime = True
		for y in listOfPrimes:
			if y > math.sqrt(x):
				break
			if x % y == 0:
				isPrime = False
				break
		if isPrime == True:
			listOfPrimes.append(x)
	return listOfPrimes

# This function factors a number 'N' into its consituent primes. It takes a list of primes, which it then passes to the
# "findPrimesUpToN" function. By passing this argument instead of declaring it in the function, we can keep the list of primes between function calls
# so that we don't need to regenerate the entire list of primes every time we want to factor another number.
# The function returns a list containing the prime factorization of the number 'N'.
# So the list of factors for 7 would be [0, 0, 0, 0, 0, 0, 0, 1]
# factors of 12 would be [0, 0, 2, 1]. Notice how array[2] has a 2 in it, because there are two factors of 2 in 12.
# factors of 36 would be [0, 0, 2, 2]
# factors of 120 would be [0, 0, 3, 1, 0, 1]
def findPrimeFactors(n, listOfPrimes):
	primeFactors = [0 for i in range(n+1)]
	listOfPrimes = findPrimesUpToN(math.floor(math.sqrt(n)), listOfPrimes) # Generate all of the primes up to the square root of the number we're trying to factor.
	nIsPrime = False														# It turns out that if a number isn't divisible by any primes less than or equal to its square root, then you know it's prime. #MathFacts
	while nIsPrime == False:
		j = 0
		nIsPrime = True
		while listOfPrimes[j] <= math.sqrt(n):
			if n % listOfPrimes[j] == 0:
				n = math.floor(n / listOfPrimes[j]) # If the number is divisible by that prime, add that prime to its list of factors and divide the number by that prime for the next iteration of factoring.
				primeFactors[listOfPrimes[j]] += 1 # This line is the one adding the factors to the list
				nIsPrime = False
				break
			j += 1
	primeFactors[n] += 1
	return primeFactors, listOfPrimes

# This function takes an integer N and returns the value of the first triangle number with at least N divisors
# The trickiest thing about this function is the way it finds the factors of a triangle number.
# The nth triangle number is equal to n(n+1)/2. To factor this number faster, I simply factored n and n+1,
# and subtracted a factor of two from whichever one of those was even. This saves a lot of time.
# Another trick of this function is that it actually only every calculates the factors of n+1.
# For example: suppose we want to find the factors of the 4th triangle number. The 4th triangle number = 4(4+1)/2. So we find the factors of 4 and 5.
# For the next triangle number, we need the factors of 5 and 6. But we've already factored 5 for the previous trangle number, so we just reuse the array of factors from the last iteration.
# This cuts run time in half.
def findFirstTriangleNumberWithOverNDivisors(n):
	divisors = 1
	factorsArray1 = [0, 0, 0, 1] #This is the factors array for 3, which is the 2nd triangle number. factorsArray[3] = 1, which indicates that 3 has a single prime factor of 3. The factor array for 4 would be [0, 0, 2, 0, 0]
	factorsArray2 = []
	listOfPrimes = []
	for x in itertools.count(4): # x is (n+1) from the formula
		if x % 2 == 1: # If x is odd, store its factors in the second array
			factorsArray2, listOfPrimes = findPrimeFactors(x, listOfPrimes)
		else: # If x is even, store its factors in the first array
			factorsArray1, listOfPrimes = findPrimeFactors(x, listOfPrimes)
			factorsArray1[2] -= 1 # Since the formula for the Nth triangle number is n(n+1)/2, we need to remove a factor of 2 from the array containing the factors of the even number.
		divisors = 1
		for factOne, factTwo in itertools.zip_longest(factorsArray1, factorsArray2): 	# zip_longest is a neat little function in python that allows you to iterate through two lists of different lengths and assign each element to a variable.
			if factOne == None:															# When the shorter list runs out of elements, the iterator assigned to it is set to 'None'
				factOne = 0
			if factTwo == None:
				factTwo = 0
			divisors *= factOne + factTwo + 1 # The most difficult to explain part of this code. See explanation below.
		if divisors > n:
			break
	print(math.floor(x*(x-1)/2))

# EXPLANATION OF divisors *= factOne + factTwo + 1
# Every divisor of a number is a product of a subset of the prime factors of that number.
# For example, 12 has a prime factorization of 2*2*3. Our divisors can have 0, 1, or 2 factors of 2 and 0 or 1 factors of 3.
# So 12 has 3*2 = 6 divisors.
# To demonstrate: the divisors of 12 are 1, 2, 3, 4, 6, 12
# 1 = 2^0 * 3^0
# 2 = 2^1 * 3^0
# 3 = 2^0 * 3^1
# 4 = 2^2 * 3^0
# 6 = 2^1 * 3^1
# 12 = 2^2 * 3^1
# So for a number M with a prime factorization p1^e1*p2^e2*p3^e3*....*pn^en, the number of divisors
# of M is (e1+1)(e2+1)(e3+1)....(en+1)
findFirstTriangleNumberWithOverNDivisors(500)