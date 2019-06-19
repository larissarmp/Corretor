'''
Analisador morfológico
'''
import json
from pathlib import Path
from typing import List

import nltk.tokenize

from core.palavra import Palavra

DIR = Path(__file__).resolve().parent
MAXIMO_DICAS = 5
DICIONARIO: List[Palavra]


def _getDicionario() -> List[Palavra]:
    dicionario = []
    objArr = json.load(Path.open(DIR / 'Dados' / 'dicionario.json'))
    for _ in range(0, 41):
        dicionario.append([])
    for obj in objArr:
        dicionario[len(obj['palavra'])].append(Palavra(obj))
        del obj
    return dicionario


DICIONARIO = _getDicionario()


def _zeros(linhas, colunas):
    aux = [0] * colunas
    matrix = []
    for _ in range(linhas):
        matrix.append(aux[:])
    return matrix


def _levenshteinThreshold(palavra1: str, palavra2: str, limite: int=999):
    insertion = 2
    deletion = 2
    substitution = 1
    levMatrix = _zeros(len(palavra1) + 1, len(palavra2) + 1)
    for i in range(len(palavra1)):
        levMatrix[i + 1][0] = levMatrix[i][0] + deletion
    for j in range(len(palavra2)):
        levMatrix[0][j + 1] = levMatrix[0][j] + insertion
    for i, charI in enumerate(palavra1):
        for j, charJ in enumerate(palavra2):
            if charI == charJ:
                levMatrix[i + 1][j + 1] = levMatrix[i][j]
            else:
                levMatrix[i + 1][j + 1] = min(levMatrix[i + 1][j] + insertion,
                                              levMatrix[i][j + 1] + deletion,
                                              levMatrix[i][j] + substitution)
        if min(levMatrix[i + 1]) >= limite:
            return -1
    return levMatrix[len(palavra1)][len(palavra2)]


def _inserirOrdenado(lista, obj):
    inseriu = False
    for i, existente in enumerate(lista):
        if obj.distancia <= existente.distancia:
            inseriu = True
            lista.insert(i, obj)
            break
    if not inseriu:
        lista.append(obj)


def _existe(palavra: str) -> bool:
    lista = DICIONARIO[len(palavra)]
    for possibilidade in lista:
        if possibilidade.palavra == palavra:
            return True
    return False


def _getPalavra(palavra: str) -> Palavra:
    lista = DICIONARIO[len(palavra)]
    for possibilidade in lista:
        if possibilidade.palavra == palavra:
            return possibilidade
    return None


def _analisarPalavra(palavra: str):
    realPalavra = _getPalavra(palavra)
    realPalavra = _verificarPalavra(realPalavra, palavra)
    return realPalavra


def _verificarPalavra(realPalavra: Palavra, palavra: str):
    if realPalavra is None:
        listaPalavraPossivel = []
        limiteInferior = len(palavra) - 2
        if limiteInferior <= 0:
            limiteInferior = 0
        limiteSuperior = len(palavra) + 2
        for i in range(limiteInferior, limiteSuperior):
            for possibilidade in DICIONARIO[i]:
                limite = (listaPalavraPossivel[-1].distancia
                          if len(listaPalavraPossivel) >= MAXIMO_DICAS else float('inf'))
                distancia = _levenshteinThreshold(palavra, possibilidade.palavra, limite)
                if distancia > -1:
                    if len(listaPalavraPossivel) == MAXIMO_DICAS:
                        listaPalavraPossivel.pop()
                    possibilidade.distancia = distancia
                    _inserirOrdenado(listaPalavraPossivel, possibilidade)
                    listaPalavraPossivel = sorted(listaPalavraPossivel, key=lambda x: x.distancia)
        realPalavra = Palavra(listaPalavraPossivel)
    return realPalavra


def analisarTexto(texto: str):
    """Analisar morfologicamente cada palavra do texto

    :param texto: frase a ser lida
    :type texto: str
    :return: Lista de objetos Palavra referente a cada palavra do texto
    :rtype: List[Palavra]
    """

    listaString = nltk.tokenize.word_tokenize(texto)

    listaPalavra: List[Palavra] = []
    for palavra in listaString:
        listaPalavra.append(_analisarPalavra(palavra))
    return listaPalavra
