import Portfolio as prt
from Plots import *
from intens import *
import Calibration as cali
import MNCDS
import Copula as cp
import CDO

default_cortimes = []


def Pricing (default_cortimes):
    r = 0.01
    maturity = 4
    guess = [0.001]
    portfolio = prt.Portfolio()
    portfolio.set_Credits()
    mnCDS = MNCDS.MNCDS(portfolio,maturity,r)
    mnCDS.set_CDS()
    cdo=CDO.CDO_Tranche(portfolio,mnCDS,0.05,0.1,maturity,r)
    #print(mnCDS.CDSs)
    '''cov = Flat_Correlation_Matrix(0.4,len(mnCDS.CDSs))
    coupula = cp.Gaussian_Copula(cov)
    uniforme = coupula.Simulate(len(mnCDS.CDSs))
    print(uniforme)'''
    Correlation = [0,0.5,0.8]
    labels=['e = 0','e = 50%' , 'e = 80%']
    #default_cortimes = []
    for cor in Correlation:
        cov = Flat_Correlation_Matrix(cor, len(mnCDS.CDSs))
        coupula = cp.Gaussian_Copula(cov)
        uniforme = coupula.Simulate(len(mnCDS.CDSs))
        #print(uniforme)
        default_times = []
        for cds in range(len(mnCDS.CDSs)):
            calibration = cali.Calibration( CDS = mnCDS.CDSs[cds],id=cds,
                                        Guess = guess )
            print(cds)
            calibrated_lambda = calibration.Calibrate()
            uni = uniforme[cds]
            dft = mnCDS.CDSs[cds].default_time(calibrated_lambda,Uniforme = uni)
            default_times.append(dft)
        print(calibration.RMSE(len(mnCDS.CDSs)))
        value=mnCDS.Pricing(default_times,15)
        print(value)
        value2 = cdo.CDO_Pricing(default_times)
        print(value2)
        default_cortimes.append(default_times)
    distrubitions_plot(labels,default_cortimes[0],default_cortimes[1],default_cortimes[2])
    #dot_plot(labels, default_cortimes[0],default_cortimes[1],default_cortimes[2])
    return default_cortimes

dt=Pricing (default_cortimes)
print(dt)
#distrubitions_plot(['r','t'],[[1,2,2,4],[5,5,3,4]])
