import ctypes
import sys
import threading
import gc

from user_interface.joy_user_interface import UI
from io_operator.joy_offset_rewriter import read_joystick
from io_operator.joy_rw_config import read_config

gc.enable()

class vars:       
    def __init__(self):
        self.axis = [0, 0, 0, 0, 0, 0]
        self.new_axis = [0, 0, 0, 0, 0, 0]
        self.config = read_config() 
        self.joy_id = self.config['usages']['joy_id']
        self.msg = ''
        self.ReadInput = True
        self.KeepMain = True
        self.first_time = True 
        self.threads = []
        
        
    def kill_tasks_force(self):
        self.threads = None
        
        gc.collect(generation=2)
        sys.exit(0)
        
            
        
def main():
    s1 = vars()

    s1.threads.append(threading.Thread(target=read_joystick, args=(s1, )))
    s1.threads[0].daemon = True
    s1.threads[0].start()
    
    s1.threads.append(threading.Thread(target=UI, args=(s1, )))
    s1.threads[1].daemon = True
    s1.threads[1].start()
    s1.threads[1].join()
    
   
if __name__ == "__main__":
    myappid = 'Suundumused.Joy Offset.Joy Offset.1' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    main()