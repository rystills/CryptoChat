#I'll spawn two local chat instances ready to talk to each other

from subprocess import Popen, CREATE_NEW_CONSOLE

def main():
    Popen("python main.py 5004 5005",creationflags=CREATE_NEW_CONSOLE)
    Popen("python main.py 5005 5004",creationflags=CREATE_NEW_CONSOLE)
    
if __name__ == "__main__":
    main()