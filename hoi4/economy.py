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
		self.produced = 0
		
	def daily_prod(self):
		output_IC = self.fact_out * self.prod_eff * mil_base
		self.prod_eff_daily_gain()
		self.produced += output_IC
		
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
		self.produced = 0

	def daily_prod(self):
		output_IC = self.dyd_out * dyd_base
		self.produced += output_IC


class Production:
		
	def __init__(self, date, mils_max, mils_base, dyds, bonus_sched, base_prod, prod_cap, fact_out, dyd_out):
		self.date = date
		self.bonus_sched = bonus_sched
		self.base_prod = base_prod
		self.prod_cap = prod_cap
		self.fact_out = fact_out
		self.mils = []
		self.new_mils(mils_max, 'max')
		self.new_mils(mils_base)
		self.dyd_out = dyd_out
		self.dyds = []
		self.new_dyds(dyds)

	def new_mils(self, num_of_mils, curr_prod_eff=None):
		prod_eff = self.prod_cap if curr_prod_eff == 'max' else self.base_prod
		for x in range(num_of_mils):
			self.mils.append(Mil(self.date, prod_eff, self.prod_cap, self.fact_out))

	def new_dyds(self, num_of_dyds):
		for x in range(num_of_dyds):
			self.dyds.append(Dyd(self.date, self.dyd_out))

	def update_mods(self):
		if self.date in self.bonus_sched:
			bonus_dict = self.bonus_sched[self.date]
			for mod in bonus_dict:
				bonus = bonus_dict[mod]
				if mod == 'base_mod':
					self.base_prod += bonus
				elif mod == 'cap_mod':
					self.prod_cap += bonus
				elif mod == 'fact_mod':
					self.fact_out += bonus
				elif mod == 'dyd_mod':
					self.dyd_out += bonus
			
	def advance_day(self):
		pass						
