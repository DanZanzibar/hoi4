import forces, economy
from datetime import date, timedelta


def get_mil_IC(prod: economy.Production, init_date, start_maxed=False):
	for mil in prod.mils:
		if mil.init_date == init_date and mil.start_maxed == start_maxed:
			return mil.produced
	raise Exception('No such Mil')
			

def get_dyd_IC(prod: economy.Production, init_date):
	for dyd in prod.dyds:
		if dyd.init_date == init_date:
			return dyd.produced
	raise Exception('No such Dyd')
	

