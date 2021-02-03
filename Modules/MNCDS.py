from Modules import CDS
from Modules import intens as ints
import numpy as np
import pandas as pd



class MNCDS():
    def __init__ (self,portfolio,maturity,rate):

        self.CDS = CDS
        self.CDSs = []
        self.portfolio = portfolio
        self.discountrate = rate
        self.Maturity= maturity

    def set_CDS(self,method):

        pr = pd.read_excel('Credit-Portfolio.xls', sheet_name='Portfolio', index_col=None)
        for k in range(len(self.portfolio.Credits)):
            self.CDSs.append(CDS.CDS(self.portfolio.Credits[k], self.Maturity, self.discountrate, method))



    def Pricing(self,default_times,K_default):
        sorted_default_times = sorted(default_times)
        print(sorted_default_times)
        if len(sorted_default_times) < K_default:
            print('in1')
            value = 0
        elif sorted_default_times[K_default - 1] < self.Maturity:
            print('in2')
            t = sorted_default_times[K_default - 1]
            value = ints.DiscountCurve(self.discountrate,0, t)
        else:
            print('in3')
            value = 0
        return value
