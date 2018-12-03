import hashlib

#def sha1(msg):
#    pass

"""
perform hmac with blockSize = 64 bytes; outputSize = 20 bytes
@param key: array of bytes to use as the key
@param msg: array of bytes to use as the message
@param hFunc: hashing function (should ultimately be our own sha1 implementation)
"""
def hmac(key,msg,hFunc): 
    blockSize = 64
    #outputSize = 20
    #Keys longer than blockSize are shortened by hashing them
    if (len(key) > blockSize):
        key = hFunc(key) #Key becomes outputSize bytes long
       
    #Keys shorter than blockSize are padded to blockSize by padding with zeros on the right
    if (len(key) < blockSize):
        key = (key.decode("utf-8") + chr(0) * (64 - len(key))).encode("utf-8") #pad key with zeros to make it blockSize bytes long
    
    o_key_pad = bytesxor(key,(0x5c * blockSize)) #Outer padded key
    i_key_pad = bytesxor(key,(0x36 * blockSize)) #Inner padded key
    
    return hFunc(bytesconcat(o_key_pad,hFunc(i_key_pad + msg).hexdigest())).hexdigest() #Where + is concatenation

def bytesxor(b,i):
    return str(int(b.hex(),16)^i).encode("utf-8")
    
def bytesconcat(b,i):
    #return str(int(b.hex(),16)+i).encode("utf-8")
    return (b.decode("utf-8")+str(i)).encode("utf-8")
    
if __name__ == "__main__":
    KEY = "key"
    MESSAGE = "hello"
    print((hmac(KEY.encode('utf-8'), MESSAGE.encode('utf-8'), hashlib.sha1)))