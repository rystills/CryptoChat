#my job is to store networking globals (plus a reference to the GUI instance since all the threads talk to him)
import socket

inConn = outConn = None
outSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
securingConnection = False
BUFFER_SIZE = 4096
inPort = outPort = None
#TODO: set ip and port in GUI
inIp = '127.0.0.1'
outIp = '127.0.0.1'
gui = None