import wx

def main(): 
    app = wx.App(redirect=True)
    top = wx.Frame(None, title="Hello World", size=(300,200))
    top.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()