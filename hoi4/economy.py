civ_base = 5
mil_base = 4.5
dyd_base = 2.5

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


class Mil:
		
	def __init__(self, equipment, prod_eff, prod_cap, fact_out):
		self.equip = equipment
		self.prod_eff = prod_eff
		self.prod_cap = prod_cap
		self.fact_out = fact_out
		self.at_prod_cap = False
		
	def daily_prod(self):
		output_IC = self.fact_out * self.prod_eff * mil_base
		equip_cost = self.equip.get_IC()
		output_equip = output_IC / equip_cost
		self.prod_eff_daily_gain()
		return self.equip, output_equip
		
	def prod_eff_daily_gain(self):
		if self.at_prod_cap == False:
			self.prod_eff = self.prod_eff + 0.001 * self.prod_cap ** 2 / self.prod_eff
			if self.prod_eff > self.prod_cap:
				self.prod_eff = self.prod_cap
				self.at_prod_cap = True


class Economy:
		
	def __init__(self, date, mils, dyds, resources, stockpile, fact_out, prod_cap, base_prod_eff):
		self.date = date
		self.mils = []
		for entry in mils:
			self.new_mils(*entry)
		self.dyds = dyds
		self.resources = resources
		self.stockpile = stockpile
		self.fact_out = fact_out
		self.prod_cap = prod_cap
		self.base_prod_eff = base_prod_eff

	def new_mils(self, num_of_mils, equip, curr_prod_eff=None):
		for x in range(num_of_mils):
			if curr_prod_eff:
				prod_eff = self.prod_cap if curr_prod_eff == 'max' else curr_prod_eff
			else:
				prod_eff = self.base_prod_eff
			self.mils.append(Mil(equip, prod_eff, self.prod_cap, self.fact_out))

	# def new_dyds(self, num_of_dyds, equip):
	# 	for x in range(num_of_dyds):
	# 		self.dyds.append(Dyd)

	# def add_factories(self):
			
	def advance_day(self):
		self.add_bonuses()
		self.add_factories()

						
