'''
Classe palavra
'''
#pluralidade
SINGULAR = 0
PLURAL = 1
INDEFINIDO = 2
#genêro
INDEFINIDO = 0
MASCULINO = 1
FEMININO = 2
#transitividade
INTRANSITIVO = 0
DIRETO = 1
INDIRETO = 2
DIRETO_INDIRETO = 3
NOMINAL = 4

#classe gramatical
NOME = 0
DETERMINANTE = 1
PRONOME = 2
VERBO = 3 #pela transitividade, o verbo ocupa 4 classes, 3-7
VERBO_IMP = 8
PREPOSICAO = 9
ADJETIVO = 10
ADVERBIO = 11
CONJUNCAO = 12
PRE_DETERMINANTE = 13


class Palavra:
    """Classe que representa uma palavra e seus atributos"""
    def __init__(self, jsonObj):
        self.palavra = ''
        self.distancia = 0
        self.genero = 0
        self.pluralidade = 0
        if isinstance(jsonObj, list):
            self.listaPossibilidades = jsonObj
        else:
            self.listaPossibilidades = []
            self.palavra = jsonObj['palavra']
            self.classe = jsonObj['classe']
            if 'genero' in jsonObj:
                self.genero = jsonObj['genero']
            if 'pluralidade' in jsonObj:
                self.pluralidade = jsonObj['pluralidade']
            if 'transitividade' in jsonObj:
                self.classe += jsonObj['transitividade']

    def tokenId(self):
        """Retorna o id único do tipo de token

        :return: id do token
        :rtype: int
        """

        return (self.classe << 6) + (self.pluralidade << 2) + self.genero

    def verificarPalavra(self, palavra) -> bool:
        """Verifica se uma string é a igual a esta palavra

        :param palavra: String de uma palavra
        :type palavra: str
        :return: True se a palavra informada é igual a esta
        :rtype: bool
        """

        return self.palavra == palavra
    
    def existe(self) -> bool:
        return len(self.palavra) > 0

    def __repr__(self):
        return self.palavra
