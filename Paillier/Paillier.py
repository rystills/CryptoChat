import math
import types
import primality
import cryptoutil

"""
generate private and public key
@param bits: number of bits to use in key generation
@returns: a tuple of dict-like objects (privateKey, publicKey)
"""
def generate_keypair(bits=128):
    p = primality.generatePrime(bits // 2)
    q = primality.generatePrime(bits // 2)
    l = (p-1) * (q-1)
    n = p*q
    return types.SimpleNamespace(l=l, m=cryptoutil.modInv(l, p*q)), types.SimpleNamespace(n=n,n2=n*n)

"""
encrypt the specified message using the specified public key
@param pub: public key
@param msg: message to encrypt
@returns: the encrypted msg
"""
def encrypt(pub, msg):
    r = 0
    while not (r > 0 and r < pub.n):
        r = primality.generatePrime(round(math.log(pub.n, 2)))
    return (pow(pub.n+1, msg, pub.n2) * pow(r, pub.n, pub.n2)) % pub.n2

"""
decrypt the specified message using the specified public and private key
@param priv: private key
@param pub: public key
@param msg: encrypted message to decrypt
@returns: the decrypted msg
"""
def decrypt(priv, pub, msg):
    return (((pow(msg, priv.l, pub.n2) - 1) // pub.n) * priv.m) % pub.n