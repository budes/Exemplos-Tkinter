from tkinter import *

class Paint():
	print('Hello world 7')

	def __init__(self):
		
		#Instancia Tk
		self.inst = Tk()

		#Tela
		self.canvas = Canvas(self.inst, bg='lightgray')#, height=768, width=1024)
		self.canvas.pack()
		
		#Binding
		self.canvas.bind('<Button-1>', self.checkpos)
		self.p1, self.p2 = None, None
		
		
		#O mainloop
		self.inst.mainloop()
		
	def checkpos(self, event):
		# Se a posição inicial não foi definida
		if self.p1 == None:
			self.p1 = (self.canvas.winfo_pointerx()-self.canvas.winfo_rootx(), self.canvas.winfo_pointery()-self.canvas.winfo_rooty())
		
		# A partir do segundo toque	
		else:
			self.p2 = (self.canvas.winfo_pointerx()-self.canvas.winfo_rootx(), self.canvas.winfo_pointery()-self.canvas.winfo_rooty())
			self.canvas.create_line((self.p1[0], self.p1[1]), (self.p2[0], self.p2[1]), fill='black')
			
			self.p1 = self.p2
			self.p2 = None
		
	
if __name__ == '__main__':
	Paint()
