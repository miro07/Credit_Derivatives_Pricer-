from scipy.stats import norm, chi2, uniform, gamma, t
from Modules import intens as ints
from scipy.stats import norm
from scipy.optimize import brentq
from numpy.random import multivariate_normal
import math
from abc import ABC,abstractmethod


class Copula(ABC):
    @abstractmethod
    def __init__(self):
        pass



class Gaussian_Copula(Copula):

    def __init__(self,cov):
        self.Cov = cov

    def Simulate(self,N):
        mean = [0.0] * N
        Z = multivariate_normal(mean, self.Cov)
        U = norm.cdf(Z)


        return U



class Student_Copula(Copula):

    def __init__(self, cov,copula_df=2):


        self.Cov = cov
        self.df = copula_df

    def Simulate(self,N):
        """docstring for Simulate"""
        mean = [0.0] * N

        s = chi2.rvs(self.df)
        Z = multivariate_normal(mean, self.Cov)
        X = [math.sqrt(self.df) / math.sqrt(s) * z for z in Z]
        S = [t.cdf(x, self.df) for x in X]

        return S

class Copula_Simulation(object):

    def __init__(self, copula):
        self.copula = copula

    def MC_Simulation(self, n_sim):
        taus = []
        for i in range(n_sim):
            tau= self.copula.Simulate()
            taus.append(tau)
            # print tau

        return taus

