from tkinter import *
from functools import partial
from PIL import Image, ImageTk 


class Calculadora():
	def __init__(self):
		
		# Coloquei a instancia Tk e o background
		self.inst = Tk()
		self.inst.geometry('720x1200')
		self.inst['background'] = 'white'
		
		# Fontes e imagens usadas
		fonte = ('Verdana', 12, 'bold')
		fontea = ('Verdana', 12)
		fonte2 = ('Verdana', 18, 'bold')
	
		# Vou colocar os calculos no Label
		self.calculo = Label(self.inst, text='', font=fonte2,
		bg='white', height=5)
		 
		self.calculo.pack()
		
		# Fiz desse jeito pq é mais rápido e simples
		Frames = [Frame(self.inst, bg='white', padx=0, pady=0) for cria in range(5)]
		
		# Empacota os Frames
		for empacotar in Frames: empacotar.pack()
		
		self.texto = (
		('C', '<×', '^', '/'),
		('7', '8', '9', 'x'),
		('4', '5', '6', '+'),
		('1', '2', '3', '-'),
		('.', '0', '()', '=')
		)
		
		# Cria os botoes na tela
		self.botoes = []
		
		for i in range(5):
			frame = Frames[i]
			for simbol in self.texto[i]:
				
				but = Button(frame, text=simbol, font=fontea, 
				height=2, width=3, relief=GROOVE, bg='white',
				command=partial(self.InterpretaBotoes, simbol)
				)
					
				but.pack(side=LEFT)
				self.botoes.append(but)
				
				# Muda a cor e a fonte do botão de acordo com o tipo
				
				if simbol in ('C', '<×', '^', '/', 'x', '+', '-'):
					but['bg'] = 'lightgray'
					but['fg'] = 'darkcyan'
					but['font'] = fonte
					
				elif simbol == '=':
					but['bg'] = 'green'
					but['fg'] = 'white'
					but['font'] = fonte
			
		
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
		elif valor == '()':
			texto = self.calculo['text']
			try:
				if texto[len(texto)-1] in '+-/^x' or len(texto) == 0:
					self.calculo['text'] += '('
					
				elif texto[len(texto)-1] in '1234567890)':
					self.calculo['text'] += ')'
					
			except:
				self.calculo['text'] += '('
			
		else:
			self.calculo['text'] += valor
			
		if len(self.calculo['text']) % 15 == 0:
			self.calculo['text'] += '\n'
		
	
	def Calcula(self):
		# Se tiver um dos operadores ele tenta fazer calculo
		if any([op in self.calculo['text'] for op in ['+', '-', '/', '^', 'x']]):
			calculo = ''
			for elemento in self.calculo['text']:
				for e in self.texto:
					if elemento == 'x':
						calculo += '*'
						break
						
					elif elemento == '^':
						calculo += '**'
						break
						
					elif elemento in '()':
						calculo += elemento
						break 
						
					elif elemento in e:
						calculo += elemento
						break
				
			self.calculo['text'] = ''
			resultado = str(eval(calculo))
			
			auxiliar = ''
			for i in range(len(resultado)):
				if (i+1) % 15 == 0:
					auxiliar += '\n'
					
				auxiliar += resultado[i]
			
			self.calculo['text'] = auxiliar
		
Calculadora()