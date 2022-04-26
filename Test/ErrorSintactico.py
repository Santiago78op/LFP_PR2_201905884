class ErrorSintactico():
    def __init__(self, caracter: str, descripcion: str, tipo: str) -> None:
        self.caracter = caracter
        self.tipo = tipo
        self.descripcion = descripcion

    def toString(self) -> str:
        c = self.caracter.replace('\n', r'\n')
        return f'Error: {str(self.caracter)} {str(self.descripcion)}: {str(self.tipo)}'
