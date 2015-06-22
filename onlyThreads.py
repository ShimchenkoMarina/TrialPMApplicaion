import threading
import time
global stop_event

def MainFunction():
	
	#event for stop
	stop_event = threading.Event()

	#InitialThread
	initial_th = InitialThread(stop_event)
	
	#start it here
	initial_th.start()
	
	#end or wait
	#initial_th.join()
	print("Exiting main thread.")

class MyWindow:

  def __init__(self, _stop_event):
    self.stop_event = _stop_event

  def Show(self):
    time.sleep(5)
    self.OnQuit()

  def OnQuit(self):
    print("Hello, I'm a window!")
    input("close me: ")
    self.stop_event.set()


class InitialThread(threading.Thread):

  def __init__(self, _stop_event):
    threading.Thread.__init__(self)
    self.stop_event = _stop_event

  def run(self):
    print ("It is initial thread")
	#create a window
    my_win = MyWindow(self.stop_event)
    my_win.Show()
 
    #launch the computer
    computer = Computer(self.stop_event)
    computer.start()
 

    computer.join()
    
    print("Terminating the initial thread.")


class Computer(threading.Thread):

  def __init__(self, _stop_event):
    threading.Thread.__init__(self)
    self.stop_event = _stop_event

  def run(self):
    while not self.stop_event.is_set():
      print("Compute")
      #calculation process
      time.sleep(2)

    print("Terminating the computer.")

if __name__ == '__main__':
  MainFunction()
