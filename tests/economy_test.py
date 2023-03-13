from hoi4.economy import *

class Test_Mil:

    def test_basic_prod(self):
        mil = Mil(date(1936, 1, 1), 1, 1, 1)
        for _ in range(100):
            mil.daily_prod()
            mil.prod_eff_daily_gain()
        assert mil.produced == 100 * mil_base

    def test_prod_eff_gain(self):
        mil = Mil(date(1936, 1, 1), 0.5, 1, 1)
        count = 0
        while mil.prod_eff < mil.prod_cap:
            mil.prod_eff_daily_gain()
            count += 1
        assert count == 375