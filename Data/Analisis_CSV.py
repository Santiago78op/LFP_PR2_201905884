
# CSV Librerias
import re
import os

from numpy import append
from Builder.Temporada import Temporada
from List.List_Temporada import List_Temporada
# Librerias lectura CSV
import pandas as pd

# Flask Components
import requests
import json


class CSV():

    def Match(self, elemento):
        if elemento['Palabra_Reservada0'] == 'RESULTADO':
            temporada = elemento['Fecha']
            temporada = temporada.replace('<', '')
            temporada = temporada.replace('>', '')
            temporada = str(temporada)
            equipo1 = elemento['Cadena_0']
            equipo1 = str(equipo1)
            equipo2 = elemento['Cadena_1']
            equipo2 = str(equipo2)
            cadena = self.resultadoDeUnPartido(temporada, equipo1, equipo2)
            return cadena
        elif elemento['Palabra_Reservada0'] == 'JORNADA':
            temporada = elemento['Fecha']
            temporada = temporada.replace('<', '')
            temporada = temporada.replace('>', '')
            temporada = str(temporada)
            jornada = elemento['Numero']
            jornada = int(jornada)
            palabra = elemento['Palabra_Reservada1']
            palabra = str(palabra)
            file = ''
            if 'Bandera_Archivo' in elemento:
                dato = elemento['Bandera_Archivo']
                file = dato[1]
                cadena = self.resultadosJornada(temporada, jornada, file)
                return cadena
            else:
                cadena = self.resultadosJornada(temporada, jornada, file)
                return cadena
        elif elemento['Palabra_Reservada0'] == 'GOLES':
            palabra = elemento['Palabra_Reservada1']
            if palabra == 'LOCAL':
                equipo1 = elemento['Cadena_0']
                temporada = elemento['Fecha']
                temporada = temporada.replace('<', '')
                temporada = temporada.replace('>', '')
                cadena = self.totalDeGolesEnUnaTemporada(
                    temporada, equipo1, palabra)
                return cadena
            elif palabra == 'VISITANTE':
                equipo1 = elemento['Cadena_0']
                temporada = elemento['Fecha']
                temporada = temporada.replace('<', '')
                temporada = temporada.replace('>', '')
                cadena = self.totalDeGolesEnUnaTemporada(
                    temporada, equipo1, palabra)
                return cadena
            elif palabra == 'TOTAL':
                equipo1 = elemento['Cadena_0']
                temporada = elemento['Fecha']
                temporada = temporada.replace('<', '')
                temporada = temporada.replace('>', '')
                cadena = self.totalDeGolesEnUnaTemporada(
                    temporada, equipo1, palabra)
                return cadena
        elif elemento['Palabra_Reservada0'] == 'TABLA':
            file = ''
            if 'Bandera_Archivo' in elemento:
                temporada = elemento['Fecha']
                temporada = temporada.replace('<', '')
                temporada = temporada.replace('>', '')
                dato = elemento['Bandera_Archivo']
                file = dato[1]
                cadena = self.tablaGeneraldeTemporada(temporada, file)
                return cadena
            else:
                temporada = elemento['Fecha']
                temporada = temporada.replace('<', '')
                temporada = temporada.replace('>', '')
                cadena = self.tablaGeneraldeTemporada(temporada, file)
                return cadena
        elif elemento['Palabra_Reservada0'] == 'PARTIDOS':
            #temporadaDeUnEquipo(self, sesson, equipo, file, ji, jf)
            file = ''
            if 'Bandera_Archivo' in elemento and 'Bandera_Jornada' in elemento:
                temporada = elemento['Fecha']
                temporada = temporada.replace('<', '')
                temporada = temporada.replace('>', '')
                equipo = elemento['Cadena_0']
                dato = elemento['Bandera_Archivo']
                file = dato[1]
                datoj = elemento['Bandera_Jornada']
                ji = datoj[1]
                ji = int(ji)
                jf = datoj[3]
                jf = int(jf)
                cadena = self.temporadaDeUnEquipo(
                    temporada, equipo, file, ji, jf)
                return cadena
            elif 'Bandera_Archivo' in elemento and 'Bandera_Jornada' not in elemento:
                temporada = elemento['Fecha']
                temporada = temporada.replace('<', '')
                temporada = temporada.replace('>', '')
                equipo = elemento['Cadena_0']
                dato = elemento['Bandera_Archivo']
                file = dato[1]
                ji = 0
                jf = 0
                cadena = self.temporadaDeUnEquipo(
                    temporada, equipo, file, ji, jf)
                return cadena
            elif 'Bandera_Archivo' not in elemento and 'Bandera_Jornada' in elemento:
                temporada = elemento['Fecha']
                temporada = temporada.replace('<', '')
                temporada = temporada.replace('>', '')
                equipo = elemento['Cadena_0']
                file = ''
                datoj = elemento['Bandera_Jornada']
                ji = datoj[1]
                ji = int(ji)
                jf = datoj[3]
                jf = int(jf)
                cadena = self.temporadaDeUnEquipo(
                    temporada, equipo, file, ji, jf)
                return cadena
            else:
                temporada = elemento['Fecha']
                temporada = temporada.replace('<', '')
                temporada = temporada.replace('>', '')
                equipo = elemento['Cadena_0']
                dato = elemento['Bandera_Archivo']
                file = ''
                ji = 0
                jf = 0
                cadena = self.temporadaDeUnEquipo(
                    temporada, equipo, file, ji, jf)
                return cadena
        elif elemento['Palabra_Reservada0'] == 'TOP':
            if 'Bandera_Equipo' in elemento:
                palabra = elemento['Palabra_Reservada1']
                temporada = elemento['Fecha']
                temporada = temporada.replace('<', '')
                temporada = temporada.replace('>', '')
                dato = elemento['Bandera_Equipo']
                num = dato[1]
                num = int(num)
                cadena = self.topGoles(temporada, num, palabra)
                return cadena
            elif 'Bandera_Equipo' not in elemento:
                palabra = elemento['Palabra_Reservada1']
                temporada = elemento['Fecha']
                temporada = temporada.replace('<', '')
                temporada = temporada.replace('>', '')
                num = 0
                cadena = self.topGoles(temporada, num, palabra)
                return cadena

    def resultadoDeUnPartido(self, sesson, equipo1, equipo2):
        data = pd.read_csv('Document/LaLigaBot-LFP.csv', header=0)
        temporada = data[(data.Temporada == sesson) &
                         (data.Equipo1 == equipo1) & (data.Equipo2 == equipo2)]
        if temporada.empty:
            print('Este Resultado no existe revice Documentacion')
            answer = 'Este Resultado no existe revice Documentacion'
            return answer
        else:
            temporada = temporada.reset_index()
            temporada = temporada.drop(['index'], axis=1)
            Equipo1 = temporada["Equipo1"]
            Equipo2 = temporada["Equipo2"]
            Goles1 = temporada["Goles1"]
            Goles2 = temporada["Goles2"]
            for indice in range(0, len(temporada)):
                if Equipo1[indice] == equipo1 and Equipo2[indice] == equipo2:
                    answer = f'El resultado de este partido fue {equipo1} {Goles1[indice]} - {equipo2} {Goles2[indice]}'
                    return answer
                else:
                    answer = f'El resultado de este partido no existe!'
                    return answer

    def resultadosJornada(self, sesson, journey, file):
        jornada = dict()
        data = pd.read_csv('Document/LaLigaBot-LFP.csv', header=0)
        temporada = data[(data.Temporada == sesson)
                         & (data.Jornada == journey)]
        if temporada.empty:
            print('Temporada o Jornada no existen revice Documentacion')
            answer = 'Este Resultado no existe revice Documentacion'
            return answer
        else:
            lista_equipos = list()
            temporada = temporada.reset_index()
            temporada = temporada.drop(['index'], axis=1)
            Equipo1 = temporada["Equipo1"]
            Goles1 = temporada["Goles1"]
            Equipo2 = temporada["Equipo2"]
            Goles2 = temporada["Goles2"]
            cont = 1
            for indice in range(0, len(temporada)):
                equipo1 = Equipo1[indice]
                equipo1 = str(equipo1)
                equipo2 = Equipo2[indice]
                equipo2 = str(equipo2)
                goles1 = Goles1[indice]
                goles1 = int(goles1)
                goles2 = Goles2[indice]
                goles2 = int(goles2)
                cont = int(cont)
                lista_equipos.append(
                    [cont, equipo1, equipo2, goles1, goles2])
                cont += 1
            jornada["Jornada"] = lista_equipos
            if file != None and file != '':
                jornada["Nombre"] = file
            else:
                jornada["Nombre"] = "jornada"
                file = 'jornada'
            print(json.dumps(jornada, indent=4))
            self.sendResulTadosJornada(jornada)
            ruta = f'Reports\\Tables\\Jornada\\{file}.html'
            os.startfile(ruta)
            answer = f'Generando archivo de resultados Jornada {journey} Temporada {sesson}'
            return answer

    def sendResulTadosJornada(self, jornada):
        r = requests.post(
            'http://127.0.0.1:5000/postTablaJornada', json=jornada)
        print('> Server devolvio: ', r.status_code)

    def totalDeGolesEnUnaTemporada(self, sesson, equipo, condicion):
        data = pd.read_csv('Document/LaLigaBot-LFP.csv', header=0)
        goles1Temporada = data[(data.Temporada == sesson)
                               & (data.Equipo1 == equipo)]
        totalgoles1 = goles1Temporada["Goles1"].sum()
        goles2Temporada = data[(data.Temporada == sesson)
                               & (data.Equipo2 == equipo)]
        totalgoles2 = goles2Temporada["Goles2"].sum()
        if condicion == 'LOCAL':
            answer = f'Los goles anotados por el {equipo} en total en la temporada {sesson} fueron {totalgoles1}'
            return answer
        elif condicion == 'VISITANTE':
            answer = f'Los goles anotados por el {equipo} en total en la temporada {sesson} fueron {totalgoles2}'
            return answer
        elif condicion == 'TOTAL':
            totalgoles = totalgoles1 + totalgoles2
            answer = f'Los goles anotados por el {equipo} en total en la temporada {sesson} fueron {totalgoles}'
            return answer

    def tablaGeneraldeTemporada(self, anos, file):
        session = dict()
        data = pd.read_csv('Document/LaLigaBot-LFP.csv', header=0)
        temporada = data[(data.Temporada == anos)]
        if temporada.empty:
            print('Temporada no existen revice Documentacion')
            answer = 'Este Resultado no existe revice Documentacion'
            return answer
        else:
            lista_equipos = list()
            temporada = temporada.reset_index()
            temporada = temporada.drop(['index'], axis=1)
            Equipo1 = temporada["Equipo1"]
            Goles1 = temporada["Goles1"]
            Equipo2 = temporada["Equipo2"]
            Goles2 = temporada["Goles2"]
            for indice in range(0, len(temporada)):
                if Equipo1[indice] not in lista_equipos:
                    lista_equipos.append(Equipo1[indice])
                if Equipo2[indice] not in lista_equipos:
                    lista_equipos.append(Equipo2[indice])
            # print(lista_equipos)
            lista_T = List_Temporada()
            for element in lista_equipos:
                nuevoEquipo = Temporada(element)
                lista_T.insertar(nuevoEquipo)
            # lista_T.recorrer()
            for indice in range(0, len(temporada)):
                lista_T.golesEquipos(
                    Equipo1[indice], Goles1[indice], Equipo2[indice], Goles2[indice])
            lista = list()
            for element in lista_equipos:
                equipo = lista_T.busqueda(element)
                lista.append([equipo.equipo, equipo.puntos])
            session["Temporada"] = lista
            if file != None and file != '':
                session["Nombre"] = file
            else:
                session["Nombre"] = "temporada"
                file = "temporada"
            print(json.dumps(session, ensure_ascii=False, indent=4))
            self.sendTablaGeneraldeTemporada(session)
            ruta = f'Reports\\Tables\\Temporada\\{file}.html'
            os.startfile(ruta)
            answer = f'Generando archivo de clasificación de temporada {anos}'
            return answer

    def sendTablaGeneraldeTemporada(self, session):
        r = requests.post(
            'http://127.0.0.1:5000/postTablaTemporada', json=session)
        print('> Server devolvio: ', r.status_code)

    def temporadaDeUnEquipo(self, sesson, equipo, file, ji, jf):
        session = dict()
        data = pd.read_csv('Document/LaLigaBot-LFP.csv', header=0)
        temporada = data[(data.Temporada == sesson)
                         & (data.Equipo1 == equipo) | (data.Equipo2 == equipo)]
        if temporada.empty:
            print('Temporada o Jornada no existen revice Documentacion')
            answer = 'Este Resultado no existe revice Documentacion'
            return answer
        else:
            if ji == 0 and jf == 0:
                lista_equipos = list()
                temporada = temporada.sort_values('Jornada', ascending=True)
                temporada = temporada.reset_index()
                temporada = temporada.drop(['index'], axis=1)
                Jornada = temporada["Jornada"]
                Equipo1 = temporada["Equipo1"]
                Equipo2 = temporada["Equipo2"]
                Goles1 = temporada["Goles1"]
                Goles2 = temporada["Goles2"]
                for indice in range(0, len(temporada)):
                    equipo1 = Equipo1[indice]
                    equipo1 = str(equipo1)
                    equipo2 = Equipo2[indice]
                    equipo2 = str(equipo2)
                    goles1 = Goles1[indice]
                    goles1 = int(goles1)
                    goles2 = Goles2[indice]
                    goles2 = int(goles2)
                    jornada = Jornada[indice]
                    jornada = int(jornada)
                    lista_equipos.append(
                        [jornada, equipo1, equipo2, goles1, goles2])
                session["Resultado"] = lista_equipos
                equipo = str(equipo)
                session["Equipo"] = equipo
                if file != '':
                    session["Nombre"] = file
                else:
                    session["Nombre"] = "partidos"
                    file = 'partidos'
                print(json.dumps(session, indent=4))
                self.sendTemporadaDeUnEquipo(session)
                ruta = f'Reports\\Tables\\Temporada_Equipo\\{file}.html'
                os.startfile(ruta)
                answer = f'Generando archivo de resultados de temporada {sesson} del {equipo}'
                return answer

            else:
                list_num = list()
                lista_equipos = list()
                temporada = temporada.sort_values('Jornada', ascending=True)
                temporada = temporada.reset_index()
                temporada = temporada.drop(['index'], axis=1)
                for num in range(ji, jf+1):
                    if num in temporada.Jornada.values:
                        list_num.append("True")
                    else:
                        list_num.append("False")
                if "False" in list_num:
                    print("El Rango de la Jornada es Incorecto")
                else:
                    for num in range(ji, jf+1):
                        dato = temporada[(temporada.Jornada == num)]
                        dato = dato.reset_index()
                        dato = dato.drop(['index'], axis=1)
                        print(dato)
                        Jornada = dato["Jornada"]
                        Equipo1 = dato["Equipo1"]
                        Equipo2 = dato["Equipo2"]
                        Goles1 = dato["Goles1"]
                        Goles2 = dato["Goles2"]
                        for indice in range(0, len(dato)):
                            equipo1 = Equipo1[indice]
                            equipo1 = str(equipo1)
                            equipo2 = Equipo2[indice]
                            equipo2 = str(equipo2)
                            goles1 = Goles1[indice]
                            goles1 = int(goles1)
                            goles2 = Goles2[indice]
                            goles2 = int(goles2)
                            jornada = Jornada[indice]
                            jornada = int(jornada)
                            lista_equipos.append(
                                [jornada, equipo1, equipo2, goles1, goles2])

                    session["Resultado"] = lista_equipos
                    equipo = str(equipo)
                    session["Equipo"] = equipo
                    if file != '':
                        session["Nombre"] = file
                    else:
                        session["Nombre"] = "partidos"
                        file = 'partidos'
                    print(json.dumps(session, indent=4))
                    self.sendTemporadaDeUnEquipo(session)
                    ruta = f'Reports\\Tables\\Temporada_Equipo\\{file}.html'
                    os.startfile(ruta)
                    answer = f'Generando archivo de resultados de temporada {sesson} del {equipo}'
                    return answer

    def sendTemporadaDeUnEquipo(self, session):
        r = requests.post(
            'http://127.0.0.1:5000/postTemporadaDeUnEquipo', json=session)
        print('> Server devolvio: ', r.status_code)

    def topGoles(self, anos, num, condicion):
        session = dict()
        data = pd.read_csv('Document/LaLigaBot-LFP.csv', header=0)
        temporada = data[(data.Temporada == anos)]
        if temporada.empty:
            print('Temporada no existen revice Documentacion')
            answer = 'Este Resultado no existe revice Documentacion'
            return answer
        else:
            lista_equipos = list()
            temporada = temporada.reset_index()
            temporada = temporada.drop(['index'], axis=1)
            Equipo1 = temporada["Equipo1"]
            Goles1 = temporada["Goles1"]
            Equipo2 = temporada["Equipo2"]
            Goles2 = temporada["Goles2"]
            for indice in range(0, len(temporada)):
                if Equipo1[indice] not in lista_equipos:
                    lista_equipos.append(Equipo1[indice])
                if Equipo2[indice] not in lista_equipos:
                    lista_equipos.append(Equipo2[indice])
            # print(lista_equipos)
            lista_T = List_Temporada()
            for element in lista_equipos:
                nuevoEquipo = Temporada(element)
                lista_T.insertar(nuevoEquipo)
            # lista_T.recorrer()
            for indice in range(0, len(temporada)):
                lista_T.golesEquipos(
                    Equipo1[indice], Goles1[indice], Equipo2[indice], Goles2[indice])
            lista = list()
            for element in lista_equipos:
                equipo = lista_T.busqueda(element)
                lista.append([equipo.equipo, equipo.puntos])
            session["Temporada"] = lista
            lista_T.bubbleSort()
            lista_rango = lista_T.obtener()
            cadena = ""
            if num != 0:
                if condicion == "SUPERIOR":
                    p = 0
                    n = num
                    cadena += f"El top superior de la temporada {anos} fue:\n"
                    for nom in lista_rango[p:n]:
                        cadena += f"{nom}\n"
                elif condicion == "INFERIOR":
                    cont = 1
                    cadena += f"El top superior de la temporada {anos} fue:\n"
                    for nom in reversed(lista_rango):
                        if cont <= num:
                            cadena += f"{nom}\n"
                            cont += 1

            elif num == 0:
                num = 5
                if condicion == "SUPERIOR":
                    p = 0
                    n = num
                    cadena += f"El top superior de la temporada {anos} fue:\n"
                    for nom in lista_rango[p:n]:
                        cadena += f"{nom}\n"
                elif condicion == "INFERIOR":
                    cont = 1
                    cadena += f"El top superior de la temporada {anos} fue:\n"
                    for nom in reversed(lista_rango):
                        if cont <= num:
                            cadena += f"{nom}\n"
                            cont += 1
            return cadena


