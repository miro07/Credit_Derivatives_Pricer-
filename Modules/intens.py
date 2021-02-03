from math import exp,sqrt ,sinh, log, tanh , atanh
from numpy import ones, eye






def HP_Model(t, Lambda):
    return exp(- Lambda * t)

def IHP_Model( Lambdas,t):
    tenors = [1,3,5]
    sum = 0
    for c in range(len(tenors)):
        if t.any() >= tenors[c]:
            if c == 0:
                sum += Lambdas[c] * tenors[c]
            else:
                sum += Lambdas[c] * (tenors[c] - tenors[c - 1])
        else:
            if c == 0:
                sum += Lambdas[c] * t
            else:
                sum += Lambdas[c] * (t - tenors[c])
            break
    return exp(-sum)

def CIR_Model(coefs,t):
    def coth(x):
        return 1 / tanh(x)
    k, v, gamma, lambda0 = coefs
    if t == 0.0:
        return 1
    else:
        rho = sqrt(k ** 2 + 2 * lambda0 ** 2)
        survival = 1 - (exp(k ** 2 * v * t / gamma ** 2) * exp(-2 * lambda0 / (k + rho * coth(rho * t / 2))))/ (coth(rho * t / 2) + k * sinh(rho * t / 2) / rho) ** (2 * k * v / gamma ** 2)

        return survival

def GammaOUC_Model(coefs,t):

    a, b,gamma, lambda0 = coefs

    survival = exp(-lambda0 / gamma * (1 - exp(-gamma * t)) - ((gamma * a) / (1 + gamma * b)) * \
                   (b * log(b / (b + 1 / gamma * (1 - exp(-gamma * t)))) + t))

    return survival

def IGOU_Model(coefs,t):
    a, b, gamma,lambda0 = coefs

    k = 2 * b ** (-2) / gamma
    A = (1 - sqrt(1 + k * (1 - exp(-gamma * t)))) \
             / k + 1 / sqrt(1 + k) \
             * (atanh(sqrt(1 + k * (1 - exp(-gamma * t))) /
                     sqrt(1 + k)) - atanh(1 / sqrt(1 + k)))

    survival = exp((-lambda0 / gamma) * (1 - exp(-gamma * t)) - 2 * a / (b * gamma) * A)

    return survival

def DiscountCurve (r,t1,t2):
    return (1 + r) ** -(t2 - t1)

def Flat_Correlation_Matrix(rho,N):
    return rho * ones([N, N]) + (1 - rho) * eye(N, N)
def DiscountCurve (r,t1,t2):
    return (1 + r) ** -(t2 - t1)

def Flat_Correlation_Matrix(rho,N):
    return rho * ones([N, N]) + (1 - rho) * eye(N, N)