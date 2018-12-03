from sha1 import sha1

"""
perform hmac with blockSize = 64 bytes; outputSize = 20 bytes
@param key: array of bytes to use as the key
@param msg: array of bytes to use as the message
@param hFunc: hashing function (should ultimately be our own sha1 implementation)
"""
def hmac(key,msg,hFunc=sha1,blockSize = 64): 
    #Keys longer than blockSize are shortened by hashing them
    if (len(key) > blockSize):
        key = (key.decode("utf-8")[:blockSize]).encode("utf-8")
       
    #Keys shorter than blockSize are padded to blockSize by padding with zeros on the right
    if (len(key) < blockSize):
        key = (key.decode("utf-8") + chr(0) * (64 - len(key))).encode("utf-8") #pad key with zeros to make it blockSize bytes long
    
    o_key_pad = bytesxor(key,(0x5c * blockSize)) #Outer padded key
    i_key_pad = bytesxor(key,(0x36 * blockSize)) #Inner padded key
    return hFunc(bytesconcat(o_key_pad,hFunc(i_key_pad + msg))) #Where + is concatenation

"""
perform an xor on a bytestring and an int
@param b: the bytestring to xor
@param i: the int to xor
@returns: the xor of int(b) and i, re-encoded as a bytestream
"""
def bytesxor(b,i):
    return str(int(b.hex(),16)^i).encode("utf-8")

"""
perform a concatenation on a bytestring and an int
@param b: the bytestring to concatenate
@param i: the int to concatenate
@returns: the concatenation of int(b) and i, re-encoded as a bytestream
""" 
def bytesconcat(b,i):
    return (b.decode("utf-8")+str(i)).encode("utf-8")
    
if __name__ == "__main__":
    KEY = "key"
    MESSAGE = "hello"
    print(hmac(KEY.encode('utf-8'), MESSAGE.encode('utf-8')))
    print(hmac(KEY.encode('utf-8'), MESSAGE.encode('utf-8'))=="7cd394cecfc56075888e45bb87118241325d556f")