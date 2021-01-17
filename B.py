from tkinter import *
import winsound

# um somzinho com o pc

tk = Tk()

b = Button(tk)


def do(event): winsound.Beep(262, 1000)
def re(event): winsound.Beep(294, 1000)
def mi(event): winsound.Beep(330, 1000)
def fa(event): winsound.Beep(349, 1000)
def so(event): winsound.Beep(392, 1000)
def la(event): winsound.Beep(440, 1000)
def si(event): winsound.Beep(494, 1000)
def do2(event): winsound.Beep(523, 1000)


b.bind('<KeyPress-q>', do)
b.bind('<KeyPress-w>', re)
b.bind('<KeyPress-e>', mi)
b.bind('<KeyPress-r>', fa)
b.bind('<KeyPress-t>', so)
b.bind('<KeyPress-y>', la)
b.bind('<KeyPress-u>', si)
b.bind('<KeyPress-i>', do2)


b.focus_force()
b.pack()
tk.mainloop()
