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