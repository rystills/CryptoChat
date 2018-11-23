import socket
from DES import decrypt, frombits, defaultKey

#boilerplate TCP code from https://wiki.python.org/moin/TcpCommunication
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 64000

#establish socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

#accept connection
conn, addr = s.accept()
print('Connection address:', addr)

#await data
while 1:
    data = conn.recv(BUFFER_SIZE).decode()
    #store data in a list of bits
    data = [int(i) for i in list(data)]
    if not data: break
    print("Received data:\n", data)
    
    #decode and display data
    bitArray = [int(i) for i in list(data)]
    result = frombits(decrypt(bitArray, defaultKey))
    print("Decrypted data:\n{0}".format(result))
    
conn.close()