import wx, wx.lib.scrolledpanel
import socket
import threading
import time
import sys

global frame
#layouting constants
#TODO: magic numbers
winPadX = 16 #horizontal padding to fit content to window
winPadY = 65 #vertical padding to fit content to window

#networking vars
BUFFER_SIZE = 4096
#TODO: set ip and port in GUI
inIp = '127.0.0.1'
outIp = '127.0.0.1'
outPort = 5005
inPort = 5004
outSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
global inConn
global outConn
inConn = None
outConn = None

class GUI(wx.Frame):
    def __init__(self,parent,id,title,screenWidth,screenHeight):
        #Create a fixed size frame
        wx.Frame.__init__(self,parent,id,title,size=(screenWidth,screenHeight), style=(wx.DEFAULT_FRAME_STYLE) ^ (wx.RESIZE_BORDER|wx.MAXIMIZE_BOX))
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
    
    def OnClicked(self, event): 
        btn = event.GetEventObject()
        if (btn == self.sendBtn and self.msgField.GetValue() != ""):
            self.sendMessage(self.msgField.GetValue())
            self.msgField.SetValue("")
        if (btn == self.connectButton):
            connectToServer()
        
    def sendMessage(self,msg):
        self.messageLogString.SetValue(self.messageLogString.GetValue() + ("\n"+'-'*148+"\nSent: " if self.messageLogString.GetValue() != "" else "Sent: ") + msg)
        sendMessage(msg)
    
    def addReceivedMessage(self,msg):
        self.messageLogString.SetValue(self.messageLogString.GetValue() + ("\n"+'-'*148+"\nReceived: " if self.messageLogString.GetValue() != "" else "Received: ") + msg)

def sendMessage(msg):
    print("sending {0}".format(msg))
    if (inConn):
        print("sending on inConn")
        inConn.send(msg.encode("utf-8"))
    elif (outConn):
        print("sending on outConn")
        outConn.send(msg.encode("utf-8"))

def connectToServer():
    global outConn
    outSock.connect((outIp, outPort))
    print("established outgoing connection")
    outConn = outSock
    
def awaitMessages():
    global inConn
    global outConn
    while (True):
        if (not (inConn or outConn)):
            time.sleep(.1)
            continue
        print("awaiting inConn data")
        data = inConn.recv(BUFFER_SIZE) if inConn else outConn.recv(BUFFER_SIZE)
        print("data packet is: {0}".format(data))
        if (not data):
            if (inConn):
                inConn.close()
                inConn = None
            else:
                outConn.close()
                outConn = None
        frame.addReceivedMessage(data.decode("utf-8"))
        
def awaitConnections():
    inSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    inSock.bind((inIp, inPort))
    inSock.listen(1)
    global inConn
    while (True):
        if (inConn):
            time.sleep(.1)
            continue
        inConn, addr = inSock.accept()
        print("accepted incoming connection from inConn {0}\noutConn {1}".format(inConn,addr))            

if __name__=='__main__':
    if (len(sys.argv) > 1):
        inPort = int(sys.argv[1])
    if (len(sys.argv) > 2):
        outPort = int(sys.argv[2])
    print("initializing with inPort {0} outPort {1}".format(inPort,outPort))
        
    global frame
    threading.Thread(target=awaitConnections, args=()).start()
    threading.Thread(target=awaitMessages, args=()).start()
    app = wx.App()
    frame = GUI(parent=None, id=-1, title="CryptoChat",screenWidth = 640, screenHeight = 480)
    frame.Show()
    app.MainLoop()