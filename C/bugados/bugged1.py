from tkinter import *
from constantes import *
from sys import exit
from random import choice


# from functools import partial


class JogoDaCobrinha:
    def __init__(self):
        self.inst = Tk()
        self.inst.attributes('-fullscreen', True)

        # -- Constantes ou elementos especiais --
        self.jogando = False
        self.cobra = []

        fonte = ('Small Fonts', '15', 'bold')

        # -- Widgets --
        self.canvas = Canvas(self.inst, bg='black', width=LARGURA, height=ALTURA)
        self.canvas.pack()

        self.but = Button(self.inst, text='JOGAR', font=fonte, width=100, command=self.IniciarJogo, relief=GROOVE)
        self.but.pack()

        but_sair = Button(self.inst, text='SAIR', font=fonte, width=100, command=exit, relief=GROOVE)
        but_sair.pack()

        # -- Movimentação --

        self.modx = self.mody = 0

        self.vx = self.vy = 0

        self.canvas.bind('<Left>', self.esquerda)
        self.canvas.bind('<Right>', self.direita)
        self.canvas.bind('<Up>', self.cima)
        self.canvas.bind('<Down>', self.baixo)

        self.inst.mainloop()

    def esquerda(self, event):
        self.modx, self.mody = -VELOCIDADE, 0;
        self.VelocidadePlayer()

    def direita(self, event):
        self.modx, self.mody = VELOCIDADE, 0;
        self.VelocidadePlayer()

    def cima(self, event):
        self.modx, self.mody = 0, -VELOCIDADE;
        self.VelocidadePlayer()

    def baixo(self, event):
        self.modx, self.mody = 0, VELOCIDADE;
        self.VelocidadePlayer()

    def IniciarJogo(self):
        # -- Inicializa o game cheiroso --
        self.jogando = True

        self.cobra.append(
            [self.canvas.create_rectangle((X + 10, Y + 20), (X - 10, Y), fill='white', tag='player', outline='white'),
             0, 0])

        self.canvas.focus_force()
        self.CriaMacas()

        self.Update()

    def Update(self):
        # -- Atualiza as condições do jogo --
        if self.jogando:

            self.ChecaPontos()

            print(self.cobra)
            self.AtribuiVelocidade()

            for cobra in self.cobra:
                if cobra != self.cobra[0]:
                    self.MovimentaCorpo(cobra[0], cobra[1], cobra[2])
                else:
                    self.Movimenta()

            print(self.cobra)
            self.inst.after(100, self.Update)

    def VelocidadePlayer(self):
        # -- Muda a velocidade do player --
        self.cobra[0].pop(2)
        self.cobra[0].pop(1)

        self.cobra[0].insert(1, self.modx)
        self.cobra[0].insert(2, self.mody)

    def AtribuiVelocidade(self):
        # -- Atribui a velocidade pra cada membro da cobra --
        if len(self.cobra) > 1:
            for i_cobra in range(len(self.cobra) - 1, -1, -1):
                self.cobra[i_cobra].pop(2)
                self.cobra[i_cobra].pop(1)

                self.cobra[i_cobra].insert(1, self.cobra[i_cobra - 1][1])
                self.cobra[i_cobra].insert(2, self.cobra[i_cobra - 1][2])

    def CriaMacas(self):
        # -- Cria maçãs em cantos aleatórios --
        x = choice(range(0, LARGURA - 19, 20))
        y = choice(range(0, ALTURA - 19, 20))

        self.canvas.create_rectangle((x + 20, y + 20), (x, y), fill='red', tag='maça')

    def Movimenta(self):
        # -- Movimenta o personagem --
        self.canvas.move('player', self.modx, self.mody)

    def MovimentaCorpo(self, id, vx, vy):
        # -- Movimenta o corpo --
        self.canvas.move(id, vx, vy)

    def ChecaPontos(self):
        # -- Checa se fez colisão --
        colis_player = self.canvas.bbox('player')
        colis_ponta = self.canvas.bbox(self.cobra[len(self.cobra) - 1][0])
        colis_maca = self.canvas.bbox('maça')

        if colis_maca[:] == colis_player[:]:
            self.canvas.delete('maça')
            self.CriaMacas()

            self.cobra.append([self.canvas.create_rectangle((colis_ponta[0] - 20, colis_ponta[1] - 1),
                                                            (colis_ponta[2] - 20, colis_ponta[3]), outline='white',
                                                            fill='white'), 0, 0])


if __name__ == '__main__':
    JogoDaCobrinha()
