ALTURA = 680
LARGURA = 1020
 
VELOCIDADE = 20

Y = ALTURA // 2
X = LARGURA // 2

LARGURA_PIXEL = 20

ESQUERDA = ("self.canvas.create_rectangle((coord[0]+3, coord[1]+3), (coord[0]+8, coord[1]+8), fill='black', tag='olhos')", "self.canvas.create_rectangle((coord[0]+3, coord[3]-3), (coord[0]+8, coord[3]-8), fill='black', tag='olhos')")
DIREITA = ("self.canvas.create_rectangle((coord[2]-3, coord[1]+3), (coord[2]-8, coord[1]+8), fill='black', tag='olhos')", "self.canvas.create_rectangle((coord[2]-3, coord[3]-3), (coord[2]-8, coord[3]-8), fill='black', tag='olhos')")

CIMA = ("self.canvas.create_rectangle((coord[0]+3, coord[1]+4), (coord[0]+8, coord[1]+9), fill='black', tag='olhos')", "self.canvas.create_rectangle((coord[2]-3, coord[1]+4), (coord[2]-8, coord[1]+9), fill='black', tag='olhos')")
BAIXO = ("self.canvas.create_rectangle((coord[0]+3, coord[3]-4), (coord[0]+8, coord[3]-9), fill='black', tag='olhos')", "self.canvas.create_rectangle((coord[2]-3, coord[3]-4), (coord[2]-8, coord[3]-9), fill='black', tag='olhos')")

TICK_MAX = 110
TICK_MIN = 30

# Se quiser que a velocidade não se altere 
# Coloque o SUB == 0
SUB = 2
