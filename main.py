import wx, wx.lib.scrolledpanel
#layouting constants
winPadX = 16 #horizontal padding to fit content to window
winPadY = 65 #vertical padding to fit content to window
msgPadY = 8 #num vertical pixels between message strings

class GUI(wx.Frame):
    def __init__(self,parent,id,title,screenWidth,screenHeight):
        #Create a fixed size frame
        wx.Frame.__init__(self,parent,id,title,size=(screenWidth,screenHeight), style=(wx.DEFAULT_FRAME_STYLE) ^ (wx.RESIZE_BORDER|wx.MAXIMIZE_BOX))
    
        #menubar panel
        menubarHeight = 28
        menubarPanel = wx.Panel(self,size=(screenWidth-winPadX,menubarHeight), pos=(0,0), style=wx.SIMPLE_BORDER)
        menubarPanel.SetBackgroundColour('#EEEEEE')
        menuSizer = wx.BoxSizer(wx.HORIZONTAL)
        menuSizer.Add(wx.Button(menubarPanel,label="Start a New Chat",pos=(0,0),size=(100,menubarHeight-2)), 0, wx.ALL, 5 )
        menuSizer.Add(wx.Button(menubarPanel,label="Exit Current Chat",pos=(99,0),size=(100,menubarHeight-2)), 0, wx.ALL, 5 ) 
        menubarPanel.SetSizer(menuSizer)
        
        #main window panel
        self.contentPanel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(screenWidth-winPadX,screenHeight-winPadY), pos=(0,28), style=wx.SIMPLE_BORDER)
        self.contentPanel.SetupScrolling()
        self.contentPanel.SetBackgroundColour('#FFFFFF')
        #disable horizontal scrolling
        self.contentPanel.SetupScrolling(scroll_x=False)
        
        #test scrollbar by adding a bunch of "message" strings
        self.bSizer = wx.BoxSizer(wx.VERTICAL)
        self.messageLogString = wx.StaticText(self.contentPanel,label="")
        self.bSizer.Add(self.messageLogString, 0, wx.ALL, msgPadY) 
        self.contentPanel.SetSizer(self.bSizer)
        
        #TODO: this stuff should go in its own panel below
        #message input field
        self.msgField = wx.TextCtrl(self.contentPanel,size=(screenWidth-2*winPadX-2,100),style= wx.TE_MULTILINE | wx.SUNKEN_BORDER)
        self.bSizer.Add(self.msgField)
        self.sendBtn = wx.Button(self.contentPanel,label="Send Message",size=(86,menubarHeight-2))
        self.sendBtn.Bind(wx.EVT_BUTTON,self.OnClicked)
        self.bSizer.Add(self.sendBtn,0,wx.ALL,0)
    
    def OnClicked(self, event): 
        btn = event.GetEventObject()
        if (btn == self.sendBtn and self.msgField.GetValue() != ""):
            self.sendMessage(self.msgField.GetValue())
            self.msgField.SetValue("")
        
    def sendMessage(self,msg):
        self.messageLogString.Label = self.messageLogString.Label + "\n" + msg

if __name__=='__main__':
    app = wx.App()
    frame = GUI(parent=None, id=-1, title="CryptoChat",screenWidth = 640, screenHeight = 480)
    frame.Show()
    app.MainLoop()