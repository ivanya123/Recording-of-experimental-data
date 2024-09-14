import tkinter
from tkinter import *

tkinter.Event

def event_info(event):
    print(type(event))
    print(event)
    print(event.time)
    print(event.x_root)
    print(event.y_root)


root = Tk()
root.bind('a', event_info)
root.mainloop()