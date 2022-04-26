class Error():
    def __init__(self, fila: int, col: int, caracter: str, tipo:str) -> None:
        self.fila = fila
        self.col = col
        self.caracter = caracter
        self.tipo = tipo

    def toString(self) -> str:
        c = self.caracter.replace('\n', r'\n')
        return f'en: ({str(self.tipo)}, {str(self.fila)}, {str(self.col)}) -> " {c} "'
