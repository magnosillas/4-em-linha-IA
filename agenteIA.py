from defines import *
from agente import Agente
from tabuleiro import Tabuleiro
import random

class AgenteIA(Agente):

    # Calcula a heurística para um grupo de 4 espaços
    def calculaHeuristicaGrupo(self, grupo, idAgente):
        # Determina o ID do adversário
        idAdversario = AGENTE_2 if self.getId() == AGENTE_1 else AGENTE_1

        valorHeuristicaGrupo = 0

        # Adiciona 100 pontos se há 3 peças do agente e 1 espaço vazio
        if (grupo.count(idAgente) == 3 and grupo.count(AGENTE_VAZIO) == 1):
            valorHeuristicaGrupo += 100

        # Adiciona 45 pontos se há 2 peças do agente e 2 espaços vazios
        if (grupo.count(idAgente) == 2 and grupo.count(AGENTE_VAZIO) == 2):
            valorHeuristicaGrupo += 45

        # Subtrai 90 pontos se há 3 peças do adversário e 1 espaço vazio
        if (grupo.count(idAdversario) == 3 and grupo.count(AGENTE_VAZIO) == 1):
            valorHeuristicaGrupo -= 90

        return valorHeuristicaGrupo

    # Define o valor heurístico de um estado do tabuleiro
    def calculaHeuristicaTabuleiro(self, tabuleiro, idAgente):
        matriz = tabuleiro.getMatriz()

        valorHeuristica = 0

        # Adiciona pontos para a coluna central, que dá mais controle do tabuleiro
        for linha in range(tabuleiro.getLinhas()):
            if (matriz[linha][tabuleiro.getColunas() // 2] == idAgente):
                valorHeuristica += 50

        # Avalia linhas horizontais
        for linha in range(tabuleiro.getLinhas()):
            for coluna in range(tabuleiro.getColunas() - 3):
                horizontal = [matriz[linha][coluna], matriz[linha][coluna + 1], matriz[linha][coluna + 2], matriz[linha][coluna + 3]]
                valorHeuristica += self.calculaHeuristicaGrupo(horizontal, idAgente)

        # Avalia linhas verticais
        for coluna in range(tabuleiro.getColunas()):
            for linha in range(tabuleiro.getLinhas() - 3):
                vertical = [matriz[linha][coluna], matriz[linha + 1][coluna], matriz[linha + 2][coluna], matriz[linha + 3][coluna]]
                valorHeuristica += self.calculaHeuristicaGrupo(vertical, idAgente)

        # Avalia diagonais
        for linha in range(tabuleiro.getLinhas() - 3):
            for coluna in range(tabuleiro.getColunas() - 3):

                # Diagonal superior esquerda para inferior direita
                diagonal1 = [matriz[linha][coluna], matriz[linha + 1][coluna + 1], matriz[linha + 2][coluna + 2], matriz[linha + 3][coluna + 3]]
                valorHeuristica += self.calculaHeuristicaGrupo(diagonal1, idAgente)

                # Diagonal inferior esquerda para superior direita
                diagonal2 = [matriz[linha][coluna + 3], matriz[linha + 1][coluna + 2], matriz[linha + 2][coluna + 1], matriz[linha + 3][coluna]]
                valorHeuristica += self.calculaHeuristicaGrupo(diagonal2, idAgente)

        return valorHeuristica

    # Implementa o algoritmo Minimax com poda alfa-beta
    def buscaColunaMiniMax(self, tabuleiro, profundidade, alpha, beta, maximizar):
        colunasLivres = tabuleiro.getListaColunasLivres()

        # Verifica se há um estado de vitória
        vitoriaAgente1 = tabuleiro.verificaEstado(AGENTE_1) == VITORIA
        vitoriaAgente2 = tabuleiro.verificaEstado(AGENTE_2) == VITORIA

        # Determina se o jogo está em um estado terminal
        posicaoTerminal = len(colunasLivres) == 0 or vitoriaAgente1 or vitoriaAgente2

        if (profundidade == 0 or posicaoTerminal):

            if posicaoTerminal:
                if vitoriaAgente1:
                    return (None, INFINITO_NEGATIVO)
                elif vitoriaAgente2:
                    return (None, INFINITO_POSITIVO)
                else:
                    return (None, 0)  # Nenhuma jogada válida
            else:
                # Profundidade zero indica o último nó possível de expandir
                return (None, self.calculaHeuristicaTabuleiro(tabuleiro, AGENTE_2))

        if maximizar:
            valorHeuristica = INFINITO_NEGATIVO
            colunaRet = random.choice(colunasLivres)

            for coluna in colunasLivres:
                # Cria uma cópia do tabuleiro para avaliar as variações recursivamente
                tabuleiroAux = Tabuleiro(tabuleiro.getLinhas(), tabuleiro.getColunas(), tabuleiro.getMatriz().copy())
                tabuleiroAux.posiciona(coluna, AGENTE_2)

                # Chama recursivamente o Minimax para a próxima profundidade, alternando para minimizar
                heuristicaFilho = self.buscaColunaMiniMax(tabuleiroAux, profundidade - 1, alpha, beta, False)[1]
                if heuristicaFilho > valorHeuristica:
                    valorHeuristica = heuristicaFilho
                    colunaRet = coluna

                alpha = max(alpha, valorHeuristica)

                if beta <= alpha:
                    # Poda alfa-beta: interrompe a busca neste ramo
                    break

            return colunaRet, valorHeuristica

        else:
            valorHeuristica = INFINITO_POSITIVO
            colunaRet = random.choice(colunasLivres)

            for coluna in colunasLivres:
                # Cria uma cópia do tabuleiro para avaliar as variações recursivamente
                tabuleiroAux = Tabuleiro(tabuleiro.getLinhas(), tabuleiro.getColunas(), tabuleiro.getMatriz().copy())
                tabuleiroAux.posiciona(coluna, AGENTE_1)

                # Chama recursivamente o Minimax para a próxima profundidade, alternando para maximizar
                heuristicaFilho = self.buscaColunaMiniMax(tabuleiroAux, profundidade - 1, alpha, beta, True)[1]
                if heuristicaFilho < valorHeuristica:
                    valorHeuristica = heuristicaFilho
                    colunaRet = coluna

                beta = min(beta, valorHeuristica)

                if beta <= alpha:
                    # Poda alfa-beta: interrompe a busca neste ramo
                    break

            return colunaRet, valorHeuristica

    # Método que realiza a jogada do agente
    def onJogar(self, tabuleiro, tela):
        # Chama o Minimax para encontrar a melhor coluna para jogar
        coluna, valorMiniMax = self.buscaColunaMiniMax(tabuleiro, tabuleiro.getLinhas() - 1, INFINITO_NEGATIVO, INFINITO_POSITIVO, True)

        # Posiciona a peça na coluna escolhida
        tabuleiro.posiciona(coluna, self.getId())
