import random

"""miller-robin primality check
@param n: the number to test for primality
@returns: whether the miller-robin primality check yielded true or false
"""
def millerRobin(n):
    """main test component of the primality check; performed k times
    @param d: the value calculated in step 3 st d*2^r = n-1
    """
    def millerTest(d):
        """calculate modular exponentiation of (x^y)%p
        @param x: copy of a
        @param y: copy of d
        @param p: copy of n
        """
        def power(x,y,p):
            res = 1
            x = x % p;
            while (y > 0):
                if ((y & 1) == 1):
                    res = (res * x) % p
                y = y >> 1
                x = (x * x) % p
            return res
        
        a = 2 + int((random.random() % (n - 4)))
        #Compute a^d % n
        x = power(a, d, n)
        #base case
        if (x == 1 or x == n - 1):
            return True
      
        #square x until d reaches n-1, or (x^2) % n becomes 1 or n-1
        while (d != n - 1):
            x = x**2 % n
            d *= 2
            if (x == 1):
                return False
            if (x == n - 1):
                return True
      
        #return composite
        return False
    k = 100
    
    #1. base case: small #'s
    if (n <= 3):
        return True if n > 1 else False
    
    #2. base case: even #'s
    if (n%2 == 0):
        return False
    
    #3. search for value d*2^r = n-1
    d = n - 1 
    while (d % 2 == 0): 
        d //= 2 
    
    #4. apply miller test k times
    for _ in range(k):
        if (not millerTest(d)):
            return False
    return True

"""pollard-rho factorization algorithm
@param n: the number to factorize
@returns: a factor of n or None, if no such factor was discovered
"""
def pollardRho(n,secondTry = False):
    """hard-coded polynomial; here we use (x^2+1)%n
    @param v: the value to run through the polynomial
    @param secondTry: whether or not this is our second try; if it is, initialize x and y to 3 instead of 2
    @returns: the result of applying v to g
    """
    def g(v):
        return (v**2+1)%n
    
    """calculate the greatest common divisor of two numbers
    @param a: the first number
    @param b: the second number
    @returns: the greatest common divisor of a and b
    """
    def gcd(a, b):
        while b:
            a, b = b, a%b
        return a

    x = y = 3 if secondTry else 2
    d = 1
    while (d == 1):
        x = g(x)
        y = g(g(y))
        d = gcd(abs(x - y), n)
    if (d == n):
        #if this is our first attempt, try again with x=y=3; otherwise, there's nothing more we can do
        return None if secondTry else pollardRho(n,True)
    return d

"""
generate a random prime of bits number of bits
@param bits: number of bits in the desired prime
@returns: a prime with bits number of bits
"""
def generatePrime(bits):
    while True:
        p = random.randrange(2 ** (bits-1) + 1, 2 ** bits) | 1
        if millerRobin(p):
            return p

def main():
    for i in [31531, 520482, 485827, 15485863]:
        print("{0} is {1}".format(i,"prime" if millerRobin(i) else "not prime; factoring it yields {0}".format(pollardRho(i))))

if __name__ == "__main__":
    main()
