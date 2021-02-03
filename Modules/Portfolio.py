import pandas as pd
from Modules import Credit as cr
from random import gauss
from math import floor, sqrt
from scipy.stats import norm
from statistics import mean


class Portfolio():
    n_sim = 1000
    def __init__(self,maturity):
        self.Credits=[]
        self.loss=[]
        self.VaR=None
        self.ES=None
        self.EL=None
        self.UEL=None
        self.CL=None
        self.corr=None
        self.sect_Corr=None
        self.Pt_Amount=0
        self.num_sectors=None
        self.Maturity = maturity
    def set_Credits(self):
        rt = pd.read_excel('Credit-Portfolio.xls', sheet_name='Rate', index_col=None)
        pr = pd.read_excel('Credit-Portfolio.xls', sheet_name='Portfolio', index_col=None)
        for id in pr['ID']:
            self.Credits.append(cr.Credit(id))
            self.Credits[id].set_parametres(pr,'ID','EAD','Rating','LGD','Sector')
            self.Credits[id].RATE_to_PD(rt,'PD', '1Y', '3Y', '5Y')
            self.Pt_Amount = self.Pt_Amount + self.Credits[id].EAD
            self.num_sectors = len(set(pr['Sector']))


    def MC_Sim(self,n_sim):
        sect = pd.read_excel('Credit-Portfolio.xls', sheet_name='Sector', index_col=None)
        parm = pd.read_excel('Credit-Portfolio.xls', sheet_name='Params', index_col=None)
        self.corr = parm.loc[:, 'GlobalCorrelation'].iloc[0]
        self.CL = parm.loc[:, 'IC'].iloc[0]
        self.sect_Corr = sect['Correlation'].values
        for i in range(n_sim):
            loss=0
            Z = 0
            X = gauss(0,1.0)
            Xs = [gauss(0,1.0) for i in range(self.num_sectors)]
            for k in range(len(self.Credits)):
                mati = {"1Y": self.Credits[k].PD1,
                        "2Y": self.Credits[k].PD3,
                        "3Y": self.Credits[k].PD5}
                p_d = mati[self.Maturity]
                Z=sqrt(self.corr)*X+sqrt(self.sect_Corr[self.Credits[k].Sector]-self.corr)*Xs[self.Credits[k].Sector]+sqrt(1-self.sect_Corr[self.Credits[k].Sector])*gauss(0,1.0)
                if Z < norm.ppf(p_d):
                    loss = loss+self.Credits[k].EAD * self.Credits[k].LGD
            self.loss.append(-loss)
    def Var(self):
        tri_loss = sorted(self.loss)
        self.VaR = -(tri_loss[floor(Portfolio.n_sim*(1-self.CL))]+(floor(Portfolio.n_sim*(1-self.CL))-(Portfolio.n_sim*(1-self.CL))*(tri_loss[floor(Portfolio.n_sim*(1-self.CL))+1]-tri_loss[floor(Portfolio.n_sim*(1-self.CL))])))
        return self.VaR
    def Calculs(self):
        for k in range(len(self.Credits)):
            mati = {"1Y": self.Credits[k].PD1,
                    "2Y": self.Credits[k].PD3,
                    "3Y": self.Credits[k].PD5}
            p_d = mati[self.Maturity]
            self.EL += self.Credits[k].EAD*self.Credits[k].LGD * p_d
        self.UEL = self.VaR-self.EL
    def Price_Gauss2d(self,s,l):
        tranche = []
        for n in self.loss:
            k=-n/ self.Pt_Amount
            tranche.append(max(min(k,s+l)-l,0)/s)
        return mean(tranche)

