# from Projetos.C.constantes import LARGURA_PIXEL
from random import choice
from sys import exit
import shelve
from tkinter import *

# Muda para o diretório onde o script está, para previnir problemas
from constantes import *


class JogoDaCobrinha:
    def __init__(self):
        self.arq = shelve.open('data', 'c')
        self.inst = Tk()
        self.inst.attributes('-fullscreen', True)

        # -- Elementos especiais e fontes --
        # self.IniciaElementos()
        # PS: Eu defini dnv, mesmo tendo o método pra isso, pq o PyCharm fica mostrando warning
        # warning incomoda muito, mas se quiser apagar e só colocar o self.IniciaElementos() é de boas
        self.jogando = False
        self.cobra = []
        self.lado = None
        self.colis_face = None
        self.pontos = 0
        self.tick = 75
        self.obstaculos = []

        fonte = ('Small Fonts', '15', 'bold')
        self.font = ('Small Fonts', '30', 'bold')

        # -- Widgets --
        self.canvas = Canvas(self.inst, bg='black', width=LARGURA, height=ALTURA)
        self.canvas.pack()

        self.canvas.create_text((X, Y), text='A lenda da cobra Juvenildo', font=self.font, fill='white', tag='LOG')
        self.canvas.create_text((X, Y + 50), text=f'RECORDE: {self.arq["recorde"]}', font=self.font, fill='white',
                                tag='LOG')

        self.but = Button(self.inst, text='JOGAR', font=fonte, width=100, command=self.IniciarJogo, relief=GROOVE)
        self.but.pack()

        but_sair = Button(self.inst, text='SAIR', font=fonte, width=100, command=self.SairJogo, relief=GROOVE)
        but_sair.pack()

        # -- Movimentação --
        self.modx = self.mody = 0

        self.vx = self.vy = 0

        self.canvas.bind('<Left>', self.esquerda)
        self.canvas.bind('<Right>', self.direita)
        self.canvas.bind('<Up>', self.cima)
        self.canvas.bind('<Down>', self.baixo)

        self.inst.mainloop()

    # -- Inicia e termina o jogo --

    def IniciarJogo(self):
        # -- Inicializa o game cheiroso --
        self.jogando = True

        self.but['text'] = ''
        self.but['command'] = lambda: None

        self.canvas.itemconfig('LOG', text='')

        if X % 20 == 0:
            coord = (X + LARGURA_PIXEL, Y + LARGURA_PIXEL), (X, Y)
        elif Y % 20 == 0:
            coord = (X + 10, Y + 20), (X - 10, Y)
        else:
            coord = (X + 10, Y + 10), (X - 10, Y - 10)

        self.cobra.append(
            [self.canvas.create_rectangle(coord, fill='green', outline='darkgreen', tag='player'),
             0, 0, self.lado])

        self.canvas.focus_force()
        self.CriaMacas()

        self.Update()

    def SairJogo(self):
        # -- Sai do Jogo -- 
        self.arq.close()
        return exit()

    # -- Método principal --

    def Update(self):
        # -- Atualiza as condições do jogo --
        if self.jogando:

            for cobra in self.cobra:
                if cobra != self.cobra[0][0]:
                    self.MovimentaCorpo(cobra[0], cobra[1], cobra[2])
                else:
                    self.Movimenta()

            self.but['text'] = f'Pontos: {self.pontos}'

            self.AtribuiVelocidade()
            self.VelocidadePlayer()
            self.ChecaDirecao()
            self.ChecaPontos()

            #self.pontos = 10
            if len(self.obstaculos) < self.pontos // 10:
                self.GeraObstaculos()

            self.inst.after(self.tick, self.Update)

        else:
            # -- Deleta tudo e bota a mensagem 'VOCÊ PERDEU !!!' --
            if self.pontos > self.arq['recorde']:
                self.arq['recorde'] = self.pontos

            self.DeletaTudo()
            self.IniciaElementos()

            self.canvas.create_text((X, Y), text='VOCÊ PERDEU!!!', font=self.font, fill='white', tag='LOG')
            self.canvas.create_text((X, Y + 50), text=f'RECORDE: {self.arq["recorde"]}', font=self.font, fill='white',
                                    tag='LOG')

            self.but['text'] = 'Reiniciar Jogo?'
            self.but['command'] = self.IniciarJogo

    # -- Métodos responsáveis pela maior parte do jogo -- 

    def VelocidadePlayer(self):
        # -- Muda a velocidade do player --
        self.cobra[0].pop(2)
        self.cobra[0].pop(1)

        self.cobra[0].insert(1, self.modx)
        self.cobra[0].insert(2, self.mody)

    def AtribuiVelocidade(self):
        # -- Atribui a velocidade pra cada membro da cobra --
        if len(self.cobra) > 1:
            for i_cobra in range(len(self.cobra) - 1, 0, -1):
                self.cobra[i_cobra].pop(2)
                self.cobra[i_cobra].pop(1)

                self.cobra[i_cobra].insert(1, self.cobra[i_cobra - 1][1])
                self.cobra[i_cobra].insert(2, self.cobra[i_cobra - 1][2])

    def CriaMacas(self):
        # -- Cria maçãs em cantos aleatórios --
        x = choice(range(0, LARGURA - LARGURA_PIXEL + 1, LARGURA_PIXEL))
        y = choice(range(0, ALTURA - LARGURA_PIXEL + 1, LARGURA_PIXEL))

        self.canvas.create_rectangle((x + LARGURA_PIXEL, y + LARGURA_PIXEL), (x, y), fill='red', outline='brown',
                                     tag='maça')

    def ChecaPontos(self):
        # -- Checa se fez colisão --
        colis_player = self.canvas.bbox('player')
        colis_ponta = self.canvas.bbox(self.cobra[len(self.cobra) - 1][0])
        colis_maca = self.canvas.bbox('maça')

        if colis_maca[:] == colis_player[:]:
            self.canvas.delete('maça')
            self.pontos += 10
            self.CriaMacas()

            self.cobra.append([self.canvas.create_rectangle((colis_ponta[0] + 1, colis_ponta[1] + 1),
                                                            (colis_ponta[2] - 1, colis_ponta[3] - 1),
                                                            outline='darkgreen', fill='green'), 0, 0])

            if self.tick > TICK_MIN:
                self.tick -= SUB

        elif colis_player[0] + 10 <= 0 or colis_player[2] - 10 >= LARGURA or colis_player[1] + 10 >= ALTURA or \
                colis_player[3] - 10 <= 0:
            self.jogando = False

        if self.colis_face is not None:
            colisoes = self.canvas.find_overlapping(self.colis_face[0][0], self.colis_face[0][1], self.colis_face[1][0],
                                                    self.colis_face[1][1])
            if len(colisoes) >= 1:
                if colisoes[0] != 'player':
                    for c in self.cobra:
                        if c[0] in colisoes:
                            self.jogando = False

                    for c in self.obstaculos:
                        if c in colisoes:
                            self.jogando = False

    def ChecaDirecao(self):
        # -- Muda a direção da carinha e adapta a colisão --
        coord = self.canvas.bbox('player')

        if self.lado is not None:
            self.canvas.delete('olhos')

        if self.lado == 'D':
            for direcao in DIREITA: eval(direcao)
            self.colis_face = ((coord[2], coord[1] + 5), (coord[2], coord[3] - 5))
        if self.lado == 'E':
            for direcao in ESQUERDA: eval(direcao)
            self.colis_face = ((coord[0], coord[1] + 5), (coord[0], coord[3] - 5))
        if self.lado == 'C':
            for direcao in CIMA: eval(direcao)
            self.colis_face = ((coord[0] + 5, coord[1]), (coord[2] - 5, coord[1]))
        if self.lado == 'B':
            for direcao in BAIXO: eval(direcao)
            self.colis_face = ((coord[0] + 5, coord[3]), (coord[2] - 5, coord[3]))

    def GeraObstaculos(self):
        # -- Gera determinados obstaculos dentro do jogo --
        while True:
            #borda = True  # choice(range(2))
            coord = []

            lado = choice(range(2))
            sublado = None

            # Cima e baixo
            if lado == 0:
                sublado = baixo = choice(range(2))
                for c in range(4):
                    if c % 2 == 0 and c > 0:
                        coord.append(coord[0] + LARGURA_PIXEL)
                    elif c % 2 == 0 and c == 0:
                        coord.append(choice(range(LARGURA_PIXEL * 3, LARGURA - LARGURA_PIXEL * 3, LARGURA_PIXEL)))

                    elif c % 2 != 0 and c != 1:
                        if baixo == 0:
                            coord.append(choice(range(LARGURA_PIXEL * 3, LARGURA_PIXEL * 4, LARGURA_PIXEL)))
                        else:
                            coord.append(choice(range(ALTURA - LARGURA_PIXEL * 3,  LARGURA_PIXEL * 4, -LARGURA_PIXEL)))

                    else:
                        coord.append(ALTURA*baixo)

            #print(coord)

            # Esquerda e direita
            if lado == 1:
                sublado = direita = choice(range(2))
                for c in range(4):
                    if c % 2 != 0 and c > 1:
                        coord.append(coord[1] + LARGURA_PIXEL)
                    elif c % 2 != 0 and c == 1:
                        coord.append(choice(range(LARGURA_PIXEL * 3, ALTURA - LARGURA_PIXEL * 3, LARGURA_PIXEL)))

                    elif c % 2 == 0 and c != 0:
                        if direita == 0:
                            coord.append(choice(range(LARGURA_PIXEL * 3, LARGURA - LARGURA_PIXEL * 4, LARGURA_PIXEL)))
                        else:
                            coord.append(choice(range(LARGURA - LARGURA_PIXEL * 3, LARGURA_PIXEL * 4, -LARGURA_PIXEL)))

                    else:
                        coord.append(LARGURA*direita)

            print(coord)
            if self.ChecaObstaculos(coord, lado, sublado):
                self.obstaculos.append(self.canvas.create_rectangle(coord, fill='lightgray'))
                break

    def ChecaObstaculos(self, coord:list, lado:int, sublado:int):
        # -- Checa se pode criar o obstáculo --

        colisoes = [[self.canvas.bbox(elementos[0]) for elementos in self.cobra], self.canvas.bbox('maca'),
                    [self.canvas.bbox(elementos) for elementos in self.obstaculos]]

        permissao = True
        if (0 > coord[1] >= ALTURA or 0 > coord[3] >= ALTURA) or (0 > coord[0] >= LARGURA or 0 > coord[3] >= LARGURA):

            for indice in range(3):
                for parte in colisoes[indice]:
                    resultados = []
                    for testes in range(4):
                        if parte[testes] / LARGURA_PIXEL > 1:
                            parte = parte[testes] - 1
                        else:
                            parte = parte[testes] + 1

                        # Se a colisão não se tratar das dos obstáculos, ele executa esse trecho
                        if indice is not 3:
                            if parte == coord[testes]:
                                resultados.append(False)
                            else:
                                resultados.append(True)
                        else:
                            if lado == 0:
                                # Cima e baixo
                                if sublado == 0:
                                    ...
                                else:
                                    ...

                            else:
                                # Esquerda e direita
                                if sublado == 0:
                                    ...
                                else:
                                    ...


                    permissao = all(resultados)
                    if not permissao:
                        break

        return permissao

    # -- Os métodos que fazem os movimentos --
    def esquerda(self, *args):
        if self.modx == 0:
            self.modx, self.mody = -VELOCIDADE, 0
            self.lado = 'E'  # ; self.VelocidadePlayer()

    def direita(self, *args):
        if self.modx == 0:
            self.modx, self.mody = VELOCIDADE, 0
            self.lado = 'D'  # ; self.VelocidadePlayer()

    def cima(self, *args):
        if self.mody == 0:
            self.modx, self.mody = 0, -VELOCIDADE
            self.lado = 'C'  # ; self.VelocidadePlayer()

    def baixo(self, *args):
        if self.mody == 0:
            self.modx, self.mody = 0, VELOCIDADE
            self.lado = 'B'  # ; self.VelocidadePlayer()

    def Movimenta(self):
        # -- Movimenta o personagem --
        self.canvas.move('player', self.modx, self.mody)

    def MovimentaCorpo(self, id, vx, vy):
        # -- Movimenta o corpo --
        self.canvas.move(id, vx, vy)

    # -- Os métodos responsáveis por colocar e tirar tudo --
    def DeletaTudo(self):
        # -- Deleta todos os elementos existentes no canvas -- 
        for elemento in self.cobra: self.canvas.delete(elemento[0])
        for elemento in self.obstaculos: self.canvas.delete(elemento)
        self.canvas.delete('olhos')
        self.canvas.delete('maça')

    def IniciaElementos(self):
        # -- Inicia os elementos -- 
        self.jogando = False
        self.cobra = []
        self.lado = None
        self.colis_face = None
        self.pontos = 0
        self.tick = 75
        self.obstaculos = []


if __name__ == '__main__':
    JogoDaCobrinha()
