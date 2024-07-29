from defines import *
from tabuleiro import Tabuleiro
from jogador import Jogador
from agenteIA import AgenteIA
import pygame as pg

estado = ANDAMENTO
tabuleiroReal = Tabuleiro(LINHAS, COLUNAS)

# Basta trocar qual classe do agente aqui para ajustar ordem ou colocar IA x IA ou jogador x jogador
agentes = [Jogador(AGENTE_1), AgenteIA(AGENTE_2)]

pg.init()
tela = pg.display.set_mode((LARGURA_DISPLAY, ALTURA_DISPLAY))
pg.display.set_caption("Connect 4 - Inteligência Artificial")

def esperar_tecla():
    esperando = True
    while esperando:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                esperando = False

if __name__ == "__main__":

    tabuleiroReal.printMatriz(tela)

    while estado == ANDAMENTO:

        for agente in agentes:

            agente.jogar(tabuleiroReal, tela)
            estado = tabuleiroReal.verificaEstado(agente.getId())

            if estado == VITORIA or estado == EMPATE:
                tabuleiroReal.anunciaEstado(tela, estado, agente.getId())

                esperar_tecla()  # Esperar até que uma tecla seja pressionada
                break

    pg.quit()
 