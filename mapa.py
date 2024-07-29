import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from defines import *
from tabuleiro import Tabuleiro

# Função para desenhar o tabuleiro de uma forma mais clara
def desenha_tabuleiro(ax, tabuleiro):
    linhas, colunas = tabuleiro.getLinhas(), tabuleiro.getColunas()
    matriz = tabuleiro.getMatriz()

    # Desenhar a grade do tabuleiro
    for linha in range(linhas):
        for coluna in range(colunas):
            rect = plt.Rectangle((coluna - 0.5, linhas - linha - 1.5), 1, 1, edgecolor='black', facecolor='blue')
            ax.add_artist(rect)

    # Desenhar as peças
    for linha in range(linhas):
        for coluna in range(colunas):
            cor = 'white' if matriz[linha][coluna] == 0 else ('red' if matriz[linha][coluna] == AGENTE_2 else 'yellow')
            circle = plt.Circle((coluna, linhas - linha - 1), 0.4, edgecolor='black', facecolor=cor)
            ax.add_artist(circle)

    ax.set_xlim(-0.5, colunas - 0.5)
    ax.set_ylim(-0.5, linhas - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    ax.grid(False)

# Função para converter o estado do tabuleiro in string
def estado_para_string(tabuleiro):
    return str(tabuleiro.getMatriz().flatten())

# Função para calcular a heurística de um estado do tabuleiro
def calculaHeuristicaGrupo(grupo, idAgente):
    idAdversario = AGENTE_2 if idAgente == AGENTE_1 else AGENTE_1
    valorHeuristicaGrupo = 0
    if (grupo.count(idAgente) == 3 and grupo.count(AGENTE_VAZIO) == 1):
        valorHeuristicaGrupo += 100
    if (grupo.count(idAgente) == 2 and grupo.count(AGENTE_VAZIO) == 2):
        valorHeuristicaGrupo += 45
    if (grupo.count(idAdversario) == 3 and grupo.count(AGENTE_VAZIO) == 1):
        valorHeuristicaGrupo -= 90
    return valorHeuristicaGrupo

def calculaHeuristicaTabuleiro(tabuleiro, idAgente):
    matriz = tabuleiro.getMatriz()
    valorHeuristica = 0
    for linha in range(tabuleiro.getLinhas()):
        if (matriz[linha][tabuleiro.getColunas() // 2] == idAgente):
            valorHeuristica += 50
    for linha in range(tabuleiro.getLinhas()):
        for coluna in range(tabuleiro.getColunas() - 3):
            horizontal = [matriz[linha][coluna], matriz[linha][coluna + 1], matriz[linha][coluna + 2], matriz[linha][coluna + 3]]
            valorHeuristica += calculaHeuristicaGrupo(horizontal, idAgente)
    for coluna in range(tabuleiro.getColunas()):
        for linha in range(tabuleiro.getLinhas() - 3):
            vertical = [matriz[linha][coluna], matriz[linha + 1][coluna], matriz[linha + 2][coluna], matriz[linha + 3][coluna]]
            valorHeuristica += calculaHeuristicaGrupo(vertical, idAgente)
    for linha in range(tabuleiro.getLinhas() - 3):
        for coluna in range(tabuleiro.getColunas() - 3):
            diagonal1 = [matriz[linha][coluna], matriz[linha + 1][coluna + 1], matriz[linha + 2][coluna + 2], matriz[linha + 3][coluna + 3]]
            valorHeuristica += calculaHeuristicaGrupo(diagonal1, idAgente)
            diagonal2 = [matriz[linha][coluna + 3], matriz[linha + 1][coluna + 2], matriz[linha + 2][coluna + 1], matriz[linha + 3][coluna]]
            valorHeuristica += calculaHeuristicaGrupo(diagonal2, idAgente)
    return valorHeuristica

# Função para gerar o mapa de estados
def gera_mapa_de_estados(tabuleiro, profundidade, idAgente, grafo, estado_anterior=None):
    if profundidade == 0:
        return

    colunasLivres = tabuleiro.getListaColunasLivres()
    for coluna in colunasLivres:
        tabuleiroAux = Tabuleiro(tabuleiro.getLinhas(), tabuleiro.getColunas(), tabuleiro.getMatriz().copy())
        tabuleiroAux.posiciona(coluna, idAgente)

        estado_atual = estado_para_string(tabuleiro)
        estado_futuro = estado_para_string(tabuleiroAux)
        heuristica = calculaHeuristicaTabuleiro(tabuleiroAux, AGENTE_2)

        grafo.add_node(estado_futuro, tabuleiro=tabuleiroAux.getMatriz().copy(), heuristica=heuristica)
        if estado_anterior:
            grafo.add_edge(estado_anterior, estado_futuro)

        # Alterna o agente para o próximo nível de profundidade
        proximoAgente = AGENTE_2 if idAgente == AGENTE_1 else AGENTE_1
        gera_mapa_de_estados(tabuleiroAux, profundidade - 1, proximoAgente, grafo, estado_futuro)

# Exemplo de uso
tabuleiroInicial = Tabuleiro(LINHAS, COLUNAS)
grafo = nx.DiGraph()

# Gera o mapa de estados a partir do tabuleiro inicial, com uma profundidade de 3 níveis
gera_mapa_de_estados(tabuleiroInicial, 2, AGENTE_2, grafo)

# Filtrar os estados onde o agente vermelho faz uma jogada e exibir o tabuleiro resultante
estados_filtrados = []
for node in grafo.nodes:
    tabuleiro = grafo.nodes[node]['tabuleiro']

    estados_filtrados.append(node)

# Organizar os tabuleiros in um layout de grade
num_states = len(estados_filtrados)
rows = int(np.ceil(np.sqrt(num_states)))
cols = rows

fig, axes = plt.subplots(rows, cols, figsize=(cols * 2, rows * 2))

# Remover espaços entre subplots
fig.subplots_adjust(hspace=0.5, wspace=0.5)

for idx, node in enumerate(estados_filtrados):
    row = idx // cols
    col = idx % cols
    tabuleiro = grafo.nodes[node]['tabuleiro']
    heuristica = grafo.nodes[node]['heuristica']
    ax = axes[row, col] if rows > 1 else axes[col]
    desenha_tabuleiro(ax, Tabuleiro(LINHAS, COLUNAS, tabuleiro))
    ax.set_title(f"Heurística: {heuristica}", fontsize=8)
    ax.axis('off')

# Esconder subplots vazios
for idx in range(num_states, rows * cols):
    row = idx // cols
    col = idx % cols
    ax = axes[row, col] if rows > 1 else axes[col]
    ax.axis('off')

plt.show()
