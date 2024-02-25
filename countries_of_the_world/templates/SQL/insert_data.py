from typing import List
from mysql.connector import Error
from connection_db import DataBaseCountry
from countries_of_the_world.templates.lib.data_country import Country


class InsetDataCountry:
    def __init__(self):
        self.cursor = DataBaseCountry()

    def insert_data(self, data: List[Country]):
        try:
            for entry in data:
                cursor = self.cursor.conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM paises_del_mundo WHERE p_pais=%s AND p_nombre=%s',
                               (entry.country_name, entry.capital))
                existing_count = cursor.fetchone()[0]
                if existing_count == 0:
                    cursor.execute('''
                    INSERT INTO `paises_del_mundo`(`_id`, `p_pais`, `p_nombre`, `p_poblacion`, `p_area`) 
                    VALUES (%s, %s, %s, %s, %s)
                    ''', (entry.country_name, entry.capital, entry.population, entry.area))
                    print(f"Datos chequeados e insertandose {entry.country_name, entry.capital}")
                else:
                    print("datos no repetidos")
            self.cursor.conn.commit()
            print("Datos insertados exitosamente.")
        except Error as ex:
            print("Error: ", ex)
            return None
