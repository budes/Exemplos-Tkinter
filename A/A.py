from tkinter import *
from random import choice

class BateBola(object):
    def __init__(self):

        # A instância Tk
        self.inst = Tk()

        self.fundo = PhotoImage(file='estrelas.gif')

        # Os dois widgets básicos
        self.canvas = Canvas(self.inst, bg='black', height=400, width=400)

        self.but = Button(self.inst, text='Jogar', command=self.iniciarjogo)

        # O empacotamento dos widgets
        self.canvas.pack()
        self.but.pack()

        # Tela não muda de tamanho
        self.inst.resizable(False, False),

        # O mainloop
        self.inst.mainloop()

    def iniciarjogo(self):
        # Pro botão
        self.but['text'] = 'Tentar de Novo'

        # Dá o focus no canvas
        self.canvas.focus_force()
        self.perdeu = False
        self.venceu = False

        # Para desenhar os widgets
        self.Desenhar()

        # Os bindings
        self.canvas.bind('<Motion>', self.movimento)

        # Cria os retângulos
        self.Pontos()

        # Começa a updatar
        self.update()

    def Desenhar(self):
        # Outros objetos
        self.idFund = self.canvas.create_image((200, 200), image=self.fundo)

        # Retângulo usado no game
        self.idRet = self.canvas.create_rectangle((160, 380), (240, 370), fill='white', outline='gray', width=2, tag='plataforma')
        self.posx = 200

        # Bola
        raio = 15
        self.modx = self.mody = 3
        self.idBol = self.canvas.create_oval((100-raio, 300+raio), (100+raio, 300-raio), fill='gray', width=2, outline='lightgray', tag='bola')

        # Os retangulos flutuantes
        self.ids = []

    def movimento(self, event):
        # Se o mouse estiver entre o ponto 400 e 0 do eixo x do canvas
        if event.x > 50 and event.x < 350:
            self.canvas.move('plataforma', event.x-self.posx, 0)
            self.posx += event.x-self.posx

    def update(self):
        if self.venceu:
            # Destroi tudo
            self.DestroiWidgets()

            # Coloca a mensagem no meio
            self.canvas.create_text((200, 200), text='VOCÊ GANHOU', fill='white')

            # Troca o texto do botão
            self.but['text'] = 'Jogar de novo?'

        if self.perdeu:
            # Destroi tudo
            self.DestroiWidgets()

            # Coloca a mensagem no meio
            self.canvas.create_text((200, 200), text='VOCÊ PERDEU', fill='white')

            # Troca o texto do botão
            self.but['text'] = 'Tentar de Novo'

        else:
            # Checa se venceu
            if len(self.ids) == 0:
                self.venceu = True

            else:
                # Ele checa as colisões para orientar a bola
                self.checa_colisao()
                self.canvas.move('bola', self.modx, self.mody)

                self.inst.after(10, self.update)

    def checa_colisao(self):
        # Ele obtém a posição da bola e tenta descobrir se ela está nas bordas
        # Se estiver, ele muda a direção pra qual ela acelera

        posbola = self.canvas.bbox('bola')
        posplat = self.canvas.bbox('plataforma')

        if posbola[1] <= 0 or posbola[3] <= 0:
            self.mody *= -1

        if posbola[0] > 400 or posbola[0] < 0 or posbola[2] > 400 or posbola[2] < 0:
            self.modx *= -1

        # Caso ela entre em colisão com a plataforma
        if posbola[3] >= 370 and (self.canvas.find_closest(posbola[2], posbola[3])[0] == self.idRet or self.canvas.find_closest(posbola[0], posbola[3])[0] == self.idRet):

            self.mody = -3

        # Colisão com os retângulos
        colisoes = [
        self.canvas.find_closest(posbola[0], posbola[1]),
        self.canvas.find_closest(posbola[2], posbola[1])
        ]
        # Ele olha os dois find closest e deleta o primeiro valor se estiver na lista de ids
        for c in colisoes:

            if c[0] in self.ids:
                self.mody *= -1
                self.ids.remove(c[0])
                self.canvas.delete(c[0])

                break

        # Checa se perdeu
        if posbola[1] > 400 or posbola[3] > 400:
            self.perdeu = True

    def Pontos(self):
        cores = ['green', 'orange', 'white', 'lightgray', 'yellow', 'purple']

        x = 400/8
        y_at = y = 120/5

        for c in range(5):
            cor = choice(cores)
            x_at = 0
            y_at += y

            for wid in range(8):
                x_at += x
                self.ids.append(self.canvas.create_rectangle((x_at, y_at+y), (x_at-x, y_at), width=4,fill=cor))

    def DestroiWidgets(self):
        # Destruindo cada um
        self.canvas.delete('plataforma')
        self.canvas.delete('bola')
        self.canvas.delete(self.idFund)

        for tijolo in self.ids:
            self.canvas.delete(tijolo)


BateBola()
