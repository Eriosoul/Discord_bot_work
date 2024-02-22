import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from typing import List
from dataclasses import dataclass

@dataclass
class Country:
    country_name: str
    capital: str
    population: int
    area: float

class CountriesOfWorld:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("LINK")

    def get_status(self):
        try:
            r = requests.get(self.url)
            if r.status_code != 200:
                print(r.status_code)
                raise
            sp = BeautifulSoup(r.text, "html.parser")
            return sp
        except Exception as e:
            print(e)
            return None

    def get_data(self, sp) -> List[Country]:
        countries_data = []
        countries_rows = sp.find_all("div", class_="row")
        for row in countries_rows:
            country_name_data = row.find("h3", class_="country-name")
            if country_name_data:
                country_name = country_name_data.text.strip()
            else:
                country_name = "Unknown"

            data = row.find("div", class_="country-info")
            if data:
                capital_element = data.find("span", class_="country-capital")
                if capital_element:
                    capital = capital_element.get_text(strip=True)
                else:
                    capital = "Unknown"

                population_element = data.find("span", class_="country-population")
                if population_element:
                    population = int(population_element.get_text(strip=True))
                else:
                    population = 0

                area_element = data.find("span", class_="country-area")
                if area_element:
                    area = float(area_element.get_text(strip=True))
                else:
                    area = 0.0

                country = Country(country_name, capital, population, area)
                countries_data.append(country)
        return countries_data


def main():
    c: CountriesOfWorld = CountriesOfWorld()
    sp = c.get_status()
    if sp:
        data = c.get_data(sp)
        for country in data:
            print(country)
