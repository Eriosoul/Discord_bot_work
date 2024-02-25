import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error
from typing import List
from countries_of_the_world.templates.lib.data_country import Country
from countries_of_the_world.templates.countries_world import CountriesOfWorld
class DataBaseCountry:
    def __init__(self):
        load_dotenv()
        host = os.getenv("HOST")
        port = os.getenv("PORT")
        user = os.getenv("USER")
        psw = os.getenv("PASSWORD")
        database = os.getenv("DATABASE")
        self.conn: mysql = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password= psw,
            database= database,
        )
        self.data_content = CountriesOfWorld()
        # self.insert_data = InsetDataCountry.insert_data(
        #     data=[Country.country_name, Country.capital, Country.population, Country.area])

    def get_connection(self, data_content: List[Country]):
        try:
            if self.conn.is_connected():
                print("Conexion establecida...")
                info_server = self.conn.get_server_info()
                print("Informaciond el servido: ", info_server)
                # comprobar que la db exista
                cursor = self.conn.cursor()
                cursor.execute("show tables like 'paises_del_los_mundos'")
                result = cursor.fetchone()
                if result:
                    print("la tabla 'paises_del_los_mundos' exite")
                    self.insert_data(data_content)
                else:
                    print("La tabla no existe 'paises_del_los_mundos'. Creando tabla...")
                    self.creating_table()
        except Error as err:
            print("Error a la hora de realizar la conexion con bases de datos : {0}".format(err))
            return None

    def creating_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS paises_del_los_mundos(
                    _id INT AUTO_INCREMENT PRIMARY KEY,
                    p_pais VARCHAR(50),
                    p_nombre VARCHAR(50),
                    p_poblacion INT(50),
                    p_area FLOAT(50)
                )
            ''')
            print("\nTabla 'paises_del_los_mundos' creada exitosamente.\n")

            # comprobamos los datos en la tabla de la base de datos
            cursor.execute('SELECT COUNT(*) FROM paises_del_los_mundos')
            total_count = cursor.fetchone()[0]
            print(f'Total records in paises_del_los_mundos table: {total_count}')
        except Error as ex:
            print("Error al crear la tabla:", ex)
    def insert_data(self, data: List[Country]):
        try:
            for entry in data:
                cursor = self.conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM paises_del_los_mundos WHERE p_pais=%s AND p_nombre=%s',
                               (entry.country_name, entry.capital))
                existing_count = cursor.fetchone()[0]
                if existing_count == 0:
                    cursor.execute('''
                    INSERT INTO `paises_del_los_mundos`(`p_pais`, `p_nombre`, `p_poblacion`, `p_area`) 
                    VALUES (%s, %s, %s, %s)
                    ''', (entry.country_name, entry.capital, entry.population, entry.area))
                    print(f"Datos chequeados e insertandose {entry.country_name, entry.capital}")
                else:
                    print(f"Este dato ya se encuenta en la base de datos: {entry.country_name}")
            self.conn.commit()
            print("Datos insertados exitosamente.")
        except Error as ex:
            print("Error: ", ex)
            return None

def main_db():
    db: DataBaseCountry = DataBaseCountry()
    c = CountriesOfWorld()
    sp = c.get_status()
    if sp:
        data_content = c.get_data(sp)
        db = DataBaseCountry()
        db.get_connection(data_content)
