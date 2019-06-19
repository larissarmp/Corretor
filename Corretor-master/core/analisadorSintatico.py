"""
Módulo responsável por verificar a sintaxe
"""
import re
from typing import List
from pathlib import Path
from core.palavra import Palavra

_ERR = -99
_ACC = 99

ARQUIVO_GRAMATICA = 'Dados/matriz.txt'
PASTA = Path(__file__).resolve().parent
_TOKEN_CODIGO = {
	0: 1,
	1: 0,
	2: 2,
	3: 4,
	4: 5,
	5: 6,
	8: 7,
	9: 8,
	11: 9
}
#[1, 0, 2, 5, 6, 7, 8, 9, 11]
_END = 10 #len(_TOKEN_CODIGO)

def _getTamanhoProducao() -> List[int]:
    string = open(PASTA / 'Dados' / 'gramatica.txt').read()
    tokens = re.sub(r'^.*->\s*', '', string, flags=re.M)
    lines = tokens.splitlines()
    tamanhoProducoes = [len(x.split(' ')) for x in lines]
    return tamanhoProducoes

def _getCodigoProducao() -> List[int]:
    string = open(PASTA / 'Dados' / 'gramatica.txt').read()
    tokens = re.sub(r'->.*', '', string, flags=re.M)
    linhas = list(map((lambda x: x.strip()), tokens.splitlines()))
    producoes = []
    for linha in linhas:
        if linha not in producoes:
            producoes.append(linha)
    codigoProducao = [producoes.index(x) for x in linhas]
    return codigoProducao

def _getGramatica() -> List[List[int]]:
    arquivo = Path.open(PASTA / ARQUIVO_GRAMATICA, 'r')
    matriz: List[List[int]] = []
    linhas: List[str] = arquivo.read().splitlines()
    for linhaAtual in linhas:
        colunas = list(map(lambda numero: int(numero.strip()), linhaAtual.rsplit(',')))
        matriz.append(colunas)
    return matriz

_ESTADOS = _getGramatica()
_PRODUCAO_TAMANHO = _getTamanhoProducao()
_PRODUCAO_CODIGO = _getCodigoProducao()


def _reduzir(estado, pilha):
    prod = estado * -1
    for _ in range(0, _PRODUCAO_TAMANHO[prod] * 2):
        pilha.pop()
    codigoNaoTerminal = _PRODUCAO_CODIGO[prod] + _END + 1
    proximoEstado = _ESTADOS[pilha[-1]][codigoNaoTerminal]
    pilha.append(codigoNaoTerminal)
    pilha.append(proximoEstado)

def _interpretar(listaToken: List[int]):
    estado = 0
    pilha: List[int] = [0]
    listaToken.append(_END)
    token = listaToken.pop(0)
    while True:
        estado = pilha[-1]
        if estado >= 0:
            estado = _ESTADOS[estado][token]
            if estado >= 0:
                if estado < 99:
                    pilha.append(token)
                    pilha.append(estado)
                    token = listaToken[0]
                    listaToken.pop(0)
                else:
                    print("Aceito")
                    return True
            elif estado > -99:
                _reduzir(estado, pilha)
            else:
                print('Errou')
                return False
    return False

def _expandirPossibilidades(listaFrase: List[List[Palavra]]):
    listaFraseAlterada = []
    encontrouErro = False
    for _, frase in enumerate(listaFrase):
        for i, palavra in enumerate(frase):
            if not palavra.existe():
                for possibilidade in palavra.listaPossibilidades:
                    novaFrase = frase[:]
                    novaFrase[i] = possibilidade
                    listaFraseAlterada.append(novaFrase)
                    encontrouErro = True
                break
    if encontrouErro:
        return _expandirPossibilidades(listaFraseAlterada)
    return listaFrase

def _verificarFrase(frase: List[Palavra]):
    listaToken = list(map(lambda palavra: palavra.classe if palavra.classe <= 4 else 0, frase)) #TODO: expandir a gramática e liberar todas as palavras
    listaToken = [_TOKEN_CODIGO[classe] for classe in listaToken]
    print(listaToken)
    return _interpretar(listaToken)

def verificarSintaxe(lista: List[Palavra]) -> List[Palavra]:
    """Verifica a sintaxe da gramática

    :param lista: Lista de Palavra para ser verificada
    :type lista: List[Palavra]
    :return: Retorna True se a sintaxe está correta
    :rtype: bool
    """
    listaFrase = _expandirPossibilidades([lista])
    listaFrase = list(filter(lambda frase: _verificarFrase(frase), listaFrase))
    #transforma códigos de classe na posição da matriz
    return listaFrase
