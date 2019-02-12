# Testing.py
# Used for testing concepts

from tkinter import *

win = Tk()
var = IntVar()

def callback():
    print(var.get())

def buttonCallback():
    print("Button Pressed! " + str(var.get()))

radio = Radiobutton(win, text="1", variable=var, value=1, command=callback)
radio2 = Radiobutton(win, text="2", variable=var, value=2, command=callback)

button = Button(win, text="Go", command=buttonCallback)

radio.pack()
radio2.pack()
button.pack()
win.mainloop()
