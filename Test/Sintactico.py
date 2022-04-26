from pydoc import describe
from xml.dom.minidom import Element
from Test.Lexico import Lexico
from Test.ErrorSintactico import ErrorSintactico


class Sintactico():

    def __init__(self, lista_tokens) -> None:
        self.errores = list()
        self.caracter = ''
        self.tipo = ''
        self.respuesta = ''
        self.answer = ''
        self.posicion = 0
        self.estado = 0
        self.lista = lista_tokens
        self.ultimo = ''
        self.preanalisis = self.lista[self.posicion]
        self.ultimo = self.preanalisis = self.lista[-1]
        self.cadena = 'Cadena'
        self.palabraReservada = 'Palabra_Reservada'
        self.fecha = 'Fecha'
        self.numero = 'Numero'
        self.file = 'Nombre_Archivo'
        self.banderaFile = 'Bandera_Archivo'
        self.nameFile = 'Nombre_Archivo'
        self.banderaJornadaI = 'Bandera_Jornada_Inicio'
        self.banderaJornadaF = 'Bandera_Jornada_Final'
        self.numJornadaI = 'Numero_Inicio'
        self.numJornadaF = 'Numero_Final'
        self.banderaEquipo = 'Bandera_Equipos'
        self.numEquipos = 'Numero_Equipos'
        self.Inicio()

    def Match(self, tipo):
        if self.preanalisis.id != tipo:
            # print("--Error Sintactico",
            # str(self.preanalisis.id), " -- Se esperaba "+str(tipo))
            self.caracter = self.preanalisis.id
            self.tipo = tipo
            self.error()

        if self.preanalisis.id == tipo and self.preanalisis.id != self.ultimo.id:
            if self.posicion <= len(self.lista):
                self.posicion += 1
                self.preanalisis = self.lista[self.posicion]

        if self.preanalisis.id == self.ultimo.id:
            self.answer = 'Se a finalizado el analisis sintactico'

    def Inicio(self) -> None:
        self.posicion = 0
        self.preanalisis = self.lista[self.posicion]
        if self.palabraReservada == self.preanalisis.id:
            valor = self.preanalisis.valor
            if valor.valor == 'RESULTADO':
                self.posicion += 1
                self.preanalisis = self.lista[self.posicion]
                self.resultadoPartido()
            elif valor.valor == 'JORNADA':
                self.posicion += 1
                self.preanalisis = self.lista[self.posicion]
                self.resultadoJornada()
            elif valor.valor == 'GOLES':
                self.posicion += 1
                self.preanalisis = self.lista[self.posicion]
                self.golesTemporada()
            elif valor.valor == 'TABLA':
                self.posicion += 1
                self.preanalisis = self.lista[self.posicion]
                self.tablaTemporada()
            elif valor.valor == 'PARTIDOS':
                self.posicion += 1
                self.preanalisis = self.lista[self.posicion]
                self.temporadaEquipo()
            elif valor.valor == 'TOP':
                self.posicion += 1
                self.preanalisis = self.lista[self.posicion]
                self.topEquipos()
            else:
                self.lex = Lexico()
                self.caracter = valor.valor
                self.tipo = self.lex.reserved
                self.error()
        else:
            self.caracter = 'Vacio'
            self.tipo = self.palabraReservada
            self.error()

    def resultadoPartido(self):
        self.Match(self.cadena)
        self.Match(self.palabraReservada)
        self.Match(self.cadena)
        self.Match(self.palabraReservada)
        self.Match(self.fecha)

    def resultadoJornada(self):
        self.Match(self.numero)
        self.Match(self.palabraReservada)
        self.Match(self.fecha)

        condicion_1 = 'False'
        for elemento in self.lista:
            id = elemento
            if self.banderaFile == id.id:
                condicion_1 = 'True'

        condicion_2 = 'False'
        for elemento in self.lista:
            id = elemento
            if self.nameFile == id.id:
                condicion_2 = 'True'

        if condicion_1 == 'True' and condicion_2 == 'True':
            self.Match(self.banderaFile)
            self.Match(self.nameFile)
        elif condicion_1 == 'True' and condicion_2 == 'False':
            self.caracter = self.banderaFile
            self.tipo = self.nameFile
            self.error()

    def golesTemporada(self):
        self.Match(self.palabraReservada)
        self.Match(self.cadena)
        self.Match(self.palabraReservada)
        self.Match(self.fecha)

    def tablaTemporada(self):
        self.Match(self.palabraReservada)
        self.Match(self.fecha)

        condicion_1 = 'False'
        for elemento in self.lista:
            id = elemento
            if self.banderaFile == id.id:
                condicion_1 = 'True'

        condicion_2 = 'False'
        for elemento in self.lista:
            id = elemento
            if self.nameFile == id.id:
                condicion_2 = 'True'

        if condicion_1 == 'True' and condicion_2 == 'True':
            self.Match(self.banderaFile)
            self.Match(self.nameFile)
        elif condicion_1 == 'True' and condicion_2 == 'False':
            self.caracter = self.banderaFile
            self.tipo = self.nameFile
            self.error()

    def temporadaEquipo(self):
        self.Match(self.cadena)
        self.Match(self.palabraReservada)
        self.Match(self.fecha)

        condicion_1 = 'False'
        condicion_2 = 'False'
        for elemento in self.lista:
            id = elemento
            if self.banderaFile == id.id:
                condicion_1 = 'True'
            if self.nameFile == id.id:
                condicion_2 = 'True'

        if condicion_1 == 'True' and condicion_2 == 'True':
            self.Match(self.banderaFile)
            self.Match(self.nameFile)
        elif condicion_1 == 'True' and condicion_2 == 'False':
            self.caracter = self.banderaFile
            self.tipo = self.nameFile
            self.error()

        condicion_1 = 'False'
        condicion_2 = 'False'
        for elemento in self.lista:
            id = elemento
            if self.banderaJornadaI == id.id:
                condicion_1 = 'True'
            if self.numJornadaI == id.id:
                condicion_2 = 'True'


        if condicion_1 == 'True' and condicion_2 == 'True':
            self.Match(self.banderaJornadaI)
            self.Match(self.numJornadaI)
        elif condicion_1 == 'True' and condicion_2 == 'False':
            self.caracter = self.banderaJornadaI
            self.tipo = self.numJornadaI
            self.error()

        condicion_1 = 'False'
        condicion_2 = 'False'
        for elemento in self.lista:
            id = elemento
            if self.banderaJornadaF == id.id:
                condicion_1 = 'True'
            if self.numJornadaF == id.id:
                condicion_2 = 'True'

        if condicion_1 == 'True' and condicion_2 == 'True':
            self.Match(self.banderaJornadaF)
            self.Match(self.numJornadaF)
        elif condicion_1 == 'True' and condicion_2 == 'False':
            self.caracter = self.banderaJornadaF
            self.tipo = self.numJornadaF
            self.error()

    def topEquipos(self):
        self.Match(self.palabraReservada)
        self.Match(self.palabraReservada)
        self.Match(self.fecha)
        
        condicion_1 = 'False'
        condicion_2 = 'False'
        for elemento in self.lista:
            id = elemento
            if self.banderaEquipo == id.id:
                condicion_1 = 'True'
            if self.numEquipos == id.id:
                condicion_2 = 'True'

        if condicion_1 == 'True' and condicion_2 == 'True':
            self.Match(self.banderaEquipo)
            self.Match(self.numEquipos)
        elif condicion_1 == 'True' and condicion_2 == 'False':
            self.caracter = self.banderaEquipo
            self.tipo = self.numEquipos
            self.error()
            
    def error(self):
        descripcion = 'Se esperaba'
        err = ErrorSintactico(self.caracter, descripcion, self.tipo)
        self.errores.append(err)
