import forces
from datetime import date

mil_base = 4.5
dyd_base = 2.5


class Mil:
		
	def __init__(self, init_date, prod_eff, prod_cap, fact_out):
		self.init_date = init_date
		self.prod_eff = prod_eff
		self.prod_cap = prod_cap
		self.fact_out = fact_out
		self.at_prod_cap = False
		
	def daily_prod(self):
		output_IC = self.fact_out * self.prod_eff * mil_base
		self.prod_eff_daily_gain()
		return output_IC
		
	def prod_eff_daily_gain(self):
		if self.at_prod_cap == False:
			self.prod_eff = self.prod_eff + 0.001 * self.prod_cap ** 2 / self.prod_eff
			if self.prod_eff > self.prod_cap:
				self.prod_eff = self.prod_cap
				self.at_prod_cap = True


class Dyd:

	def __init__(self, init_date, dyd_out) -> None:
		self.init_date = init_date
		self.dyd_out = dyd_out

	def daily_prod(self):
		output_IC = self.dyd_out * dyd_base
		return output_IC


class Economy:
		
	def __init__(self, date, mils_max, mils_base, dyds, base_prod, prod_cap, fact_out, dyd_out, bonus_sched):
		self.date = date
		self.base_prod = base_prod
		self.prod_cap = prod_cap
		self.fact_out = fact_out
		self.mils = []
		self.new_mils(mils_max, 'max')
		self.new_mils(mils_base)
		self.dyd_out = dyd_out
		self.dyds = []


	def new_mils(self, num_of_mils, curr_prod_eff=None):
		prod_eff = self.prod_cap if curr_prod_eff == 'max' else self.base_prod
		for x in range(num_of_mils):
			self.mils.append(Mil(self.date, prod_eff, self.prod_cap, self.fact_out))

	def new_dyds(self, num_of_dyds):
		for x in range(num_of_dyds):
			self.dyds.append(Dyd(self.date, self.dyd_out))
			
	def advance_day(self):
		pass						
