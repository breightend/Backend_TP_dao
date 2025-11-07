from estado import Estado
from tipoDaño import TipoDaño


class Daño:
    fecha: str
    gravedad: int
    estado: Estado
    tipoDaño: TipoDaño

    def __init__(self, fecha: str, gravedad: int, estado: Estado, tipoDaño: TipoDaño):
        self.fecha = fecha
        self.estado = estado
        self.tipoDaño = tipoDaño

        if gravedad < 1:
            self.gravedad = 1
        elif gravedad > 5:
            self.gravedad = 5
        else:
            self.gravedad = gravedad

    def getFecha(self) -> str:
        return self.fecha

    def getGravedad(self) -> int:
        return self.gravedad

    def getEstado(self) -> Estado:
        return self.estado

    def getTipoDaño(self) -> TipoDaño:
        return self.tipoDaño

    def calcularCostoTotal(self):
        return int(self.tipoDaño.getCostoBase() * (1 + self.gravedad / 10))

    def actualizarEstado(self, nuevoEstado: Estado):
        self.estado = nuevoEstado
