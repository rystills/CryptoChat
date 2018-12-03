import struct, io
import cryptoutil

"""
process a 64 chunk of data, returning the modified h0-h4 digest values
@param chunk: the data chunk to process
@param h0: 0th hex digest value
@param h1: first hex digest value
@param h2: second hex digest value
@param h3: third hex digest value
@param h4: fourth hex digest value
"""
def processChunk(chunk, h0, h1, h2, h3, h4):
    #break chunk into 4-byte words
    w = [0] * 80
    for i in range(16):
        w[i] = struct.unpack(b'>I', chunk[i * 4:i * 4 + 4])[0]
    for i in range(16, 80):
        w[i] = cryptoutil._left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

    #calculate hash values
    a,b,c,d,e = h0,h1,h2,h3,h4
    for i in range(80):
        f,k = (d ^ (b & (c ^ d)),0x5A827999) if i < 20 else (b ^ c ^ d,0x6ED9EBA1) if i < 40 else \
        ((b & c) | (b & d) | (c & d),0x8F1BBCDC) if i < 60 else (b ^ c ^ d,0xCA62C1D6)
        a,b,c,d,e = ((cryptoutil._left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff,a, cryptoutil._left_rotate(b, 30), c, d)
    return tuple([i&0xffffffff for i in (h0+a,h1+b,h2+c,h3+d,h4+e)])

"""hash a data message using sha1, returning the hex digest
@param data: the bytes message to hash
@returns: the hex digest of the sha1 hash of data
"""
def sha1(data):
    h = (0x67452301,0xEFCDAB89,0x98BADCFE,0x10325476,0xC3D2E1F0) #standard starting digest values
    msgLen = len(data.decode("utf-8"))
    bData = io.BytesIO(data) #convert data to a bytestream so we can read words easily
 
    #read in groups of 64 bytes
    for _ in range(64,msgLen,64):
        h = processChunk(bData.read(64), *h)

    #pad message with b"1, congruence to 56 (mod 64), message length in words
    msg = bData.read(64) + (b'\x80' + (b'\x00' * ((56 - (msgLen + 1) % 64) % 64))) + struct.pack(b'>Q', msgLen * 8)
    
    #process remaining data
    h = processChunk(msg[:64], *h)
    return "%08x%08x%08x%08x%08x" % (h if len(msg) == 64 else processChunk(msg[64:], *h))