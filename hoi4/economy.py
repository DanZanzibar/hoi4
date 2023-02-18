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
		
		def __init__(self, date, mils, civs, dyards, resources, fact_out, prod_cap):
				self.date = date
				self.resources = resources
				self.fact_out = fact_out
				self.prod_cap = prod_cap
				
		def advance_date(self, new_date):
				self.date = new_date
				
		def daily_prod(self):
				for mil in mils:
						
		
		
class Mil(Economy):
		
		def __init__(self, equipment, prod_eff):
				self.equip = equipment
				self.prod_eff = prod_eff
			
		def daily_prod(self):
				output_IC = Economy.fact_out * self.prod_eff * mil_base
				equip_cost = self.equip.get_IC()
				output_equip = output_IC / equip_cost
				self.prod_eff_daily_gain()
				return self.equip, output_equip
			
		def prod_eff_daily_gain(self):
				pass
