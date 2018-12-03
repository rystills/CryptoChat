
import sys

#Learned simple AES from https://www.rose-hulman.edu/~holden/Preprints/s-aes.pdf

# S-Box
sBox  = [0x9, 0x4, 0xa, 0xb, 0xd, 0x1, 0x8, 0x5,
         0x6, 0x2, 0x0, 0x3, 0xc, 0xe, 0xf, 0x7]

# Inverse S-Box
sBoxI = [0xa, 0x5, 0x9, 0xb, 0x1, 0x7, 0x8, 0xf,
         0x6, 0x0, 0x2, 0x3, 0xc, 0x4, 0xd, 0xe]

rounds = [None] * 6

def polyMultiply(polyA, polyB):
    poly = 0
    while polyB:
        if polyB & 0b1:
            poly ^= polyA
        polyA <<= 1
        if polyA & 0b10000:
            polyA ^= 0b11
        polyB >>= 1
    return poly & 0b1111

def keyExp(key):
    def smallSub(smol):
        return sBox[smol >> 4] + (sBox[smol & 0x0f] << 4)

    x, y = 0b10000000, 0b00110000

    rounds[0] = (key & 0xff00) >> 8
    rounds[1] = key & 0x00ff
    rounds[2] = rounds[0] ^ x ^ smallSub(rounds[1])
    rounds[3] = rounds[2] ^ rounds[1]
    rounds[4] = rounds[2] ^ y ^ smallSub(rounds[3])
    rounds[5] = rounds[4] ^ rounds[3]

def addKey(s1, s2):
    return [i ^ j for i, j in zip(s1, s2)]

def intToVec(num):
    return [num >> 12, (num >> 4) & 0xf, (num >> 8) & 0xf,  num & 0xf]

def vecToInt(vec):
    return (vec[0] << 12) + (vec[2] << 8) + (vec[1] << 4) + vec[3]

def subBytes(sbox, s):
    return [sbox[i] for i in s]

def shiftRow(shift):
    return [shift[0], shift[1], shift[3], shift[2]]

def encrypt(plainText):
    def mixColumn(s):
        return [s[0] ^ polyMultiply(4, s[2]), s[1] ^ polyMultiply(4, s[3]),
                s[2] ^ polyMultiply(4, s[0]), s[3] ^ polyMultiply(4, s[1])]

    step = intToVec(((rounds[0] << 8) + rounds[1]) ^ plainText)

    step = mixColumn(shiftRow(subBytes(sBox, step)))

    step = addKey(intToVec((rounds[2] << 8) + rounds[3]), step)

    step = shiftRow(subBytes(sBox, step))

    return vecToInt(addKey(intToVec((rounds[4] << 8) + rounds[5]), step))

def decrypt(crypto):
    def imixColumn(s):
        return [polyMultiply(9, s[0]) ^ polyMultiply(2, s[2]), polyMultiply(9, s[1]) ^ polyMultiply(2, s[3]),
                polyMultiply(9, s[2]) ^ polyMultiply(2, s[0]), polyMultiply(9, s[3]) ^ polyMultiply(2, s[1])]

    step = intToVec(((rounds[4] << 8) + rounds[5]) ^ crypto)

    step = subBytes(sBoxI, shiftRow(step))

    step = imixColumn(addKey(intToVec((rounds[2] << 8) + rounds[3]), step))

    step = subBytes(sBoxI, shiftRow(step))

    return vecToInt(addKey(intToVec((rounds[0] << 8) + rounds[1]), step))

if __name__ == '__main__':

    #test to make sure AES works
    key = 110100101011110101
    keyExp(key)

    new = 57755
    print(new)
    c = encrypt(new)
    print(c)
    d = decrypt(c)
    print(d)
