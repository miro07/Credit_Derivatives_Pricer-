from numpy import arange
from Modules import intens as ints
from scipy.optimize import brentq
import numpy as np

class CDS(object):

    def __init__(self,credit,maturity,rate,method):

        self.credit = credit
        self.Method=method
        self.Maturity = maturity
        self.PaymentDates = arange(0, self.Maturity, 0.25)
        self.protS_leg = None
        self.protB_leg = None
        self.Coefs = None
        self.Spread = None
        self.discountrate = rate


    def spread(self,coefs):
        self.Coefs = coefs
        methods = {'HP': ints.HP_Model,
                   'IHP': ints.IHP_Model,
                   'CIR': ints.CIR_Model,
                   'GammaOUC': ints.GammaOUC_Model,
                   'IGOU': ints.IGOU_Model
                   }
        Intensity= methods[self.Method]
        c = 0
        for date in self.PaymentDates:
            t_start = date
            t_end = date + 0.25
            self.protS_leg = ints.DiscountCurve(self.discountrate,0, t_end) * \
                            (Intensity(self.Coefs, t_start) - Intensity(self.Coefs, t_end))

            self.protB_leg = ints.DiscountCurve(self.discountrate,0, t_end) * \
                             Intensity(self.Coefs, t_end) * 0.25

            if self.Method == 'HP' :
                c = self.credit.LGD * coefs


            else:
                c = self.credit.LGD * self.protS_leg / self.protB_leg
        self.Spread = c * 10000
        #print(self.Spread)
        return (self.Spread)

    def default_time(self,coefs,Uniforme):
        #print('in')
        methods = {'HP': ints.HP_Model,
                   'IHP': ints.IHP_Model,
                   'CIR': ints.CIR_Model,
                   'GammaOUC': ints.GammaOUC_Model,
                   'IGOU': ints.IGOU_Model
                   }
        method=methods[self.Method]
        #print(method)
        if len(coefs) == 1:
            self.Coefs = coefs[0]
        else:
            self.Coefs = coefs
        pd = lambda t: 1 - method(t,self.Coefs)
        #f = lambda t: pd(t) - (-log(1-Uniforme))
        f = lambda t: pd(t) - Uniforme
        try:
            tau = brentq(f, 0, 150)
        except:
            tau = 150

        return tau






