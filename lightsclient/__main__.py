import sys
from ctypes import cdll, byref, create_string_buffer
from lightsclient.interface import Interface

def main(args=None):
    
    """Set process name"""
    name = "Lights Client"
    length = len(name)
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(length+1)
    buff.value = bytes(name, 'utf8')
    libc.prctl(15, byref(buff), 0, 0, 0)
    
    """Main routine"""
    if args is None:
        args = sys.argv[1:]
        
    print("Starting")
    
    i = Interface()
    songPath = i.getInput()
    song = i.parseFiles(songPath)
    
    sys.exit(0)
    
if __name__ == "__main__":
    main()