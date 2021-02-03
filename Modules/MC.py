import pandas as pd
from Modules import Portfolio as prt
import numpy as np
from Modules import intens as ints
from Modules import Calibration as cali
from Modules import MNCDS
from Modules import Copula as cp
from Modules import CDO

class MC ():
    def __init__(self):
        self.MNCDS_prices = None
        self.CDO_Prices = None

    def MC_intens( self,coefs, maturity,r,corr ,n_sim ,k ,s ,l ,method):
        portfolio = prt.Portfolio(maturity)
        portfolio.set_Credits()
        mnCDS = MNCDS.MNCDS(portfolio, maturity, r)
        mnCDS.set_CDS(method)
        cdo = CDO.CDO_Tranche(portfolio, mnCDS, s, l, maturity, r)
        cov = ints.Flat_Correlation_Matrix(corr, len(mnCDS.CDSs))
        value1 = []
        value2 = []
        calibrated_lambda = []
        for cds in range(len(mnCDS.CDSs)):
            calibration = cali.Calibration(CDS=mnCDS.CDSs[cds], id=cds,
                                       Guess=coefs)
            calibrated_lambda.append(calibration.Calibrate())
        for N in range(n_sim):
            coupula = cp.Gaussian_Copula(cov)
            uniforme = coupula.Simulate(len(mnCDS.CDSs))
            default_times = []
            for cds in range(len(mnCDS.CDSs)):
                uni = uniforme[cds]
                dft = mnCDS.CDSs[cds].default_time(calibrated_lambda[cds], Uniforme=uni)
                default_times.append(dft)
            value1.append(mnCDS.Pricing(default_times, k))
            value2.append(cdo.CDO_Pricing(default_times))
        self.MNCDS_prices = value1
        self.CDO_Prices = value2
        kCDS_price = np.mean(value1)
        CDO_price = np.mean(value1)
        result = {'K-default CDS price': kCDS_price, 'Size of CDO Tranche': CDO_price, 'Number of Simulation': n_sim}
        return result

    def get_MNCDS_prices(self):
        return self.MNCDS_prices
    def get_CDO_Prices(self):
        return self.CDO_Prices