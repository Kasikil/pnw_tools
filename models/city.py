import requests


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

        self.id = None

    def import_city_from_id(self, id):
        self.id = id


