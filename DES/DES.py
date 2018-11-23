#provide some default key; feel free to change this, as long as it remains 10 bits
defaultKey = [1,1,1,0,0,0,1,1,1,0]

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
external input method for toy DES decryption
@param bitArr: the bit array to decrypt
@param bitKey: the decryption key to use
@return: the result of decrypting the input bit array using the input key
""" 
def decrypt(bitArr,bitKey):
    decBits = []
    for i in range(0,len(bitArr),8):
        #we can use encrypt when going in either direction, as long as we implemented DES correctly
        decBits += DES(bitArr[i:i+8],bitKey,False)
    return decBits

"""
external input method for toy DES encryption
@param bitArr: the bit array to encrypt
@param bitKey: the encryption key to use
@return: the result of encrypting the input bit array using the input key
""" 
def encrypt(bitArr,bitKey):
    encBits = []
    for i in range(0,len(bitArr),8):
        encBits += DES(bitArr[i:i+8],bitKey)
    return encBits

"""
core DES encryption/decryption method
@param bits: the 8 bit array to encrypt
@param key: the encryption key to use
@param encrypting: whether to encrypt (true) or decrypt (false)
@return: the result of encrypting/decrypting the input but array using the input key
""" 
def DES(bits,key, encrypting = True):
    #DES constants
    initialPermutation = [2,6,3,1,4,8,5,7]
    keyPermutation = [3,5,2,7,4,10,1,9,8,6]
    KeyPermutation8Bit = [6,3,7,4,8,5,10,9]
    inverseInitialPermutation = [4,1,3,5,7,2,8,6]
    FExpandPermutation = [4,1,2,3,2,3,4,1]
    FRecombinePermutation = [2,4,3,1]
    S0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
    S1 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]
    """
    DES helper method; scrambles input bits using S-boxes and input key
    @param bits: the 4 bit array
    @param key: the 8 bit key
    @return: the result of manipulating the input bits using the input key
    """ 
    def F(bitArr,keyArr):
        #1. expand/permutate bit array
        expandedBits = [0,0,0,0,0,0,0,0]
        for i in range(len(expandedBits)):
            expandedBits[i] = bitArr[FExpandPermutation[i]-1]
            
        #2. xor with key
        xorbits = xor(expandedBits,keyArr)
        
        #3. split xor list into 2 4-bit lists
        xorlbits = xorbits[:4]
        xorrbits = xorbits[4:]
        
        #4. index into s-boxes, and convert the resulting int back into binary, left-padding with a 0 if necessary
        lsbits = [int(i) for i in list(("0" + "{0:b}".format(S0[xorlbits[0]*2 + xorlbits[3]][xorlbits[1]*2 + xorlbits[2]]))[-2:])]
        rsbits = [int(i) for i in list(("0" + "{0:b}".format(S1[xorrbits[0]*2 + xorrbits[3]][xorrbits[1]*2 + xorrbits[2]]))[-2:])]
        
        #5. recombine and permutate
        recombinedBits = [0,0,0,0]
        for i in range(len(recombinedBits)):
            recombinedBits[i] = lsbits[FRecombinePermutation[i]-1] if FRecombinePermutation[i]-1 < 2 else rsbits[FRecombinePermutation[i]-1-2]
        
        #done
        return recombinedBits
    
    #1. apply initial permutation
    encBits = [0,0,0,0,0,0,0,0]
    for i in range(len(encBits)):
        encBits[i] = bits[initialPermutation[i]-1]
        
    #2. split bits
    lbits = encBits[:4]
    rbits = encBits[4:]
    
    #3. apply key permutation
    keyBits = [0,0,0,0,0,0,0,0,0,0]
    for i in range(len(keyBits)):
        keyBits[i] = key[keyPermutation[i]-1]
    
    #4. split key
    lkey = keyBits[:5]
    rkey = keyBits[5:]
    
    #5. left shift key halves
    lkey.pop(0)
    lkey.append(0)
    rkey.pop(0)
    rkey.append(0)
    
    #6. recombine into 8 bit key k1
    k1 = [0,0,0,0,0,0,0,0]
    for i in range(len(k1)):
        k1[i] = lkey[KeyPermutation8Bit[i]-1] if KeyPermutation8Bit[i]-1 < 5 else rkey[KeyPermutation8Bit[i]-1-5]
    
    #7. left shift key halves a second time
    lkey.pop(0)
    lkey.append(0)
    rkey.pop(0)
    rkey.append(0)
    
    #8. recombine into 8 bit key k2
    k2 = [0,0,0,0,0,0,0,0]
    for i in range(len(k2)):
        k2[i] = lkey[KeyPermutation8Bit[i]-1] if KeyPermutation8Bit[i]-1 < 5 else rkey[KeyPermutation8Bit[i]-1-5]
        
    #9. call F with k1, then xor with lbits
    Fval1 = xor(F(rbits,k1 if encrypting else k2),lbits)
    
    #10. call F with k2, then xor with rbits
    Fval2 = xor(F(Fval1,k2 if encrypting else k1),rbits)
    
    #11. apply inverse initial permutation on the concatenation of our second result with our first result
    bitsFinal = [0,0,0,0,0,0,0,0]
    for i in range(len(bitsFinal)):
        bitsFinal[i] = Fval2[inverseInitialPermutation[i]-1] if inverseInitialPermutation[i]-1 < 4 else Fval1[inverseInitialPermutation[i]-1-4]
    
    #done
    return bitsFinal