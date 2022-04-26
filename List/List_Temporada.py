from Node.Node_Temporada import Nodo_Temporada


class List_Temporada():

    def __init__(self, nodecount=0):
        self.head = None  # self.estar_node = None
        self.nodecount = nodecount

    def insertar(self, nuevoEquipo):
        if self.head is None:
            self.head = Nodo_Temporada(data=nuevoEquipo)
            self.nodecount = self.nodecount + 1
            return  # Si cumple la condicion, sale del if y cumple la funcion
        actual = self.head
        while actual.siguiente:  # Devuelve True si el siguiente no es vacio, si es vacio sale del ciclo
            actual = actual.siguiente
        actual.siguiente = Nodo_Temporada(data=nuevoEquipo)
        self.nodecount = self.nodecount + 1

    def busqueda(self, equipo):
        if self.head is None:
            return
        actual = self.head
        while actual is not None:
            if actual.data.equipo == equipo:
                return actual.data
            actual = actual.siguiente
        return None

    def recorrer(self):
        actual = self.head
        while actual != None:
            print("Equipo:", actual.data.equipo, "Goles:",
                  actual.data.goles, "Puntos:", actual.data.puntos)
            actual = actual.siguiente

    def puntosEquipo(self, equipo1, equipo2):
        if self.head is None:
            return
        actual = self.head
        while actual is not None:
            if actual.data.equipo == equipo1:
                Equipo1 = actual.data
                Equipo2 = self.busqueda(equipo2)
                if Equipo1.goles > Equipo2.goles:
                    Equipo1.puntos = Equipo1.puntos + 3
                    Equipo2.puntos = Equipo2.puntos + 0
                elif Equipo1.goles < Equipo2.goles:
                    Equipo1.puntos = Equipo1.puntos + 0
                    Equipo2.puntos = Equipo2.puntos + 3
                elif Equipo1.goles == Equipo2.goles:
                    Equipo1.puntos = Equipo1.puntos + 1
                    Equipo2.puntos = Equipo2.puntos + 1
            actual = actual.siguiente
        return None

    def golesEquipos(self, equipo1, goles1, equipo2, goles2):
        if self.head is None:
            return
        actual = self.head
        while actual is not None:
            if actual.data.equipo == equipo1:
                Equipo1 = actual.data
                Equipo2 = self.busqueda(equipo2)
                Equipo1.goles = goles1
                Equipo2.goles = goles2
                self.puntosEquipo(equipo1, equipo2)
            actual = actual.siguiente
        return None

    def bubbleSort(self):
        for i in range(self.nodecount-1):
            curr = self.head
            nxt = curr.siguiente
            prev = None
            while nxt:
                if curr.data.puntos < nxt.data.puntos:
                    if prev == None:
                        prev = curr.siguiente
                        nxt = nxt.siguiente
                        prev.siguiente = curr
                        curr.siguiente = nxt
                        self.head = prev
                    else:
                        temp = nxt
                        nxt = nxt.siguiente
                        prev.siguiente = curr.siguiente
                        prev = temp
                        temp.siguiente = curr
                        curr.siguiente = nxt
                else:
                    prev = curr
                    curr = nxt
                    nxt = nxt.siguiente
            i = i+1

    def obtener(self):            
        actual = self.head
        lista_puntos = list()
        while actual != None:
            lista_puntos.append(actual.data.equipo)
            actual = actual.siguiente
        return lista_puntos
