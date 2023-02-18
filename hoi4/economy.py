con_costs = {
    'CIV': 10800,
    'MIL': 7200,
    'DYD': 6400,
    'SYNR': 14500,
    'FUEL': 5000,
    'ROCK': 6400,
    'NUKE': 30000
}

research = {

}

class Economy:

    def __init__(self, Production, Construction, Naval_Production) -> None:
        self.prod = Production
        self.cons = Construction
        self.navp = Naval_Production

    def change_date(self):
        pass


class Production(Economy):
    pass

class Construction(Economy):
    pass

class Naval_Production(Economy):
    pass

