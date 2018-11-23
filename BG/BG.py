import math

"""apply Blum Goldwasser Probabilistic Algorithm (encryption) to the specified message
@param m: the message to encrypt
@param p: first Blum prime
@param q: second Blum prime
@param x0: random seed 
@returns: the result of encrypting the specified message with the specified parameters using the Blum Goldwasser algorithm
"""
def BGPEnc(m,p=499,q=547,x0=159201):
    #calculations just following the algorithm
    n=p*q
    k = int(math.log(n,2))
    h = int(math.log(k,2))
    t = len(m)//h
    #mts stores the values m_i from 1 to t; stored as strings for easy bit splicing
    mts = [m[i*h:i*h+h] for i in range(t)]
    c = []
    for m in mts:
        x0 = pow(x0, 2, n)
        #convert to a binary string to extract the last h elements
        pi = str(bin(x0))[-h:]
        for i in range(h):
            #manual bitwise or implementation for strings of bits
            c.append(1 if pi[i] != str(m[i]) else 0)
    return c,pow(x0, 2, n)

"""quick and dirty greatest common divisor calculation
@param x: first value for divisor check
@param y: second value for divisor check
@returns: the greatest common divisor of x and y
"""
def gcd(x,y):
    smaller = y if x > y else x
    for i in range(1, smaller+1): 
        if((x % i == 0) and (y % i == 0)): 
            g = i 
    return g

"""apply Blum Goldwasser Probabilistic Algorithm (decryption) to the specified message
@param m: the message to encrypt
@param x: x_t+1 value calculated from encryption step
@param p: first Blum prime
@param q: second Blum prime
@param a: first provided value
@param b: second provided value
@returns: the result of decrypting the specified message with the specified parameters using the Blum Goldwasser algorithm
"""
def BGPDec(m,x,p=499,q=547,a=-57,b=52):
    #calculations just following the algorithm
    n=p*q
    k = int(math.log(n,2))
    h = int(math.log(k,2))
    t = len(m)//h
    
    d1 = pow(((p+1)//4), t+1, p-1)
    d2 = pow(((q+1)//4), t+1, q-1)
    u = pow(x, d1, p)
    v = pow(x, d2, q)
    x0 = (v*a*p + u*b*q) % n
    #mts stores the values m_i from 1 to t; stored as strings for easy bit splicing
    mts = [m[i*h:i*h+h] for i in range(t)]
    c = []
    for m in mts:
        x0 = pow(x0, 2, n)
        #convert to a binary string to extract the last h elements
        pi = str(bin(x0))[-h:]
        for i in range(h):
            #manual bitwise or implementation for strings of bits
            c.append(1 if pi[i] != str(m[i]) else 0)
    return c

def main():
    m=[1,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,1,1,0,0]
    enc,x0 = BGPEnc(m)
    dec = BGPDec(enc,x0)
    print("              m: {0}\nciphertext C(m): {1}\n        D(C(m)): {2}\n    m = D(C(m))? {3}".format(m,enc,dec,m==dec))
    
if __name__ == "__main__":
    main()