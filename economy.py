import forces
from datetime import date, timedelta
from copy import deepcopy

one_day_inc = timedelta(days=1)
mil_base = 4.5
dyd_base = 2.5


class Mil:
		
	def __init__(self, init_date, prod_eff, prod_cap, fact_out):
		self.init_date = init_date
		self.init_eff = prod_eff
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
		
	def __init__(self, date, mils, dyds, bonus_sched, cons_sched, base_prod=0.1, prod_cap=0.5, fact_out=1, dyd_out=1):
		self.date = date
		self.bonus_sched = bonus_sched
		self.cons_sched = cons_sched
		self.base_prod = base_prod
		self.prod_cap = prod_cap
		self.fact_out = fact_out
		self.mils = []
		for entry in mils:
			if isinstance(entry, int):
				self.new_mils(entry)
			else:
				self.new_mils(*entry)
		self.dyd_out = dyd_out
		self.dyds = []
		self.new_dyds(dyds)
		self.start = deepcopy(self)

	def new_mils(self, num_of_mils, curr_prod_eff=None):
		if curr_prod_eff:
			prod_eff = self.prod_cap if curr_prod_eff == 'max' else curr_prod_eff
		else:
			prod_eff = self.base_prod
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
					for mil in self.mils:
						mil.prod_cap = self.prod_cap
				elif mod == 'fact_mod':
					self.fact_out += bonus
					for mil in self.mils:
						mil.fact_out = self.fact_out
				elif mod == 'dyd_mod':
					self.dyd_out += bonus
					for dyd in self.dyds:
						dyd.dyd_out = self.dyd_out

	def update_cons(self):
		if self.date in self.cons_sched:
			mils, dyds = self.cons_sched[self.date]
			if mils:
				self.new_mils(mils)
			if dyds:
				self.new_dyds(dyds)
			
	def advance_day(self):
		self.update_mods()
		self.update_cons()
		for mil in self.mils:
			mil.daily_prod()
		for dyd in self.dyds:
			dyd.daily_prod()
		self.date += one_day_inc

	def advance_to_date(self, new_date):
		num_days = (new_date - self.date).days
		for day in range(num_days):
			self.advance_day()
