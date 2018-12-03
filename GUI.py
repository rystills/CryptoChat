import socket
import wx.lib.scrolledpanel
import main
import networking as net

#layouting constants
#TODO: magic numbers
winPadX = 16 #horizontal padding to fit content to window
winPadY = 65 #vertical padding to fit content to window

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
        menuSizer.Add(wx.StaticText(menubarPanel,-1,"ip",pos=(210,5)))
        self.ipField = wx.TextCtrl(menubarPanel,pos=(220,0),size=(100,menubarHeight-2))
        menuSizer.Add(wx.StaticText(menubarPanel,-1,"port",pos=(330,5)))
        self.portField = wx.TextCtrl(menubarPanel,pos=(352,0),size=(50,menubarHeight-2))
        menuSizer.Add(self.ipField, 0, wx.ALL, 5 ) 
        menuSizer.Add(wx.StaticText(menubarPanel,-1,"my ip/port: {0}/{1}".format(socket.gethostbyname(socket.gethostname()),net.inPort),pos=(412,5)))
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
            net.outIp = self.ipField.GetValue()
            net.outPort = int(self.portField.GetValue())
            if (main.connectToServer()):
                #TODO: move this message to after the connection is secured
                self.addInitMessage()
        if (btn == self.exitChatButton):
            if (main.disconnect()):
                self.addCloseMessage()
        
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
        if ((net.securingConnection) or not (net.inConn or net.outConn)):
            #nobody to send the message to
            return
        self.messageLogString.SetValue(self.messageLogString.GetValue() + ("\n"+'-'*148+"\nSent: " if self.messageLogString.GetValue() != "" else "Sent: ") + msg)
        self.scrollDown()
        main.sendMessage(msg)
    
    """
    return the correct newline string (clears the screen with -'s unless this is our first message)\
    @returns: the correct newline string
    """
    def newlineStr(self):
        return "\n"+'-'*148 if self.messageLogString.GetValue() != "" else ""
    
    """
    add the contents of a received message to the chat history box
    @param msg: the utf-8 encoded string message we received
    """
    def addReceivedMessage(self,msg):
        self.messageLogString.SetValue(self.messageLogString.GetValue() + self.newlineStr() + "\nReceived: " + msg)
        self.scrollDown()

    """
    add a message indicating to the user that we have disconnected from a chat
    """
    def addCloseMessage(self):
        if (self.messageLogString.GetValue()[-11:] != "Closed Chat"):
            self.messageLogString.SetValue(self.messageLogString.GetValue() + self.newlineStr() + "Closed Chat")
            self.scrollDown()
    
    """
    add a message indicating to the user that we have initiated a chat
    """
    def addInitMessage(self):
        self.messageLogString.SetValue(self.messageLogString.GetValue() + self.newlineStr() + "Initiated Chat; negotiating...")
        self.scrollDown()
        
    """
    add a message indicating that we have negotiated the chat, and are now securing
    """
    def addSecuringMessage(self):
        self.messageLogString.SetValue(self.messageLogString.GetValue() + self.newlineStr() + "Negotiation Complete; securing Channel...")
        self.scrollDown()
        
    """
    add a message indicating that we have secured the chat, and are ready to talk securely
    """
    def addChatReadyMessage(self):
        self.messageLogString.SetValue(self.messageLogString.GetValue() + self.newlineStr() + "Securing Complete; ready to chat!")
        self.scrollDown()
        
def start():
    app = wx.App()
    guiInstance = GUI(parent=None, title="CryptoChat",screenWidth = 640, screenHeight = 480)
    guiInstance.Show()
    net.gui = guiInstance
    app.MainLoop()