import sqlite3

conn = sqlite3.connect('./db/database.db')
cursor = conn.cursor()

# Ejecutar una consulta
cursor.execute("DROP TABLE IF EXISTS Seguros")

# Obtener los resultados

conn.close()