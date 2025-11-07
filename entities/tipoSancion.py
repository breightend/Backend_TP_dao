class TipoSancion:
    nombre: str
    años: int

    def __init__(self, nombre: str, años: int):
        self.nombre = nombre
        self.años = años

    def getNombre(self) -> str:
        return self.nombre

    def setNombre(self, nombre: str):
        self.nombre = nombre

    def getAños(self) -> int:
        return self.años

    def setAños(self, años: int):
        self.años = años
