from typing import Optional
from sqlalchemy import create_engine

class DatabaseEngineSingleton:
    # 1. Variable de clase para contener la única instancia del Singleton
    _instance: Optional['DatabaseEngineSingleton'] = None
    
    # 2. Variable para almacenar el motor de SQLAlchemy
    engine = None

    def __new__(cls, database_url: str = "sqlite:///db/database.db", echo: bool = True):
        """
        Garantiza que solo se cree una instancia de DatabaseEngineSingleton.
        """
        # Si la instancia única aún no ha sido creada
        if cls._instance is None:
            # Llama al __new__ del padre (object) para crear la nueva instancia
            cls._instance = super(DatabaseEngineSingleton, cls).__new__(cls)
            
            # Inicializa el motor de SQLAlchemy SOLO en la primera creación
            cls.engine = create_engine(database_url, echo=echo)
            print("¡Motor de SQLAlchemy Creado por primera vez!")
            
        # Siempre retorna la única instancia existente
        return cls._instance
