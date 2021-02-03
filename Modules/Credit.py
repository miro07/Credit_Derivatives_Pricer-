




class Credit():

    def __init__(self,id):
        self.ID=id
        self.EAD = None
        self.RATE = None
        self.LGD = None
        self.Sector=None
        self.PD1 = None
        self.PD3 = None
        self.PD5 = None
        #Credit[self.ID]=self

    def set_parametres(self,data,id,Ead,rate,lgd,Sector):
        self.EAD = data.loc[data[id] == self.ID, Ead].iloc[0]
        self.RATE = data.loc[data[id] == self.ID, rate].iloc[0]
        self.LGD = data.loc[data[id] == self.ID, lgd].iloc[0]
        self.Sector = data.loc[data[id] == self.ID, Sector].iloc[0]

    def RATE_to_PD(self,data,PD,Y1,Y3,Y5):
         self.PD1=data.loc[data[PD]==self.RATE,Y1].iloc[0]
         self.PD3 = data.loc[data[PD] == self.RATE, Y3].iloc[0]
         self.PD5 = data.loc[data[PD] == self.RATE, Y5].iloc[0]