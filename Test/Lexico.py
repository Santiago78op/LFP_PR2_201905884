from Test.Error import Error
from Test.Token import *
from Test.Lexema import *


class Lexico():

    def __init__(self) -> None:
        self.estado = 0
        self.conteo = 0
        self.cont = 0
        self.cont_1 = 0
        self.fila = 1
        self.col = 1
        self.prefijo = ''
        self.tok = ''
        self.entrada = list()
        self.flujo = list()
        self.tokens = list()
        self.errores = list()
        self.imgs = list()
        self.img = dict()
        self.subcont = list()
        self.tipo = ''
        self.seccion = ''
        self.reserved = [
            'RESULTADO',
            'JORNADA',
            'PARTIDOS',
            'GOLES',
            'TABLA',
            'TOP'
        ]
        self.condition = [
            'VS',
            'TEMPORADA',
            'LOCAL',
            'VISITANTE',
            'TOTAL',
            'SUPERIOR',
            'INFERIOR'
        ]

    def escanear(self, entrada):
        self.str_to_list(entrada)
        while len(self.entrada) > 0:
            if self.getSeparador():
                continue
            elif self.aceptacion():
                continue
            elif self.getId():
                token = Token('Palabra_Reservada', self.getLexema())
                self.addToken(token)
            elif self.getCadena():
                token = Token('Cadena', self.getLexema())
                self.addToken(token)
            elif self.getFecha():
                token = Token('Fecha', self.getLexema())
                self.addToken(token)
            elif self.getNumero():
                token = Token('Numero', self.getLexema())
                self.addToken(token)
            elif self.getBanderaFile():
                token = Token('Bandera_Archivo', self.getLexema())
                self.addToken(token)
            elif self.getNameFile():
                token = Token('Nombre_Archivo', self.getLexema())
                self.addToken(token)
            elif self.getBanderaJornada():
                token = Token(self.tok, self.getLexema())
                self.addToken(token)
            elif self.getNumJornada():
                token = Token(self.tok, self.getLexema())
                self.addToken(token)
            elif self.getEquipo():
                token = Token('Bandera_Equipos', self.getLexema())
                self.addToken(token)
            elif self.getNumEquipo():
                token = Token('Numero_Equipos', self.getLexema())
                self.addToken(token)
            else:  # Hay un error léxico
                self.error()
                self.tipo = 'Desconocido'
        if len(self.errores) == 0:
            self.imgs.append(self.img)

    def str_to_list(self, entrada):
        chars = list()
        for c in entrada:
            chars.append(c)
        chars[len(chars):] = ['#']
        self.entrada = chars
        self.flujo = chars

    def sigChar(self) -> str:
        return self.entrada[0]

    def getLexema(self) -> Lexema:
        inicio = self.col - self.conteo
        lexema = Lexema(self.prefijo, self.fila, self.col)
        self.prefijo = ''
        self.conteo = 0
        return lexema

    def getId(self) -> bool:  # regex: [A-Z]+
        self.regresar()  # Obtener los caracteres previamente analizados por otro automata
        while 1:
            if self.estado == 0:
                if self.sigChar().isupper():
                    self.transicion(1)
                else:
                    return False
            elif self.estado == 1:
                reservada = self.prefijo
                if self.sigChar().isupper():
                    self.transicion(1)
                elif self.getSeparador():
                    if reservada in self.reserved:
                        self.seccion = f'Palabra_Reservada{str(self.cont_1)}'
                        self.img[self.seccion] = reservada
                        self.cont_1 += 1
                        return True
                    elif reservada in self.condition:
                        self.seccion = f'Palabra_Reservada{str(self.cont_1)}'
                        self.img[self.seccion] = reservada
                        self.cont_1 += 1
                        return True
                    else:
                        return False
                else:
                    if reservada in self.reserved:
                        self.seccion = f'Palabra_Reservada{str(self.cont_1)}'
                        self.img[self.seccion] = reservada
                        self.cont_1 += 1
                        return True
                    elif reservada in self.condition:
                        self.seccion = f'Palabra_Reservada{str(self.cont_1)}'
                        self.img[self.seccion] = reservada
                        self.cont_1 += 1
                        return True
                    else:
                        self.tipo = 'Error en la palabra Reservada'
                        self.prefijo = ''
                        return False

    def getCadena(self) -> bool:
        self.regresar()
        while 1:
            if self.estado == 0:
                if self.sigChar() == '"':
                    self.transicion(1)
                elif self.sigChar() == '“' or self.sigChar() == '”':
                    self.tipo = 'Error en el tipo de Comilla Ingresada'
                    return False
                else:
                    return False
            elif self.estado == 1:
                c = self.sigChar()
                if c != '"' and c != '\n':
                    self.transicion(1)
                elif c == '"':
                    self.transicion(2)
                else:
                    return False
            elif self.estado == 2:
                self.prefijo = self.prefijo.replace('"', '')
                self.seccion = f'Cadena_{str(self.cont)}'
                self.img[self.seccion] = self.prefijo
                self.cont += 1
                return True

    def getFecha(self) -> bool:
        self.regresar()
        while 1:
            if self.estado == 0:
                if self.sigChar() == '<':
                    self.transicion(1)
                else:
                    return False
            elif self.estado == 1:
                c = self.sigChar()
                if c.isdigit() and c != '\n':
                    self.transicion(1)
                elif c == '-' and c != '\n':
                    self.transicion(1)
                elif c == '>':
                    self.transicion(2)
                else:
                    self.tipo = 'Error la Fecha no puede Contener Letras'
                    return False
            elif self.estado == 2:
                self.seccion = 'Fecha'
                self.img[self.seccion] = self.prefijo
                return True

    def getNumero(self) -> bool:
        self.regresar()
        if self.seccion != 'Bandera_Jornada' and self.seccion != 'Bandera_Equipo':
            while 1:
                if self.estado == 0:
                    if self.sigChar().isdigit():
                        self.transicion(1)
                    else:
                        return False
                elif self.estado == 1:
                    if self.sigChar().isdigit():
                        self.transicion(1)
                    elif self.getSeparador():
                        self.seccion = 'Numero'
                        self.img[self.seccion] = self.prefijo
                        return True
                    else:
                        self.seccion = 'Numero'
                        self.img[self.seccion] = self.prefijo
                        return True
        else:
            return False

    def getBanderaFile(self) -> bool:
        self.regresar()
        while 1:
            if self.estado == 0:
                if self.sigChar() == '-':
                    self.transicion(1)
                else:
                    return False
            elif self.estado == 1:
                if self.sigChar() == 'f':
                    self.transicion(2)
                elif self.sigChar() != 'f':
                    self.entrada.insert(0, '-')
                    self.regresar()
                    self.prefijo = ''
                    return False
            elif self.estado == 2:
                self.seccion = 'Bandera_Archivo'
                self.subcont.append(self.prefijo)
                self.img[self.seccion] = self.subcont
                return True

    def getNameFile(self) -> bool:
        self.regresar()
        while 1:
            if self.seccion == 'Bandera_Archivo':
                if self.estado == 0:
                    if self.sigChar().isdigit():
                        self.transicion(1)
                    elif self.sigChar().isalpha():
                        self.transicion(1)
                    elif self.sigChar() == '_':
                        self.transicion(1)
                    else:
                        self.tipo = 'Letras, numeros y guiones bajos'
                        return False
                elif self.estado == 1:
                    if self.sigChar().isdigit():
                        self.transicion(1)
                    elif self.sigChar().isalpha():
                        self.transicion(1)
                    elif self.sigChar() == '_':
                        self.transicion(1)
                    elif self.sigChar() == ' ':
                        self.transicion(2)
                    elif self.sigChar() == '':
                        self.transicion(2)
                    elif self.sigChar() == '#':
                        self.transicion(2)
                    else:
                        self.tipo = 'Letras, numeros y guiones bajos'
                        return False
                elif self.estado == 2:
                    self.prefijo = self.prefijo.replace('#', '')
                    self.subcont.append(self.prefijo)
                    self.img[self.seccion] = self.subcont
                    self.subcont = list()
                    return True
            else:
                return False

    def getBanderaJornada(self):
        self.regresar()
        while 1:
            if self.estado == 0:
                if self.sigChar() == '-':
                    self.transicion(1)
                else:
                    return False
            elif self.estado == 1:
                if self.sigChar() == 'j':
                    self.transicion(2)
                elif self.sigChar() != 'j':
                    self.entrada.insert(0, '-')
                    self.regresar()
                    self.prefijo = ''
                    return False
            elif self.estado == 2:
                if self.sigChar() == 'i':
                    self.transicion(3)
                elif self.sigChar() == 'f':
                    self.transicion(3)
                else:
                    return False
            elif self.estado == 3:
                if self.prefijo == '-ji':
                    self.tok = 'Bandera_Jornada_Inicio'
                    self.seccion = 'Bandera_Jornada'
                    self.subcont.append(self.prefijo)
                    self.img[self.seccion] = self.subcont
                    return True
                elif self.prefijo == '-jf':
                    self.tok = 'Bandera_Jornada_Final'
                    self.seccion = 'Bandera_Jornada'
                    self.subcont.append(self.prefijo)
                    self.img[self.seccion] = self.subcont
                    return True

    def getNumJornada(self) -> bool:
        self.regresar()
        while 1:
            if self.seccion == 'Bandera_Jornada':
                if self.estado == 0:
                    if self.sigChar().isdigit():
                        self.transicion(1)
                    else:
                        self.tipo = 'Solo numeros'
                        return False
                elif self.estado == 1:
                    if self.sigChar().isdigit():
                        self.transicion(1)
                    elif self.sigChar() == ' ':
                        self.transicion(2)
                    elif self.sigChar() == '':
                        self.transicion(2)
                    elif self.sigChar() == '#':
                        self.transicion(2)
                    else:
                        self.tipo = 'Solo numeros'
                        return False
                elif self.estado == 2:
                    if '-ji' in self.subcont and '-jf' not in self.subcont:
                        self.tok = 'Numero_Inicio'
                        self.prefijo = self.prefijo.replace('#', '')
                        self.subcont.append(self.prefijo)
                        self.img[self.seccion] = self.subcont
                        return True
                    elif '-jf' in self.subcont and '-ji' in self.subcont:
                        self.tok = 'Numero_Final'
                        self.prefijo = self.prefijo.replace('#', '')
                        self.subcont.append(self.prefijo)
                        self.img[self.seccion] = self.subcont
                        return True
            else:
                return False

    def getEquipo(self) -> bool:
        self.regresar()
        while 1:
            if self.estado == 0:
                if self.sigChar() == '-':
                    self.transicion(1)
                else:
                    return False
            elif self.estado == 1:
                if self.sigChar() == 'n':
                    self.transicion(2)
                elif self.sigChar() != 'n':
                    self.entrada.insert(0, '-')
                    self.regresar()
                    self.prefijo = ''
                    return False
            elif self.estado == 2:
                self.subcont = list()
                self.seccion = 'Bandera_Equipo'
                self.subcont.append(self.prefijo)
                self.img[self.seccion] = self.subcont
                return True

    def getNumEquipo(self) -> bool:
        self.regresar()
        if self.seccion == 'Bandera_Equipo':
            while 1:
                if self.estado == 0:
                    if self.sigChar().isdigit():
                        self.transicion(1)
                    else:
                        self.tipo = 'Solo numeros'
                        return False
                elif self.estado == 1:
                    if self.sigChar().isdigit():
                        self.transicion(1)
                    elif not self.sigChar().isdigit():
                        self.transicion(2)
                    elif self.sigChar() == ' ':
                        self.transicion(2)
                    elif self.sigChar() == '':
                        self.transicion(2)
                    elif self.sigChar() == '#':
                        self.transicion(2)
                    else:
                        self.tipo = 'Solo numeros'
                        return False
                elif self.estado == 2:
                    self.prefijo = self.prefijo.replace('#', '')
                    self.subcont.append(self.prefijo)
                    self.img[self.seccion] = self.subcont
                    self.subcont = list()
                    return True
        else:
            return False
    
    def aceptacion(self):
        c = self.sigChar()
        if c == '#':
            self.consumir()
            return True

    def getSeparador(self) -> bool:
        c = self.sigChar()
        if c == ' ' or c == '\t':
            self.consumir()
            return True
        elif self.sigChar() == '\n':
            self.consumir()
            self.updateCount()
            return True
        else:
            return False

    def transicion(self, estado: int):
        self.prefijo += self.consumir()
        self.estado = estado

    def consumir(self) -> str:
        self.col += 1
        self.conteo += 1
        return self.flujo.pop(0)

    def updateCount(self):
        self.fila += 1
        self.col = 1
        self.conteo = 0

    def addToken(self, t: Token):
        self.tokens.append(t)
        self.entrada = self.flujo
        self.estado = 0

    def regresar(self):
        self.flujo = self.entrada
        self.estado = 0

    def error(self):
        caracter = self.consumir()
        self.entrada = self.flujo
        err = Error(self.fila, self.col, caracter, self.tipo)
        self.errores.append(err)
        self.estado = 0
