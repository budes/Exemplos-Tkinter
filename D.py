from tkinter import *
from functools import partial

class Calculadora():
	def __init__(self):
		fonte = ('Verdana', 12, 'bold')
		fontea = ('Verdana', 12)
		
		fonte2 = ('Verdana', 18, 'bold')
		
		# Coloquei a instancia Tk e o background
		self.inst = Tk()
		self.inst.geometry('720x1200')
		self.inst['background'] = 'white'
	
		# Vou colocar os calculos no Label
		self.calculo = Label(self.inst, text='', font=fonte2,
		bg='white', height=5)
		 
		self.calculo.pack()
		
		# Fiz desse jeito pq é mais rápido e simples
		Frames = [Frame(self.inst, bg='white', padx=0, pady=0) for cria in range(5)]
		
		# Empacota os Frames
		for empacotar in Frames: empacotar.pack()
		
		self.texto = (
		('C', '<×', '**', '/'),
		('7', '8', '9', '*'),
		('4', '5', '6', '+'),
		('1', '2', '3', '-'),
		('.', '0', '÷', '=')
		)
		
		# Cria os botoes na tela
		botoes = []
		
		for i in range(5):
			frame = Frames[i]
			for simbol in self.texto[i]:
				but = Button(frame, text=simbol, font=fontea, 
				height=2, width=3, relief=GROOVE, bg='white',
				command=partial(self.InterpretaBotoes, simbol)
				)
				
				# Muda a cor e a fonte do botão de acordo com o tipo
				
				if simbol in ('C', '<×', '**', '/', '*', '+', '-'):
					but['bg'] = 'lightgray'
					but['fg'] = 'darkcyan'
					but['font'] = fonte
					
				elif simbol == '=':
					but['bg'] = 'green'
					but['fg'] = 'white'
					but['font'] = fonte
					
				
				but.pack(side=LEFT)
				botoes.append(but)
		
		# Inicia a instancia
		self.inst.mainloop()
		
	# Vai executar o comando do botão pressionado
	def InterpretaBotoes(self, valor):
		if valor == 'C':
			self.calculo['text'] = ''
		elif valor == '<×':
			self.calculo['text'] = self.calculo['text'][:len(self.calculo['text'])-1]
		elif valor == '=':
			self.Calcula()
		else:
			self.calculo['text'] += valor
			
		if len(self.calculo['text']) % 15 == 0:
			self.calculo['text'] += '\n'
		
	
	def Calcula(self):
		print(any([op in self.calculo['text'] for op in ['+', '-', '/', '**', '*']]))
		print([op in self.calculo['text'] for op in ['+', '-', '/', '**', '*']])
		
		# Se tiver um dos operadores ele tenta fazer calculo
		if any([op in self.calculo['text'] for op in ['+', '-', '/', '**', '*']]):
			calculo = ''
			for elemento in self.calculo['text']:
				for e in self.texto:
					if elemento in e:
						calculo += elemento
				
			calculo = eval(calculo)
			self.calculo['text'] = str(calculo)
			
		
		
Calculadora()