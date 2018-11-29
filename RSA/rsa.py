# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 20:56:52 2018

@author: Tommy
"""

import math, random

def coprime(x, y):
    return math.gcd(x, y) == 1

def lcm(x,y):
    lcm = (x*y)//math.gcd(x,y)
    return lcm
    
# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(e, lam):
    g, x, _ = extended_euclid(lam, e)
    if g == 1:
        return x % lam

        
def extended_euclid(totient,e):
    x0 = 1
    x1 = 0
    y0 = 0
    y1 = 1
    temp = totient
    while e>0:
        q = int(totient/e) # a>b
        r = totient - q*e
        x = x1 - q*x0
        y = y1 - q*y0
        
        totient = e
        e = r
        x1 = x0
        x0 = x
        y1 = y0
        y0 = y
        
    d = totient
    x = x1
    y = y1
    return d, x, y

def main():
    p = 61
    q = 53
    n = p*q
    #totient = (p-1)*(q-1)
    lcm2 = lcm(p-1,q-1)
    
    #e must be coprime to totient, and using iteration to find totient to easy
    #to break
    e = random.randrange(2, lcm2)
    testCo = coprime(e, lcm2)
    
    
    
    while testCo != True:
        #changed 1 to 2 so cant use 1 as the coprime
        e = random.randrange(2, lcm2)
        testCo = coprime(e, lcm2) 
    
    #hardcoded to test examples
    e = 17
      
    d = mulinv(e,lcm2)

    public_key = (n, e)
    private_key = (n, d)    
    print("P=",p," Q=",q," n=",n," e=",e," lcm=",lcm2," d=",d)
    print("Public key is :", public_key)
    print("Private key is:", private_key)
if __name__ == "__main__":
    main()