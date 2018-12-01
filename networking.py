#my job is to store networking globals
import socket

inConn = outConn = None
outSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
securingConnection = False