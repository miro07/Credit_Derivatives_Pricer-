import pandas as pd
from Modules import Portfolio
from statistics import mean





class CDO_Tranche():
    """Pays off 0 if less than k defaults occur, pays l-k if more than l defaults
    occur, and pays (x-k) if k <= x < l defaults occur"""
    def __init__(self,portfolio,MNCDS,s,k,maturity,rate = 0.01):
        #super(KthToLthTranche, self).__init__(DiscountCurve)
        self.portfolio = portfolio
        self.MNCDS = MNCDS
        self.size=s
        self.lower = k
        self.upper = k+s
        self.price=None
        self.discountrate = rate
        self.Maturity = maturity
        assert  k < k+s , 'The upper of the tranche can not be below the lower of it '

    def CDO_Pricing(self,default_times):
        """Pays off 0 if less than k defaults occur, pays l-k if more than l defaults
    occur, and pays (x-k) if k <= x < l defaults occur"""
        defaults_before_t = sum(map(lambda x: x < self.Maturity, default_times))
        if defaults_before_t > (self.upper * len(self.MNCDS.CDSs)):
            value = (self.upper - self.lower)
        elif defaults_before_t < (self.lower * len(self.MNCDS.CDSs)):
            value = 0
        else:
            value = defaults_before_t - self.lower
        return float(value) / self.size
