class Auto:
    marca: str
    modelo: str
    anio: int
    color: str
    costo: float
    patente: str
    periodicidadMantenimineto: int

    def __init__(
        self,
        marca: str,
        modelo: str,
        anio: int,
        color: str,
        costo: float,
        patente: str,
        periodicidadMantenimineto: int,
    ):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.color = color
        self.costo = costo
        self.patente = patente
        self.periodicidadMantenimineto = periodicidadMantenimineto

    def mostrar_informacion(self):
        return f"{self.marca} {self.modelo}, Año: {self.anio}, Color: {self.color}, Costo: ${self.costo}, Patente: {self.patente}, Periodicidad Mantenimiento: {self.periodicidadMantenimineto} meses"
