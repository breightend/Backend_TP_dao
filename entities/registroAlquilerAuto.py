import string
from typing import List
from cliente import Cliente
from empleado import Empleado
from auto import Auto
from sancion import Sancion

class RegistroAlquilerAuto:
  fechaInicio: string
  fechaFin: string
  costoPorDia: float
  cantidadDias: int
  cliente: Cliente
  empleado: Empleado
  auto: Auto
  sanciones: List[Sancion]
  
  def __init__(self, fechaInicio: string, costoPorDia: float, cantidadDias: int, cliente: Cliente, empleado: Empleado, auto: Auto) -> None:
    self.fechaInicio = fechaInicio
    self.fechaFin = ""
    self.costoPorDia = costoPorDia
    self.cantidadDias = cantidadDias
    self.cliente = cliente
    self.empleado = empleado
    self.auto = auto
    self.sanciones = []
  
  def finalizarAlquiler(self):
    self.fechaInicio = datetime.now().strftime("%Y/%m/%d")
  
  def calcularCostoTotal(self):
    pass
    
  def calcularCostoSanciones(self):
    pass