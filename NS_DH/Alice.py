from main import generate_nonce, nonceSubtract, diffieHellman, encoder, decoder, sendMessage, receiveMessage, namePrint, chatDataHandler
import sympy, random, sys, threading
try: import simplejson as json
except ImportError: import json
sys.path.insert(0, 'DES/'); import DES
import socket

def main():
    TCP_IP = '127.0.0.1'
    SERV_PORT = 5005
    BOB_PORT = 5004
    ALICE_PORT = 5003
    BUFFER_SIZE = 4096
    
    #connect to KDC to establish aliceKey
    servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servSock.connect((TCP_IP, SERV_PORT))
    #clients are aware of each others' usernames
    alice = "Alice"
    bob = "Bob"
    servSock.send(alice.encode("utf-8"))
    aliceKey = diffieHellman(servSock, False)
    aliceNonce = generate_nonce()
    namePrint(alice,"aliceKey established with server as " + str(aliceKey))
    
    #connect to Bob to start exchanging information
    bobSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bobSock.connect((TCP_IP, BOB_PORT))
    
    #1. Alice sends a request to Bob
    namePrint(alice,"step 1: request to Bob")
    msg = [alice]
    sendMessage(bobSock,msg)
    
    #3. Alice sends a message to the server identifying herself and Bob, telling the server she wants to communicate with Bob.
    namePrint(alice,"step 3: request to Server")
    encryptedMsg = receiveMessage(bobSock)
    msg = [alice, bob, aliceNonce, encryptedMsg]
    sendMessage(servSock, msg)
    
    #5. Alice forwards the key to Bob who can decrypt it with the key he shares with the server, thus authenticating the data.
    namePrint(alice,"step 5: pass Server response to Bob")
    encryptedNewMsg = receiveMessage(servSock)
    decryptedServerMsg = DES.frombits(DES.decrypt(encryptedNewMsg,aliceKey))
    serverMsg = decoder.decode(decryptedServerMsg)
    aliceKab = serverMsg[2]
    toBob = serverMsg[3]
    sendMessage(bobSock, toBob)
    
    #7. Alice performs a simple operation on the nonce, re-encrypts it and sends it back verifying that she is still alive and that she holds the key.
    namePrint(alice,"step 7: send nonce operation result to Bob")
    encryptedNewMsg = receiveMessage(bobSock)
    decryptedBobMsg = DES.frombits(DES.decrypt(encryptedNewMsg,aliceKab))
    decryptedBob = decoder.decode(decryptedBobMsg)
    newMsg = [nonceSubtract(decryptedBob[0])]
    encryptedNewMsg = DES.encrypt(DES.tobits(encoder.encode(newMsg)),aliceKab)
    sendMessage(bobSock, encryptedNewMsg)
    
    #time too chat!
    namePrint(alice,"Success! Time to chat!")
    threading.Thread(target=chatDataHandler, args = (bobSock, bob, aliceKab)).start()
    while (True):
        sendMessage(bobSock,DES.encrypt(DES.tobits(encoder.encode(input(""))),aliceKab))

if __name__ == "__main__":
    main()