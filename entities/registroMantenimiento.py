from mantenimiento import Mantenimiento
from auto import Auto


class RegistroMantenimiento(Mantenimiento):
  fechaInicio: str
  fechaFin: str
  mantenimientos: list[Mantenimiento]
  auto: Auto
  
  def __init__(self, fechaInicio: str, fechaFin: str, mantenimientos: list[Mantenimiento], auto: Auto):
    self.fechaInicio = fechaInicio
    self.fechaFin = fechaFin
    self.mantenimientos = mantenimientos
    self.auto = auto