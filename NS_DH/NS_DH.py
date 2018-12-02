import random, sys, struct, time, subprocess
try:
    import sympy
except:
    print("Warning: sympy is not installed; cannot perform poly math")
    
try: import simplejson as json
except ImportError: import json
sys.path.insert(0, '../DES/'); import DES

x = sympy.Symbol('x')
encoder = json.JSONEncoder()
decoder = json.JSONDecoder()

BUFFER_SIZE = 4096

"""
map the polynomial res to GF(2)
@param res: the polynomial to map to GF(2)
returns the polynomial res mapped to GF(2)
"""
def GF(res):
    coeffs = res.all_coeffs()
    return sympy.Poly.from_list([abs(coeffs[i]%2) for i in range(len(coeffs))],gens=x)

"""
print a message preceded by your name
@param name: your name
@param s: string to print
"""
def namePrint(name, s):
    print("{0}: {1}".format(name,s))
    
"""
threaded method for printing received data during chat session
@param sock: socket to listen on
@param oName: name of other person with whom we are chatting
@param kab: decryption key"""
def chatDataHandler(sock, oName, kab):
    while True:
        namePrint(oName,DES.frombits(DES.decrypt(receiveMessage(sock),kab)))

"""
Generate pseudorandom number.
"""
def generate_nonce(length=8):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

"""
subtract one from the specified nonce
@param nonce: the nonce to subtract from
"""
def nonceSubtract(nonce):
    firstNonZeroIndex = -1
    for i in range(len(nonce)-1,-1,-1):
        if (nonce[i] != '0'):
            firstNonZeroIndex = i
            break
    if (firstNonZeroIndex == -1):
        return "1" * len(nonce)
    return nonce[:firstNonZeroIndex] + str(int(nonce[firstNonZeroIndex])-1) + nonce[firstNonZeroIndex+1:]

"""
receive a message from the specified connection, and strip byte encoding and stringification
@param conn: the connection on which to receive a message
"""
def receiveMessage(conn):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(conn, 4, True)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(conn, msglen)
    
"""
helper method for receiveMessage which reads the correct number of bytes
@param sock: the socket on which to read
@param n: number of bytes of size identifier
@param firstPass: whether we are running this to get the message size, or to get the messsage itself
"""
def recvall(sock, n, firstPass = False):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    if (firstPass):
        return data
    #print("received data:",data)
    return decoder.decode(data.decode("utf-8"))

"""
send a message to the specified connection, adding byte encoding and stringification
@param conn: the connection on which to send a message
@param msg: the message to send
"""
def sendMessage(conn,msg):
    sent = encoder.encode(msg).encode("utf-8")
    sent = struct.pack('>I', len(sent)) + sent
    #print("sent data:",sent)
    conn.sendall(sent)
   
"""
diffie-hellman implementation
@param conn: the socket connection to use for Ya/Yb exchange
@param meFirst: whether I should receive Yb before sending Ya during the exchange or vice versa
@param p: custom p-value
@param g: custom g-value
@returns: the calculated integer key value
""" 
def diffieHellman(conn, meFirst=True,p=13232376895198612407547930718267435757728527029623408872245156039757713029036368719146452186041204237350521785240337048752071462798273003935646236777459223,g=2):
    a = random.randint(0,1000000000)
    A = pow(g,a,p)
    print(A)
    if (meFirst):
        B = int(conn.recv(BUFFER_SIZE).decode("utf-8"))
        conn.send(str(A).encode("utf-8"))
    else:
        conn.send(str(A).encode("utf-8"))
        B = int(conn.recv(BUFFER_SIZE).decode("utf-8"))
    s = pow(B,a,p)
    return s
    #print(s)
    #return list(str(bin(s))[2:])

"""
diffie-hellman polynomial implementation
@param conn: the socket connection to use for Ya/Yb exchange
@param meFirst: whether I should receive Yb before sending Ya during the exchange or vice versa
"""
def diffieHellmanPoly(conn, meFirst = True):
    #hard-coded constants (you can change these if you want, but primpoly should stay degree 10)
    primPoly = sympy.Poly.from_list([1,0,0,0,0,0,0,0,0,1,1],gens=x)
    G = 100
    
    #randomly choose A and B -> construct polynomials
    Arand = random.randint(1,G)
    A = sympy.Poly.from_list([1]+[0]*Arand,gens=x)
    
    #apply modulo -> map to Galois field GF(2)
    Ya = GF((sympy.div(A,primPoly,domain='QQ')[1]))
    
    #exchange Ya and Yb
    #JSON won't encode a coefficient list from sympy for some reason, so manually reconstruct Yb
    if (meFirst):
        Yb = conn.recv(BUFFER_SIZE).decode('utf-8')
        Yb = sympy.Poly.from_list([int(Yb[i]) for i in range(2,len(Yb)-2,3)],gens=x)
        conn.send(encoder.encode(Ya.all_coeffs().__str__()).encode("utf-8"))
    else:
        conn.send(encoder.encode(Ya.all_coeffs().__str__()).encode("utf-8"))
        Yb = conn.recv(BUFFER_SIZE).decode('utf-8')
        Yb = sympy.Poly.from_list([int(Yb[i]) for i in range(2,len(Yb)-2,3)],gens=x)
        
    #apply modulo -> map to Galois field GF(2)
    Yba = GF(sympy.div(GF(Yb**Arand),primPoly,domain='QQ')[1])
    
    #convert poly to key 
    key = Yba.all_coeffs()
    key = [0] * (10-len(key)) + key
    
    return key
    
def main():
    subprocess.Popen("python KDC.py",creationflags=subprocess.CREATE_NEW_CONSOLE)
    time.sleep(2)
    subprocess.Popen("python Bob.py",creationflags=subprocess.CREATE_NEW_CONSOLE)
    time.sleep(2)
    subprocess.Popen("python Alice.py",creationflags=subprocess.CREATE_NEW_CONSOLE)
    
if __name__ == "__main__":
    main()