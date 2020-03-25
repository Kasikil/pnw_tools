from bs4 import BeautifulSoup
from datetime import datetime
import math
from models.improvements import Improvements
import json
import re

COAL_POWER_PP = 8
OIL_POWER_PP = 6
BAUX_MINE_PP = 12
COAL_MINE_PP = 12
FARM_PP = 2
IRON_MINE_PP = 12
LEAD_MINE_PP = 12
OIL_WELL_PP = 12
URANIUM_MINE_PP = 20
OIL_REFINERY_PP = 32
STEEL_MILL_PP = 40
ALUMINUM_REFINERY = 40
MUNITIONS_FACTORY = 32
POLICE_STATION_PP = 1
HOSPITAL_PP = 4
RECYCLING_CENTER_PP = -70
SUBWAY_PP = -45
SHOPPING_MALL_PP = 2
STADIUM_PP = 5

SUPERMARKET_C = 0.03
BANK_C = 0.05
SHOPPING_MALL_C = 0.09
STADIUM_C = 0.12
SUBWAY_C = 0.08


class City:

    def __init__(self):
        self.name = None
        self.infra = None
        self.land = None
        self.disease = None
        self.commerce = None
        self.powered = None
        self.founded = None
        self.population = None
        self.population_density = None
        self.crime = None
        self.average_income = None
        self.pollution_index = None
        self.age = None
        self.improvements = Improvements()

        self.id = None
        self.pollution_mod = None
        self.base_pop = None
        self.equation_population_density = None
        self.age_bonus = None
        self.crime_deaths = None
        self.disease_deaths = None

    def import_city_from_id(self, session, city_id):
        self.id = city_id
        self.import_city_from_pnw(session)

    def import_city_from_pnw(self, session):
        html = session.get('https://politicsandwar.com/city/id='.format(self.id))
        city_soup = BeautifulSoup(html.text, 'html.parser')
        city_table_html = city_soup.find("table", {"class": "nationtable"})
        nation_table_list = []
        for city_row in city_table_html:
            for city_column in city_row:
                if not str(city_column).isspace():
                    nation_table_list.append(str(city_column))
        self.infra = float(nation_table_list[2][16:-5].replace(',', ''))
        self.population = int(nation_table_list[4][4:-12].replace(',', ''))
        self.land = float(nation_table_list[6][4:-18].replace(',', ''))
        self.founded = datetime.strptime(nation_table_list[-3][4:-5], '%m/%d/%Y')
        self.age = int(nation_table_list[-1][4:-10].replace(',', ''))
        if 'Yes' in nation_table_list[-7]:
            self.powered = True
        else:
            self.powered = False

        html = session.get('https://politicsandwar.com/city/improvements/export/id={}'.format(self.id))
        city_imp_json = json.loads(html.text)
        self.improvements.import_improvements_json(city_imp_json)
        self.calculations()

    def calculations(self):
        # Pollution
        self.calculate_pollution()
        self.calculate_pollution_mod()
        # Commerce
        self.calculate_commerce()
        # Base Population
        self.calculate_base_population()
        # Equation Population Density
        self.calculate_equation_population_density()
        # Age Bonus
        self.calculate_age_bonus()
        # Crime
        self.calculate_crime()
        self.calculate_crime_deaths()
        # Disease
        self.calculate_disease()
        self.calculate_disease_deaths()
        # Full Population And Density
        self.calculate_population()
        self.calculate_population_density()

    def calculate_pollution(self):
        self.pollution_index = \
            (self.improvements.imp_coalpower * COAL_POWER_PP) + \
            (self.improvements.imp_oilpower * OIL_POWER_PP) + \
            (self.improvements.imp_coalmine * COAL_MINE_PP) + \
            (self.improvements.imp_oilwell * OIL_WELL_PP) + \
            (self.improvements.imp_uramine * URANIUM_MINE_PP) + \
            (self.improvements.imp_leadmine * LEAD_MINE_PP) + \
            (self.improvements.imp_ironmine * IRON_MINE_PP) + \
            (self.improvements.imp_bauxitemine * BAUX_MINE_PP) + \
            (self.improvements.imp_farm * FARM_PP) + \
            (self.improvements.imp_gasrefinery * OIL_REFINERY_PP) + \
            (self.improvements.imp_aluminumrefinery * ALUMINUM_REFINERY) + \
            (self.improvements.imp_munitionsfactory * MUNITIONS_FACTORY) + \
            (self.improvements.imp_steelmill * STEEL_MILL_PP) + \
            (self.improvements.imp_policestation * POLICE_STATION_PP) + \
            (self.improvements.imp_hospital * HOSPITAL_PP) + \
            (self.improvements.imp_recyclingcenter * RECYCLING_CENTER_PP) + \
            (self.improvements.imp_subway * SUBWAY_PP) + \
            (self.improvements.imp_mall * SHOPPING_MALL_PP) + \
            (self.improvements.imp_stadium * STADIUM_PP)

    def calculate_pollution_mod(self):
        self.pollution_mod = self.pollution_index * 0.05

    def calculate_commerce(self):
        self.commerce = \
            (self.improvements.imp_supermarket * SUPERMARKET_C) + \
            (self.improvements.imp_bank * BANK_C) + \
            (self.improvements.imp_mall * SHOPPING_MALL_C) + \
            (self.improvements.imp_stadium * STADIUM_C) + \
            (self.improvements.imp_subway * SUBWAY_C)

    def calculate_base_population(self):
        self.base_pop = self.infra * 100

    def calculate_equation_population_density(self):
        self.equation_population_density = self.base_pop / self.land

    def calculate_age_bonus(self):
        self.age_bonus = 1 + math.log(self.age)/15

    def calculate_crime(self):
        self.crime = ((103 - self.commerce) ** 2 + (self.infra * 100)) / 11111111 - \
                     (self.improvements.imp_policestation * 2.5)

    def calculate_crime_deaths(self):
        calc_deaths = (self.crime * 10) * (self.infra * 100) - 25
        if calc_deaths < 0:
            self.crime_deaths = 0
        else:
            self.crime_deaths = calc_deaths

    def calculate_disease(self):
        self.disease = ((((self.equation_population_density ** 2) * 0.01) - 25) / 100) + \
                       (self.base_pop / 100000) + self.pollution_mod - \
                       (self.improvements.imp_hospital * 2.5)

    def calculate_disease_deaths(self):
        self.disease_deaths = (self.disease / 100) * self.base_pop

    def calculate_population(self):
        self.population = (self.base_pop - self.disease_deaths - self.crime_deaths) * self.age_bonus

    def calculate_population_density(self):
        self.population_density = self.population / self.land
