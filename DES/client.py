import sys,socket
from DES import encrypt, tobits, defaultKey

#boilerplate TCP code from https://wiki.python.org/moin/TcpCommunication
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 64000

fileName = input("Enter name of file to send to server: ")
#read file contents, erroring out if file does not exist
try:
    with open(fileName, 'r') as f:
        data = f.read()

except:
    print("Error: input file '{0}' not found".format(fileName),file=sys.stderr)
    sys.exit()
    
#establish socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

#encrypt data from file
bitArray = tobits(data)
result = encrypt(bitArray,defaultKey)
resultStr = ''.join(str(i) for i in result)
    
#send encrypted data to server
s.send(resultStr.encode())
s.close()