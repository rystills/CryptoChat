import wx.lib.scrolledpanel
import socket
import threading
import time
import sys
import types
import cryptoutil
import json; encoder = json.JSONEncoder(); decoder = json.JSONDecoder()
sys.path.insert(0, 'DES/'); import DES
sys.path.insert(0, 'NS_DH/'); import NS_DH
sys.path.insert(0, 'BG/'); import BG
sys.path.insert(0, 'Paillier/'); import Paillier
import networking as net

#TODO: stubbed pre-established preference
encryptionMode = "BG"

global frame
#layouting constants
#TODO: magic numbers
winPadX = 16 #horizontal padding to fit content to window
winPadY = 65 #vertical padding to fit content to window

#TODO: stubbed privKey/pubKey
#privKey,pubKey = Paillier.generate_keypair()
privKey = types.SimpleNamespace(l=139358136400596210796101638829470824320, m=77579141096015302651837419351184213921) 
pubKey = types.SimpleNamespace(n=139358136400596210820028512420294596809, nsq=19420690181047178617561734038854936171810222360568237602495984522839872982481)

"""
the GUI class defines all graphical components of our application, utilizing the WxPython library.
"""
class GUI(wx.Frame):
    """
    initialize the GUI, creating all graphical elements in vertical order
    @param parent: the Wx Frame to which this Frame belongs (set to None for this Frame to act as the root)
    @param id: a unique integer identifier for this Frame (set to -1 as we don't need to lookup this frame by id)
    @param title: the window title for this frame
    @param screenWidth: the desired width (in pixels) of the window
    @param screenHeight: the desired height (in pixels) of the window
    """
    def __init__(self,parent,title,screenWidth,screenHeight):
        #Create a fixed size frame
        wx.Frame.__init__(self,parent,-1,title,size=(screenWidth,screenHeight), style=(wx.DEFAULT_FRAME_STYLE) ^ (wx.RESIZE_BORDER|wx.MAXIMIZE_BOX))
        self.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL))
    
        #menubar panel
        menubarHeight = 28
        menubarPanel = wx.Panel(self,size=(screenWidth-winPadX,menubarHeight), pos=(0,0), style=wx.SIMPLE_BORDER)
        menubarPanel.SetBackgroundColour('#EEEEEE')
        menuSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.connectButton = wx.Button(menubarPanel,label="Start a New Chat",pos=(0,0),size=(100,menubarHeight-2))
        self.connectButton.Bind(wx.EVT_BUTTON,self.OnClicked)
        menuSizer.Add(self.connectButton, 0, wx.ALL, 5 )
        self.exitChatButton = wx.Button(menubarPanel,label="Exit Current Chat",pos=(99,0),size=(100,menubarHeight-2))
        self.exitChatButton.Bind(wx.EVT_BUTTON,self.OnClicked)
        menuSizer.Add(self.exitChatButton, 0, wx.ALL, 5 ) 
        menubarPanel.SetSizer(menuSizer)
        
        #main window panel
        self.contentPanel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(screenWidth-winPadX,screenHeight-winPadY), pos=(0,28), style=wx.SIMPLE_BORDER)
        self.contentPanel.SetupScrolling()
        self.contentPanel.SetBackgroundColour('#FFFFFF')
        #disable horizontal scrolling
        self.contentPanel.SetupScrolling(scroll_x=False)
        self.bSizer = wx.BoxSizer(wx.VERTICAL)
        #previous messages display field
        #TODO: magic number
        self.messageLogString = wx.TextCtrl(self.contentPanel,size=(screenWidth-winPadX-1,screenHeight-menubarHeight*2-100-winPadY+28),style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.bSizer.Add(self.messageLogString, 0, wx.ALL, 0) 
        
        #message input field
        self.msgField = wx.TextCtrl(self.contentPanel,size=(screenWidth-winPadX-1,100),style= wx.TE_MULTILINE | wx.SUNKEN_BORDER)
        self.bSizer.Add(self.msgField)
        #message send button
        self.sendBtn = wx.Button(self.contentPanel,label="Send Message",size=(90,menubarHeight-2))
        self.sendBtn.Bind(wx.EVT_BUTTON,self.OnClicked)
        self.bSizer.Add(self.sendBtn,0,wx.ALL,0)
        self.contentPanel.SetSizer(self.bSizer)
        
        #draw hacker skull and crossbones
        skull = wx.Bitmap('skull.png', wx.BITMAP_TYPE_PNG)
        control = wx.StaticBitmap(self, -1, skull)
        control.SetPosition((90,screenHeight-winPadY+1))
            
    """
    button click handler for all buttons in our GUI
    @param event: the event corresponding to this click; stores information about the object who triggered the event
    """
    def OnClicked(self, event): 
        btn = event.GetEventObject()
        if (btn == self.sendBtn and self.msgField.GetValue() != ""):
            self.sendMessage(self.msgField.GetValue())
            self.msgField.SetValue("")
        if (btn == self.connectButton):
            connectToServer()
        if (btn == self.exitChatButton):
            disconnect()
        
    """
    scroll to the bottom of the chat history window; called any time the chat history is updated
    """
    def scrollDown(self):
        self.messageLogString.ShowPosition(self.messageLogString.GetLastPosition())
        
    """
    send a message on whichever connection is currently open, and add the messsage to our chat history
    @param msg: the string message (not yet utf-8 encoded) to send
    """
    def sendMessage(self,msg):
        if (not (net.inConn or net.outConn)):
            #nobody to send the message to
            return
        self.messageLogString.SetValue(self.messageLogString.GetValue() + ("\n"+'-'*148+"\nSent: " if self.messageLogString.GetValue() != "" else "Sent: ") + msg)
        self.scrollDown()
        sendMessage(msg)
    
    """
    add the contents of a received message to the chat history box
    @param msg: the utf-8 encoded string message we received
    """
    def addReceivedMessage(self,msg):
        self.messageLogString.SetValue(self.messageLogString.GetValue() + ("\n"+'-'*148+"\nReceived: " if self.messageLogString.GetValue() != "" else "Received: ") + msg)
        self.scrollDown()

    """
    add a message indicating to the user that we have disconnected from a chat
    """
    def addCloseMessage(self):
        self.messageLogString.SetValue(self.messageLogString.GetValue() + ("\n"+'-'*148+"\nClosed Chat" if self.messageLogString.GetValue() != "" else "Closed Chat"))
        self.scrollDown()
    
    """
    add a message indicating to the user that we have connected to a chat
    """
    def addOpenMessage(self):
        self.messageLogString.SetValue(self.messageLogString.GetValue() + ("\n"+'-'*148+"\nInitiated Chat" if self.messageLogString.GetValue() != "" else "Initiated Chat"))
        self.scrollDown()

"""
send a message on whichever connection is currently open
@param msg: the string message (not yet utf-8 encoded) to send
"""
def sendMessage(msg):
    print("sending {0}".format(msg))
    if (net.inConn):
        print("sending on net.inConn")
        net.inConn.send(encryptMsg(msg).encode("utf-8"))
    elif (net.outConn):
        print("sending on net.outConn")
        net.outConn.send(encryptMsg(msg).encode("utf-8"))

"""
encrypt a msg using the current selected encryption algorithm
@param msg: the message to encrypt
@returns the encrypted message
"""
def encryptMsg(msg):
    if (encryptionMode == "DES"):
        encrypted = cryptoutil.frombits(DES.encrypt(cryptoutil.tobits(msg),DES.defaultKey))
    elif (encryptionMode == "BG"):
        bits,x = BG.BGPEnc(cryptoutil.tobits(msg))
        #encrypt a JSON encoded tuple of (c,x) where c is the stringified encrypted bit list and x is the t+1th iteration of the random seed exponentiation
        encrypted = encoder.encode((cryptoutil.frombits(bits),x))
    print("encrypting: {0} becomes: {1}".format(msg,encrypted))
    return encrypted

"""
decrypt a msg using the current selected encryption algorithm
@param msg: the message to decrypt
@returns the decrypted message
""" 
def decryptMsg(msg):
    if (encryptionMode == "DES"):
        decrypted = cryptoutil.frombits(DES.decrypt(cryptoutil.tobits(msg),DES.defaultKey))
    elif (encryptionMode == "BG"):
        bitsStr,x = decoder.decode(msg)
        decrypted = cryptoutil.frombits(BG.BGPDec(cryptoutil.tobits(bitsStr),x))
    print("decrypting: {0} becomes: {1}".format(msg,decrypted))
    return decrypted

"""
attempt to connect to the currently specified ip and port
"""
def connectToServer():
    if (net.outConn or net.inConn):
        print("Error: already engaged in a chat; please disconnect before establishing a new connection")
        return
    net.outSock.connect((net.outIp, net.outPort))
    print("established outgoing connection")
    frame.addOpenMessage()
    net.outConn = net.outSock
    secureConnection(False)
   
"""
disconnect from the currently active chat, if one exists
""" 
def disconnect():
    if (not (net.inConn or net.outConn)):
        #no connection from which to disconnect5
        return
    
    if (net.inConn):
        net.inConn.close()
        net.inConn = None
        print("disconnected net.inConn")

    if (net.outConn):
        net.outConn.close()
        net.outConn = None
        net.outSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("disconnected net.outConn")
        
    if (frame.messageLogString.GetValue()[-11:] != "Closed Chat"):
        frame.addCloseMessage()
    
"""
daemon thread who listens for messages while we have an active chat, and adds them to the chat history box
"""
def awaitMessages():
    while (True):
        #avoid a busyloop by only checking if we're in a connection once every 100ms
        time.sleep(.1)
        if (net.inConn or net.outConn):
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
                frame.addReceivedMessage(decryptMsg(data.decode("utf-8")))
            except:
                #received an error on conn recv - likely a disconnect was staged; disconnecting
                disconnect()
   
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
daemon thread who runs through securing the connection as the server
"""
def secureConnectionServer():
    #TODO: secure connection as server
    print("server secured connection")
    net.securingConnection = False
   
"""
daemon thread who runs through securing the connection as the client
""" 
def secureConnectionClient():
    #TODO: secure connection as client
    print("client secured connection")
    net.securingConnection = False
    
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
        if (net.outConn):
            #if we just received a connection but we're already chatting on net.outConn, drop the new connection immediately
            net.inConn.close()
            net.inConn = None
        else:
            frame.addOpenMessage()
            print("accepted incoming connection from net.inConn {0}\nnet.outConn {1}".format(net.inConn,addr))     
            secureConnection(True)

if __name__=='__main__':
    net.inPort = int(sys.argv[1]) if (len(sys.argv) > 1) else 5004
    net.outPort = int(sys.argv[2]) if (len(sys.argv) > 2) else 5005
    print("initializing with inPort {0} outPort {1}".format(net.inPort,net.outPort))
        
    global frame
    inConnThread = threading.Thread(target=awaitConnections, args=())
    inMsgThread = threading.Thread(target=awaitMessages, args=())
    inConnThread.setDaemon(True)
    inMsgThread.setDaemon(True)
    inConnThread.start()
    inMsgThread.start()
    app = wx.App()
    frame = GUI(parent=None, title="CryptoChat",screenWidth = 640, screenHeight = 480)
    frame.Show()
    app.MainLoop()