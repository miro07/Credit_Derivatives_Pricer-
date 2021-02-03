from abc import ABC , abstractmethod
import scipy.optimize as optimize
from random import randint,gauss
from math import fabs,exp,sqrt , cosh, sinh, log, tanh , atanh

class Intensity(ABC):

    def __init__(self,portfolio,CDS,gamma):
        self.Gamma = gamma
        self.portfolio=portfolio
        self.CDS = CDS
        self.Method=None
        self.calibrated_gamma=None


    @abstractmethod
    def SurvivalProbability(self):
        pass

    def Spread(self, k):

        spread = (1 - self.portfolio.Credits[k].R) * self.CDS.protS_leg / self.CDS.protB_leg

        return spread * 10000


    def ObjectiveFunction(self):
        """Calculates the error in estimation for use in our calibration
        routines.

        Currently we use the L^2 norm."""
        sum = 0
        for t, market_spread in self.MarketData.Data():
            CDS = self.CDS(DiscountCurve=self.DiscountCurve,
                           maturity=t)
            model_spread = self.Spread(self.Gamma)
            sum += (model_spread - market_spread) ** 2
        return sum

    def Calibrate(self, method='nm'):
        """Performs the calibration and returns the optimal parameters.

        The built in Optimise method in SciPy uses Nelder-Mead optimisation."""
        methods = {'nm': optimize.fmin,
                   'powell': optimize.fmin_powell,
                   'cg': optimize.fmin_cg,
                   'bfgs': optimize.fmin_bfgs
                   }

        if method == None:
            optimise = methods[self.Method]
        else:
            optimise = methods[method]

        output = optimise(self.ObjectiveFunction,
                          self.Guess,
                          disp=0
                          )
        self.calibrated_gamma = output

        return output

class HP_Model(Intensity):

    def __init__(self,):
        super(HP_Model, self).__init__()

    def Survival_function(self,t):
        return exp(- self.Gamma * t)

    def Spread(self,k):
        spread = (1 - self.portfolio.Credits[k].R) * self.Gamma
        return spread * 10000

class IHP_Model(Intensity):

    def __init__(self):
        super(IHP_Model, self).__init__()
        self.counter = None
        self.Lambdas = None

    def Survival_function(self, t, N):
        self.counter = sorted([randint(0, t) for i in range(N)])
        self.Lambdas = sorted([1 + fabs(gauss(0, 1)) for i in range(N)])
        sum = 0
        for c in range(len(self.counter)):
            if t >= self.counter[c]:
                if c == 0:
                    sum += self.Lambdas[c] * self.counter[c]
                else:
                    sum += self.Lambdas[c] * (self.counter[c] - self.counter[c-1])
            else:
                if c == 0:
                    sum += self.Lambdas[c] * t
                else:
                    sum += self.Lambdas[c] * (t - self.counter[c])
                break
        return exp(-sum)

class CIR_Model(Intensity):

    def __init__(self, coefs):
        super(CIR_Model, self).__init__()
        self.Coefs=coefs
        assert (len(coefs) == 4)

    def Survival_function(self, t):

        def coth(x):
            return 1 / tanh(x)

        k,v,gamma,lambda0 = self.Coefs

        if t == 0.0 :
            return 1
        else:
            rho = sqrt(k**2 + 2 * lambda0**2)
            survival= 1 - ( exp( k ** 2 * v * t / gamma ** 2 ) * exp( -2 * lambda0/(k + rho * coth(rho * t / 2))))\
                      / ( coth( rho * t / 2) + k * sinh( rho * t / 2) / rho) ** (2 * k * v / gamma ** 2)

            return survival

class GammaOUC_Model(Intensity):

    def __init__(self,coefs):
         super(GammaOUC_Model, self).__init__()
         self.Coefs=coefs
         assert (len(coefs) == 4)

    def Survival_function(self, t):

        gamma,a,b,lambda0= self.Coefs

        survival = exp(-lambda0 / gamma * (1 - exp(-gamma * t)) - (( gamma * a) / (1 + gamma * b)) * \
                   (b * log(b / (b + 1 / gamma * (1 - exp(-gamma * t)))) + t))

        return survival

class IGOU_Model (Intensity):

    def __init__(self, coefs):
        super(IGOU_Model, self).__init__()
        self.Coefs = coefs
        self.A = None
        assert (len(coefs) == 4)

    def Survival_function(self, t):

        gamma, a, b, lambda0 = self.Coefs

        k = 2 * b ** (-2) / gamma
        self.A = (1 - sqrt(1 + k * (1 - exp(-gamma * t)))) \
                 / k + 1 / sqrt(1 + k) \
                 * (atanh(sqrt(1 + k * (1 - exp(-gamma * t))) / \
                         sqrt(1 + k)) - atanh(1 / sqrt(1 + k)))

        survival = exp( (-lambda0 / gamma) * (1 - exp( -gamma * t)) - 2 * a / (b * gamma) * self.A )

        return survival

































