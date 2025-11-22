from datetime import datetime
from re import M

from .auto import Auto
from .mantenimiento import Mantenimiento


class RegistroMantenimiento:
    fechaInicio: str
    fechaFin: str
    auto: Auto

    def __init__(
        self,
        fechaInicio: str,
        fechaFin: str,,
        auto: Auto,
    ):
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin

        self.auto = auto

    # Hacer la consulta a base de datos para obtener todos los mantenimientos de este registro

    def calcularCostoTotal(self) -> float:
        total = 0.0
        for mantenimiento in self.mantenimientos:
            total += mantenimiento.getCosto()
        return total

    def agregarMantenimineto(self, mantenimineto: Mantenimiento):
        if datetime.strptime(mantenimineto.getFecha(), "%Y-%m-%d") >= datetime.strptime(
            self.fechaInicio, "%Y-%m-%d"
        ) and datetime.strptime(
            mantenimineto.getFecha(), "%Y-%m-%d"
        ) <= datetime.strptime(self.fechaFin, "%Y-%m-%d"):
            self.mantenimientos.append(mantenimineto)
        else:
            raise ValueError("La fecha del mantenimiento está fuera del rango del registro.")
            
            