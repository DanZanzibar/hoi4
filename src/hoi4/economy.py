from datetime import date, timedelta

one_day_inc = timedelta(days=1)
mil_base = 4.5
dyd_base = 2.5


class Mil:
		
	def __init__(self, init_date: date, prod_eff, prod_cap, fact_out, maxed_at_start=False):
		self.init_date = init_date
		self.init_eff = prod_eff
		self.prod_eff = prod_eff
		self.prod_cap = prod_cap
		self.fact_out = fact_out
		self.maxed_at_start = maxed_at_start
		self.at_prod_cap = False
		self.produced = 0

	def __str__(self) -> str:
		if self.maxed_at_start == True:
			return f'Init Date: {self.init_date} @ max efficiency'
		else:
			return f'Init Date: {self.init_date}'
		
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

	def __init__(self, init_date: date, dyd_out: float) -> None:
		self.init_date = init_date
		self.dyd_out = dyd_out
		self.produced = 0

	def daily_prod(self):
		output_IC = self.dyd_out * dyd_base
		self.produced += output_IC


class Production:
		
	def __init__(self, date: date, bonus_sched: dict, base_prod=0.1, prod_cap=0.5, fact_out=1, dyd_out=1):
		self.date = date
		self.bonus_sched = bonus_sched
		self.base_prod = base_prod
		self.prod_cap = prod_cap
		self.fact_out = fact_out
		self.mils = {Mil(date, prod_cap, prod_cap, fact_out, maxed_at_start=True): 0}
		self.dyd_out = dyd_out
		self.dyds = {Dyd(date, dyd_out): 0}
		self.init_args = (self.date, self.bonus_sched, self.base_prod, self.prod_cap, self.fact_out, self.dyd_out)

	def new_mil(self, curr_prod_eff=None):
		if curr_prod_eff:
			prod_eff = self.prod_cap if curr_prod_eff == 'max' else curr_prod_eff
		else:
			prod_eff = self.base_prod
		self.mils[Mil(self.date, prod_eff, self.prod_cap, self.fact_out)] = 0

	def new_dyd(self):
		self.dyds[Dyd(self.date, self.dyd_out)] = 0

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
			
	def advance_day(self):
		if self.date.day == 1: 
			self.new_mil(self.base_prod)
		self.update_mods()
		for mil in self.mils:
			mil.daily_prod()
		for dyd in self.dyds:
			dyd.daily_prod()
		self.date += one_day_inc

	def advance_to_date(self, new_date: date):
		num_days = (new_date - self.date).days
		for _ in range(num_days):
			self.advance_day()

	def add_tangible_mils(self, max_at_start=None, *tangible_mils):
		if max_at_start:
			for mil in self.mils:
				if mil.maxed_at_start == True:
					self.mils[mil] += max_at_start
					break
		for tan_mil in tangible_mils:
			quantity, year, month = tan_mil
			mil_date = date(year + 1900, month, 1)
			for mil in self.mils:
				if mil_date == mil.init_date and mil.maxed_at_start == False:
					self.mils[mil] += quantity
					break

	def reset_tangible_mils(self):
		for mil in self.mils:
			self.mils[mil] = 0

	def get_prod(self):
		return sum(mil.produced * self.mils[mil] for mil in self.mils)

	def reset_prod(self):
		for mil in self.mils:
			mil.produced = 0

	def report_mils(self):
		for mil in self.mils:
			if self.mils[mil] > 0:
				print(f'{self.mils[mil]} x', mil, f'for {mil.produced} IC per Mil')
		print(f'{self.get_prod()} total IC')

	def revert(self):
		self.reset_prod()
		self.reset_tangible_mils()
		self.__init__(*self.init_args)
		