import socket
import threading
import time
import sys
import types
import random
import cryptoutil
import json; encoder = json.JSONEncoder(); decoder = json.JSONDecoder()
from DES import DES
from NS_DH import NS_DH
from BG import BG
from Paillier import Paillier
from AES import AES
import GUI
import networking as net

#TODO: stubbed pre-established preference
global PKCPref #preference for establishing a secure connection (distributing keys)
global encPref #preference for message encryption/decryption
PKCPref = "NS_DH"
encPref = "Paillier"

#TODO: stubbed privKey/pubKey
#privKey,pubKey = Paillier.generate_keypair()
#privKey = types.SimpleNamespace(l=139358136400596210796101638829470824320, m=77579141096015302651837419351184213921) 
#pubKey = types.SimpleNamespace(n=139358136400596210820028512420294596809, nsq=19420690181047178617561734038854936171810222360568237602495984522839872982481)
global privKey
global pubKey

"""
send a message on whichever connection is currently open
@param msg: the string message (not yet utf-8 encoded) to send
"""
def sendMessage(msg,shouldEncrypt=True):
    print("sending {0}".format(msg))
    if (net.inConn):
        print("sending on net.inConn")
        net.inConn.send((encryptMsg(msg) if shouldEncrypt else msg).encode("utf-8"))
    elif (net.outConn):
        print("sending on net.outConn")
        net.outConn.send((encryptMsg(msg) if shouldEncrypt else msg).encode("utf-8"))

"""
encrypt a msg using the current selected encryption algorithm
@param msg: the message to encrypt
@returns the encrypted message
"""
def encryptMsg(msg):
    if (encPref == "DES"):
        encrypted = cryptoutil.frombits(DES.encrypt(cryptoutil.tobits(msg),DES.defaultKey))
    elif (encPref == "BG"):
        bits,x = BG.BGPEnc(cryptoutil.tobits(msg),privKey.l,privKey.m)
        #encrypt a JSON encoded tuple of (c,x) where c is the stringified encrypted bit list and x is the t+1th iteration of the random seed exponentiation
        encrypted = encoder.encode((cryptoutil.frombits(bits),x))
    elif (encPref == "Paillier"):
        #encrypt a JSON encoded list of encrypted segments of 12 characters each (converted to ascii)
        encrypted = encoder.encode([str(Paillier.encrypt(pubKey,cryptoutil.strToAsciiInt(msg[i:i+12]))) for i in range(0,len(msg),12)])
    print("encrypting: {0} becomes: {1}".format(msg,encrypted))
    return encrypted

"""
decrypt a msg using the current selected encryption algorithm
@param msg: the message to decrypt
@returns the decrypted message
""" 
def decryptMsg(msg):
    if (encPref == "DES"):
        decrypted = cryptoutil.frombits(DES.decrypt(cryptoutil.tobits(msg),DES.defaultKey))
    elif (encPref == "BG"):
        bitsStr,x = decoder.decode(msg)
        decrypted = cryptoutil.frombits(BG.BGPDec(cryptoutil.tobits(bitsStr),x,privKey.l,privKey.m))
    elif (encPref == "Paillier"):
        msg = decoder.decode(msg)
        decrypted = ''.join([cryptoutil.asciiIntToStr(Paillier.decrypt(privKey,pubKey,int(i))) for i in msg])
    print("decrypting: {0} becomes: {1}".format(msg,decrypted))
    return decrypted

"""
attempt to connect to the currently specified ip and port
@returns: whether or not we initiated a new connection
"""
def connectToServer():
    if (net.outConn or net.inConn):
        print("Error: already engaged in a chat; please disconnect before establishing a new connection")
        return False
    net.outSock.connect((net.outIp, net.outPort))
    print("established outgoing connection")
    net.outConn = net.outSock
    secureConnection(False)
    return True
   
"""
disconnect from the currently active chat, if one exists
@returns: whether or not we disconnected from a connection
""" 
def disconnect():
    if (not (net.inConn or net.outConn)):
        #no connection from which to disconnect5
        return False
    
    if (net.inConn):
        net.inConn.close()
        net.inConn = None
        print("disconnected net.inConn")

    if (net.outConn):
        net.outConn.close()
        net.outConn = None
        net.outSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("disconnected net.outConn")  
    return True
   
"""
secure the current connection, negotiating and establishing a secure channel. Must complete before chat messages may be sent/recvd.
@param amServer: whether we are acting as the server (true) or the client (false) in this instance
"""
def secureConnection(amServer):
    net.securingConnection = True
    print("securing connection as {0}".format("server" if amServer else "client"))
    secureConnectionThread = threading.Thread(target=secureConnectionServer if amServer else secureConnectionClient, args=())
    secureConnectionThread.setDaemon(True)
    secureConnectionThread.start()
    
"""
daemon thread who runs through securing the connection as the server (person who received connection request)
"""
def secureConnectionServer():
    #negotiation
    global PKCPref
    global encPref
    global privKey
    global pubKey
    data = net.inConn.recv(net.BUFFER_SIZE).decode("utf-8")
    print("received preference packet is: {0}".format(data))
    data = data.split(" ")
    #TODO: don't assume we have the same preference + version
    PKCPref = data[1]
    encPref = data[2]
    sendMessage("Hello2 {0} {1}".format(PKCPref,encPref),False)
    print("~PREFERENCES~\n{0} {1}".format(PKCPref,encPref))
    data = net.inConn.recv(net.BUFFER_SIZE).decode("utf-8")
    if (data[:9] != "Hello ACK"):
        disconnect()
        net.securingConnection = False
    
    net.gui.addSecuringMessage()
    #establishing a secure channel
    if (PKCPref == "RSA"):
        pass
    elif (PKCPref == "NS_DH"):
        privKey = NS_DH.diffieHellman(net.inConn,False)
        print(privKey)
    #generate additional private / public key data required by the preferred encryption cipher
    random.seed(privKey)
    if (encPref == "Paillier"):
        privKey,pubKey = Paillier.generate_keypair()
    
    print("server secured connection")
    net.securingConnection = False
    net.gui.addChatReadyMessage()
   
"""
daemon thread who runs through securing the connection as the client (person who sent connection request)
""" 
def secureConnectionClient():
    #negotiation
    global PKCPref
    global encPref
    global privKey
    global pubKey
    sendMessage("Hello {0} {1}".format(PKCPref,encPref),False)
    data = net.outConn.recv(net.BUFFER_SIZE).decode("utf-8")
    if (data[:6] != "Hello2"):
        disconnect()
        net.securingConnection = False
        return
    data = data.split(" ")
    PKCPref = data[1]
    encPref = data[2]
    sendMessage("Hello ACK",False)
    print("~PREFERENCES~\n{0} {1}".format(PKCPref,encPref))
    
    net.gui.addSecuringMessage()
    #establishing a secure channel
    if (PKCPref == "RSA"):
        pass
    elif (PKCPref == "NS_DH"):
        privKey = NS_DH.diffieHellman(net.outConn,True)
        print(privKey)
    #generate additional private / public key data required by the preferred encryption cipher
    random.seed(privKey)
    if (encPref == "Paillier"):
        privKey,pubKey = Paillier.generate_keypair()
    
    print("client secured connection")
    net.securingConnection = False
    net.gui.addChatReadyMessage()
    
"""
daemon thread who listens for messages while we have an active chat, and adds them to the chat history box
"""
def awaitMessages():
    while (True):
        #avoid a busyloop by only checking if we're in an established connection once every 100ms
        time.sleep(.1)
        if ((not net.securingConnection) and (net.inConn or net.outConn)):
            print("awaiting {0} data".format("net.inConn" if net.inConn else "net.outConn"))
            try:
                data = net.inConn.recv(net.BUFFER_SIZE) if net.inConn else net.outConn.recv(net.BUFFER_SIZE)
                print("data packet received is: {0}".format(data))
                if (not data):
                    if (net.inConn):
                        net.inConn.close()
                        net.inConn = None
                    else:
                        net.outConn.close()
                        net.outConn = None
                net.gui.addReceivedMessage(decryptMsg(data.decode("utf-8")))
            except:
                #received an error on conn recv - likely a disconnect was staged; disconnecting
                if (disconnect()):
                    net.gui.addCloseMessage()
    
"""
daemon thread who listens for incoming connections, accepting them if we are not currently in a chat
"""     
def awaitConnections():
    inSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    inSock.bind((net.inIp, net.inPort))
    inSock.listen(1)
    while (True):
        #avoid a busyloop by only checking if we're in a connection once every 100ms
        if (net.inConn or net.outConn):
            time.sleep(.1)
            continue
        net.inConn, addr = inSock.accept()
        '''if (net.outConn):
            #if we just received a connection but we're already chatting on net.outConn, drop the new connection immediately
            net.inConn.close()
            net.inConn = None
        else:'''
        net.gui.addInitMessage()
        print("accepted incoming connection from net.inConn {0}\nnet.outConn {1}".format(net.inConn,addr))     
        secureConnection(True)

if __name__=='__main__':
    net.inPort = int(sys.argv[1]) if (len(sys.argv) > 1) else 5004
    net.outPort = int(sys.argv[2]) if (len(sys.argv) > 2) else 5005
    print("initializing with inPort {0} outPort {1}".format(net.inPort,net.outPort))
    #networked threads are essentially daemons bound to the GUI; once the window is closed or an event generates a critical error, all will die
    inConnThread = threading.Thread(target=awaitConnections, args=())
    inMsgThread = threading.Thread(target=awaitMessages, args=())
    inConnThread.setDaemon(True)
    inMsgThread.setDaemon(True)
    inConnThread.start()
    inMsgThread.start()
    GUI.start()