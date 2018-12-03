#utility method from https://stackoverflow.com/questions/10237926/convert-string-to-list-of-bits-and-viceversa
"""
convert a string to a list of bits
@param s: the string to convert
@return: the bit list equivalent of s
"""
def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

#utility method from https://stackoverflow.com/questions/10237926/convert-string-to-list-of-bits-and-viceversa
"""
convert a list of bits to a string
@param bits: the list of bits to convert
@return: the string equivalent of bits
"""
def frombits(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

"""
create a new list of bits containing the result of an exclusive or on the input lists
@param l1: the first list
@param l2: the second list
@return: the result of an exclusive or on l1 and l2
"""
def xor(l1,l2):
    newList = []
    for i in range(len(l1)):
        newList.append(1 if (l1[i] == 1 or l2[i] == 1) and (l1[i] != l2[i]) else 0)
    return newList

"""
convert a string ins to an int containing the combination of the ascii values of all chars in ins
@param ins: the input string to convert to an int
@returns: the int containing the combination of ascii values of all chars in ins
"""
def strToAsciiInt(ins):
    ai = ""
    for s in ins:
        ns = str(ord(s))
        ai += "0"*(3-len(ns))+ns
    return int(ai)
    
"""
convert an int containing a combination of ascii values back into a string
@param ai: the input ascii int to convert to a string
@returns: the string represented bu the combination of ascii values in ai
"""
def asciiIntToStr(ai):
    msg = "0"*(3-(len(str(ai))%3 if len(str(ai))%3 != 0 else 3))+str(ai)
    s = ""
    for i in range(0,len(msg),3):
        s+=chr(int(msg[i:i+3]))
    return s

"""
left rotate a 32-bit integer n b bits
@param n: integer to rotate
@param b: #bits by which to rotate n
@returns: the integer n rotated by the #bits b
"""
def _left_rotate(n, b): 
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

"""
calculate the modular inverse of a and m
@param a: first value for which we wish to calculate the modular inverse
@param m: second value for which we wish to calculate the modular inverse
@returns: the modular inverse of a and m
"""
def modInv(a, m):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
    return egcd(a, m)[1] % m

"""
perform the extended euclid function on the provided primes
@param a: first prime
@param b: second prime
@returns: the values s and t such that a*s + b*t = 1
"""
def extEuclid(a,b):
    if (b == 0):
        return (1,0)
    s1, t1 = extEuclid(b,a%b)
    return t1,s1 - (a // b) * t1

def main():
    a = "test string"
    b = strToAsciiInt(a)
    c = asciiIntToStr(b)
    print(a,b,c)

if __name__ == "__main__":
    main()