from pathlib import Path
from typing import Optional
from sqlalchemy import create_engine

DATABASE_FILE = Path(__file__).resolve().parent / "database.db"


class DatabaseEngineSingleton:
    _instance: Optional['DatabaseEngineSingleton'] = None
    engine = None

    def __new__(cls, database_url: Optional[str] = None, echo: bool = False):
        """Garantiza que solo se cree una instancia de DatabaseEngineSingleton."""
        if cls._instance is None:
            cls._instance = super(DatabaseEngineSingleton, cls).__new__(cls)
            db_url = database_url or f"sqlite:///{DATABASE_FILE.as_posix()}"
            cls.engine = create_engine(db_url, echo=echo)
            print("¡Motor de SQLAlchemy Creado por primera vez!")

        return cls._instance
