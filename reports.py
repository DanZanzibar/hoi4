import forces, economy
from datetime import date, timedelta
	
	
def mils_by_date(prod_obj):
	mils_prod = {}
	for mil in prod_obj.mils:
		if 'maxed_at_start' in mils_prod:
			mils_prod[mil.init_date] = mil.produced
		else:
			mils_prod['maxed_at_start'] = mil.produced
	return mils_prod
	
	
def dyds_by_date(prod):
	dyds_prod = {}
	for dyd in prod_obj.dyds:
		dyds_prod[dyd.init_date] = dyd.produced
	return dyds_prod
	
	

	
	
def add_all_production(prod, *mils):
	mils_dict = mils_by_date(prod)
	date, quantity = mil
	total += quantity * mils_dict[date]
