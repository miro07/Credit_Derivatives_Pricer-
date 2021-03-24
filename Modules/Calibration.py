import pandas as pd
import scipy.optimize as optimize
from math import sqrt

class Calibration ():

    def __init__(self,CDS,id ,Guess,method = "nm"):
        self.CDS = CDS
        self.Guess = Guess
        self.Method = method
        self.calibrated_lambda = None
        self.CDSid=id
        self.calibrate_resultat = []
    def Eror_function(self,Lambda):
        """ Calculates the error in estimation for use in our calibration
        routines.Currently we use the RMSE norm """ 
        Mdt=pd.read_excel('Credit-Portfolio.xls', sheet_name='Portfolio', index_col=None)
        sum = 0
        maturities = [1,3,5]
        for t in maturities:
            colNames = Mdt.columns[Mdt.columns.str.contains(pat=str(t))]
            market_spread = Mdt.loc[self.CDSid,colNames].iloc[0]
            model_spread = self.CDS.spread(Lambda)
            sum += (model_spread - market_spread) ** 2
        #self.calibrate_resultat.append(sum)
        #print(sqrt(sum/3))
        return sqrt(sum/3)


    def Calibrate(self,method='nm'):
        """ Performs the calibration and returns the optimal parameters. The built in Optimise method in SciPy uses Nelder-Mead optimisation. """
        methods = {'nm': optimize.fmin,
                   'powell': optimize.fmin_powell,
                   'cg': optimize.fmin_cg,
                   'bfgs': optimize.fmin_bfgs
                   }

        if method == None:
            optimise = methods[self.Method]
        else:
            optimise = methods[method]

        output = optimise(self.Eror_function,self.Guess,disp=0.0 )
        self.calibrated_lambda = output
        #print(output)
        return output



