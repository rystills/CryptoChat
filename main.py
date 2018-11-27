import wx, wx.lib.scrolledpanel
winPadX = 16 #horizontal padding to fit content to window
winPadY = 65 #vertical padding to fit content to window

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
        contentPanel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(screenWidth-winPadX,screenHeight-winPadY), pos=(0,28), style=wx.SIMPLE_BORDER)
        contentPanel.SetupScrolling()
        contentPanel.SetBackgroundColour('#FFFFFF')

        #test scrollbar by adding a bunch of buttons   
        bSizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(8):
            bSizer.Add(wx.Button(contentPanel,label="Button {0}".format(i+1),pos=(0,50*(i+1)),size=(50,50)), 0, wx.ALL, 5 ) 
        contentPanel.SetSizer(bSizer)

if __name__=='__main__':
    app = wx.App()
    frame = GUI(parent=None, id=-1, title="CryptoChat",screenWidth = 640, screenHeight = 480)
    frame.Show()
    app.MainLoop()