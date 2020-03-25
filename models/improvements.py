class Improvements:

    def __init__(self):
        self.infra_needed = 0
        self.imp_total = 0
        self.imp_coalpower = 0
        self.imp_oilpower = 0
        self.imp_windpower = 0
        self.imp_nuclearpower = 0
        self.imp_coalmine = 0
        self.imp_oilwell = 0
        self.imp_uramine = 0
        self.imp_leadmine = 0
        self.imp_ironmine = 0
        self.imp_bauxitemine = 0
        self.imp_farm = 0
        self.imp_gasrefinery = 0
        self.imp_aluminumrefinery = 0
        self.imp_munitionsfactory = 0
        self.imp_steelmill = 0
        self.imp_policestation = 0
        self.imp_hospital = 0
        self.imp_recyclingcenter = 0
        self.imp_subway = 0
        self.imp_supermarket = 0
        self.imp_bank = 0
        self.imp_mall = 0
        self.imp_stadium = 0
        self.imp_barracks = 0
        self.imp_factory = 0
        self.imp_hangars = 0
        self.imp_drydock = 0

        self.improvement_upkeep = 0  # Per Turn
        self.daily_upkeep_cost = 0  # Per Day

        self.coal_net_production = None
        self.oil_net_production = None
        self.uranium_net_production = None
        self.lead_net_production = None
        self.iron_net_production = None
        self.bauxite_net_production = None
        self.gasoline_net_production = None
        self.munitions_net_production = None
        self.steel_net_production = None
        self.aluminum_net_production = None
        self.food_net_production = None

    def import_improvements_json(self, city_improvements_json):
        self.infra_needed = city_improvements_json['infra_needed']
        self.imp_total = city_improvements_json['imp_total']
        self.imp_coalpower = city_improvements_json['imp_coalpower']
        self.imp_oilpower = city_improvements_json['imp_oilpower']
        self.imp_windpower = city_improvements_json['imp_windpower']
        self.imp_nuclearpower = city_improvements_json['imp_nuclearpower']
        self.imp_coalmine = city_improvements_json['imp_coalmine']
        self.imp_oilwell = city_improvements_json['imp_oilwell']
        self.imp_uramine = city_improvements_json['imp_uramine']
        self.imp_leadmine = city_improvements_json['imp_leadmine']
        self.imp_ironmine = city_improvements_json['imp_ironmine']
        self.imp_bauxitemine = city_improvements_json['imp_bauxitemine']
        self.imp_farm = city_improvements_json['imp_farm']
        self.imp_gasrefinery = city_improvements_json['imp_gasrefinery']
        self.imp_aluminumrefinery = city_improvements_json['imp_aluminumrefinery']
        self.imp_munitionsfactory = city_improvements_json['imp_munitionsfactory']
        self.imp_steelmill = city_improvements_json['imp_steelmill']
        self.imp_policestation = city_improvements_json['imp_policestation']
        self.imp_hospital = city_improvements_json['imp_hospital']
        self.imp_recyclingcenter = city_improvements_json['imp_recyclingcenter']
        self.imp_subway = city_improvements_json['imp_subway']
        self.imp_supermarket = city_improvements_json['imp_supermarket']
        self.imp_bank = city_improvements_json['imp_bank']
        self.imp_mall = city_improvements_json['imp_mall']
        self.imp_stadium = city_improvements_json['imp_stadium']
        self.imp_barracks = city_improvements_json['imp_barracks']
        self.imp_factory = city_improvements_json['imp_factory']
        self.imp_hangars = city_improvements_json['imp_hangars']
        self.imp_drydock = city_improvements_json['imp_drydock']

        self.calculate_improvement_upkeep()
        self.calculate_net_resources()

    def calculate_net_resources(self):
        self.calculate_production_bonus()
        pass

    def calculate_production_bonus(self, number_of_improvements, max_slots):
        """
        max is 5 per city instead of like
        6, 12 or 10 =(round((1 + (0.5(B41 - 1) / 5))B410.25, 2))12
        so i think we take this formula and change the 5 to 4
        """
        pass

    def calculate_improvement_upkeep(self):
        self.improvement_upkeep = self.imp_coalpower * 100 + \
            self.imp_oilpower * 150 + \
            self.imp_nuclearpower * 875 + \
            self.imp_windpower * 42 + \
            self.imp_coalmine * (400 / 12) + \
            self.imp_oilwell * 50 + \
            self.imp_uramine * (5000 / 12) + \
            self.imp_leadmine * (1500 / 12) + \
            self.imp_ironmine * (1600 / 12) + \
            self.imp_bauxitemine * (1600 / 12) + \
            self.imp_farm * (300 / 12) + \
            self.imp_gasrefinery * (4000 / 12) + \
            self.imp_steelmill * (4000 / 12) + \
            self.imp_aluminumrefinery * (2500 / 12) + \
            self.imp_munitionsfactory * (3500 / 12) + \
            self.imp_policestation * (750 / 12) + \
            self.imp_hospital * (1000 / 12) + \
            self.imp_recyclingcenter * (2500 / 12) + \
            self.imp_subway * (3250 / 12) + \
            self.imp_supermarket * (600 / 12) + \
            self.imp_bank * (1800 / 12) + \
            self.imp_mall * (5400 / 12) + \
            self.imp_stadium * (12150 / 12)
        self.daily_upkeep_cost = 12 * self.improvement_upkeep


