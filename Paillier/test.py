from Paillier import *
import random
from cryptoutil import strToAsciiInt, asciiIntToStr

def main():
    priv, pub = generate_keypair()
    #x = random.randint(0,99999999)
    x = "ABCDEFGHabcd"
    enc = encrypt(pub, strToAsciiInt(x))
    dec = asciiIntToStr(decrypt(priv, pub, enc))
    print("{0}\nencrypted = {1}\ndecrypted = {2}\nx == dec? {3}".format(x,enc,dec,x==dec))

if __name__ == "__main__":
    main()