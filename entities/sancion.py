from tipoSancion import TipoSancion
from daño import Daño

class Sancion:
  
    fecha: str
    tipo: TipoSancion
    daños: list[Daño]
    
    def __init__(self, fecha: str, tipo: TipoSancion, daños: list[Daño]):
        self.fecha = fecha
        self.tipo = tipo
        self.daños = daños
    
    def calcularCostoTotal(self) -> float:
        costoTotalDaños = sum(daño.calcularCostoTotal() for daño in self.daños)
        return costoTotalDaños

    def tiempoDeSancion(self) -> int:
        return self.tipo.getAños()
    
   
