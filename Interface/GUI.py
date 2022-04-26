from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename
import os
import json
from click import command
import requests

# ? librerias internas
from Test.Lexico import Lexico
from Test.Sintactico import Sintactico
from Data.Analisis_CSV import CSV

BG_GRAY = "#ABB2B9"
BG_COLOR = "#36648B"
TEXT_COLOR = "#EAECEE"
CONT_COLOR = "#A0522D"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class GUI():

    def __init__(self) -> None:
        self.tokens = dict()
        self.lista_tokens = list()
        self.errores = dict()
        self.erroresSintacticos = dict()
        self.lista_errores = list()
        self.lista_erroresSintacticos = list()
        self.raiz = Tk()
        self._setup_mian_window()

    def run(self):
        self.raiz.mainloop()

    def _setup_mian_window(self):
        self.raiz.title("La Liga Bot")
        self.raiz.geometry("1000x550")
        self.raiz.rowconfigure(0, weight=1)
        self.raiz.columnconfigure(0, weight=1)

        mainframe = ttk.Frame(self.raiz)
        mainframe.grid(row=0, column=0, sticky=NSEW)
        mainframe.columnconfigure(1, weight=1)
        mainframe.rowconfigure(2, weight=1)

        # Encabezado
        headFrame = ttk.Frame(mainframe, borderwidth=5, relief="ridge")
        headFrame.grid(row=1, column=1, sticky=EW)
        headFrame.columnconfigure(1, weight=1)

        headLabel = tk.Label(headFrame, bg=BG_COLOR, fg=TEXT_COLOR,
                             text="Bot La Liga XD", font=FONT_BOLD, pady=10)
        headLabel.grid(row=1, column=1, sticky=NSEW)

        headline = Label(headFrame, bg=BG_GRAY)
        headline.grid(row=2, column=1, sticky=NSEW)

        # Cuerpo
        bodyFrame = ttk.Frame(mainframe, borderwidth=5, relief="ridge")
        bodyFrame.grid(row=2, column=1, sticky=NSEW)
        bodyFrame.columnconfigure(1, weight=2)
        bodyFrame.rowconfigure(1, weight=1)

        # Cuerpo Izquierda
        self.bodyText = tk.Text(bodyFrame, width=20, height=2,
                                bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5, pady=5)
        self.bodyText.grid(row=1, column=1, sticky=NSEW)
        self.bodyText.configure(cursor="arrow", state=DISABLED)

        scrollbar = Scrollbar(self.bodyText)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.bodyText.yview)

        # Cuerpo Derecha
        bodyButtons = tk.Frame(bodyFrame, bg=CONT_COLOR,
                               borderwidth=5, relief="ridge")
        bodyButtons.grid(row=1, column=2, sticky=NSEW)

        reportBugs = tk.Button(
            bodyButtons, text='Reporte de errores', font=FONT_BOLD, bg=BG_GRAY, command=lambda: self.ejecution())
        reportBugs.grid(row=1, column=1, sticky=EW)

        cleanBogs = tk.Button(
            bodyButtons, text='Limpiar log de errores', font=FONT_BOLD, bg=BG_GRAY, command=lambda: self.cleanLogErrors())
        cleanBogs.grid(row=2, column=1, sticky=EW)

        reportTokens = tk.Button(
            bodyButtons, text='Reporte de tokens', font=FONT_BOLD, bg=BG_GRAY, command=lambda: self.ejecutionToken())
        reportTokens.grid(row=3, column=1, sticky=EW)

        cleanTokens = tk.Button(
            bodyButtons, text='Limpiar log de tokens', font=FONT_BOLD, bg=BG_GRAY, command=lambda: self.cleanLogTokens())
        cleanTokens.grid(row=4, column=1, sticky=EW)

        manualUser = tk.Button(
            bodyButtons, text='Manual de usuario', font=FONT_BOLD, bg=BG_GRAY, command=lambda: self.openUsuario())
        manualUser.grid(row=5, column=1, sticky=EW)

        manualTech = tk.Button(
            bodyButtons, text='Manual técnico', font=FONT_BOLD, bg=BG_GRAY, command=lambda: self.openTecnico())
        manualTech.grid(row=6, column=1, sticky=EW)

        # Pie
        footFrame = ttk.Frame(mainframe, borderwidth=5, relief="ridge")
        footFrame.grid(row=3, column=1, sticky=EW)
        footFrame.columnconfigure(1, weight=1)

        # Pie message entry box
        self.msgEntry = tk.Entry(footFrame, bg="#2C3E50",
                                 fg=TEXT_COLOR, font=FONT)
        self.msgEntry.place(relwidth=0.74, relheight=0.06,
                            rely=0.008, relx=0.011)
        self.msgEntry.focus()
        self.msgEntry.bind("<Return>")
        self.msgEntry.grid(row=1, column=1, sticky=NSEW)

        # Pie send button
        sendButton = tk.Button(footFrame, text="Enviar", font=FONT_BOLD, bg=BG_GRAY,
                               command=lambda: self._on_enter_pressed(None))
        sendButton.grid(row=1, column=2, sticky=NSEW)

    def _on_enter_pressed(self, event):
        msg = self.msgEntry.get()
        self._insert_message(msg, "You")

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msgEntry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.bodyText.configure(state=NORMAL)
        self.bodyText.insert(END, msg1)
        self.bodyText.configure(state=DISABLED)

        if msg == 'ADIOS':
            respuesta = 'ADIOS'
            bot_name = "Julián"
            msg2 = f"{bot_name}: {respuesta}\n\n"
            self.bodyText.configure(state=NORMAL)
            self.bodyText.insert(END, msg2)
            self.bodyText.configure(state=DISABLED)

            self.bodyText.see(END)
        else:
            bot_name = "Julián"
            respuesta = self.readInfo(msg)
            msg2 = f"{bot_name}: {respuesta}\n\n"
            self.bodyText.configure(state=NORMAL)
            self.bodyText.insert(END, msg2)
            self.bodyText.configure(state=DISABLED)

            self.bodyText.see(END)

        if respuesta == 'ADIOS':
            self.raiz.destroy()

    def readInfo(self, entrada):
        if entrada != '':
            self.lex = Lexico()
            self.lex.escanear(entrada)
            if len(self.lex.errores) == 0:
                # for img in self.lex.imgs:
                #     print(json.dumps(img, indent=4))
                for elemento in self.lex.tokens:
                    id = elemento.id
                    lex = elemento.valor
                    valor = lex.valor
                    fila = lex.fila
                    columna = lex.col
                    self.lista_tokens.append([id, valor, fila, columna])
                self.tokens['tokens'] = self.lista_tokens
                print(json.dumps(self.tokens, indent=4))
                # ? Fase Analisis Sintactico
                self.sic = Sintactico(self.lex.tokens)
                if len(self.sic.errores) == 0:
                    print(self.sic.answer)
                else:
                    print('\t---ERRORES--SINTACTICOS---')
                    cadena = 'Se produjeron Algunos Errores ERRORES--SINTACTICOS en: \n'
                    for e in self.sic.errores:
                        cadena += f'"->", {e.toString()}, \n'
                        caracter = e.caracter
                        descripcion = e.descripcion
                        tipo = e.tipo
                        self.lista_erroresSintacticos.append(
                            [caracter, descripcion, tipo])
                    self.erroresSintacticos['erroresSintacticos'] = self.lista_erroresSintacticos
                    print(json.dumps(self.erroresSintacticos, indent=4))
                    return cadena
            else:
                print('\t---ERRORES--LEXICOS---')
                cadena = 'Se produjeron Algunos Errores ERRORES--LEXICOS en: \n'
                for e in self.lex.errores:
                    cadena += f'"->", {e.toString()}, \n'
                    print(">", e.toString(), sep=" ")
                    tipo = e.tipo
                    fil = e.fila
                    col = e.col
                    caracter = e.caracter
                    self.lista_errores.append(
                        [tipo, fil, col, caracter])
                self.errores['errores'] = self.lista_errores
                print(json.dumps(self.errores, indent=4))
                return cadena
            if len(self.lex.errores) == 0 and len(self.sic.errores) == 0:
                for img in self.lex.imgs:
                    print(json.dumps(img, indent=4))
                    csv = CSV()
                    cadena = csv.Match(img)
                    return cadena

    def cleanLogErrors(self):
        self.errores.clear()
        self.lista_errores.clear()
        self.erroresSintacticos.clear()
        self.lista_erroresSintacticos.clear()

    def cleanLogTokens(self):
        self.tokens.clear()
        self.lista_tokens.clear()

    def ejecution(self):
        condicion_1 = self.is_empty_Errors()
        condicion_2 = self.is_empty_ErrorsSic()
        if condicion_1 == 'False':
            self.sendErrores()
            ruta = 'Reports\\Errors\\errores.html'
            os.startfile(ruta)
        if condicion_2 == 'False':
            self.sendErroresSic()
            ruta = 'Reports\\Errors\\erroresSic.html'
            os.startfile(ruta)

    def is_empty_Errors(self):
        if self.errores:
            return 'False'
        else:
            return 'True'

    def is_empty_ErrorsSic(self):
        if self.erroresSintacticos:
            return 'False'
        else:
            return 'True'

    def ejecutionToken(self):
        if self.tokens:
            self.sendTokens()
            ruta = 'Reports\\Tokens\\tokens.html'
            os.startfile(ruta)
        else:
            return 'True'

    def openUsuario(self):
        ruta = 'Document\\Manual de Usuario.pdf'
        os.startfile(ruta)

    def openTecnico(self):
        ruta = 'Document\\Manual Tecnico.pdf'
        os.startfile(ruta)

    def sendErrores(self):
        requests.post('http://127.0.0.1:5000/postErrores', json=self.errores)

    def sendErroresSic(self):
        requests.post('http://127.0.0.1:5000/postErroresSic',
                      json=self.erroresSintacticos)

    def sendTokens(self):
        r = requests.post('http://127.0.0.1:5000/postTokens', json=self.tokens)
        print('> Server devolvio: ', r.status_code)
