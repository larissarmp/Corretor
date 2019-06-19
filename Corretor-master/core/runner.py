import json

import core.morfologico as morfologico
import core.analisadorSintatico as analisadorSintatico 

def organizarFrases(lista):
    listaPalavra = list(map(lambda palavra: palavra.palavra, lista))
    return ' '.join(listaPalavra)

def run(frase):
    listaPalavra = morfologico.analisarTexto(frase)
    listaPossiveis = analisadorSintatico.verificarSintaxe(listaPalavra)
    listaPossiveis = list(map(organizarFrases, listaPossiveis))
    return json.dumps(listaPossiveis)
