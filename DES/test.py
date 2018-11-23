#store a few local tests
from DES import *

def stringTest():
    print("~string test~")
    testString = "to be determined"
    testKey = [0,0,1,0,1,1,0,1,0,1]
    encrypedTest = (encrypt(tobits(testString),testKey))
    decryptedTest = frombits(decrypt(encrypedTest,testKey))
    print("input value:         {0}".format(testString))
    print("input as bits:       {0}".format(tobits(testString)))
    print("input key:           {0}".format(testKey))
    print("encrypted bit array: {0}".format(encrypedTest))
    print("decrypted bit array: {0}".format(decrypt(encrypedTest,testKey)))
    print("final value:         {0}".format(decryptedTest))

def bitTest():
    print("~bit test~")
    inBits = [1,0,1,1,0,1,0,1]
    inKey = [1,1,1,0,0,0,1,1,1,0]
    encrypted = encrypt(inBits,inKey)
    print("input:     {0}".format(inBits))
    print("key:       {0}".format(inKey))
    print("encrypted: {0}".format(encrypted))
    decrypted = encrypt(encrypted,inKey)
    print("decrypted: {0}".format(decrypted))

def xorTest():
    print("~xor test~")
    a = [1,1,1,1,1,0,0]
    b = [1,1,0,0,1,1,0]
    print("array a: {0}".format(a))
    print("array b: {0}".format(b))
    print("result:  {0}".format(xor(a,b)))