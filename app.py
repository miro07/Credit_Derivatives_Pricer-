from flask import Flask, render_template, request, session
import os
import matplotlib.pyplot as plt
from Modules import MC
from Modules import Portfolio as prt
import numpy as np
app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/cdp',methods=['POST'])
def cdp():
    var1 = request.form['Intensity']
    var2 = request.form['Optimise']
    session['Intensity'] = var1
    session['Optimise'] = var2
    if var1 == "G2D":
        return render_template('inputs0.html')
    if var1 == "HP":
        print('inserted value : ' + var1)
        return render_template('inputs1.html')
    elif var1 == "IHP":
        print('inserted value : ' + var1)
        return render_template('inputs2.html')
    else:
        return render_template('inputs3.html')
@app.route('/gauss',  methods=['POST'])
def gauss():
    maturity = str(request.form['Maturity'])
    n_sim = int(request.form['Simulation Number'])
    s = float(request.form['Size of CDO Tranche'])
    l = float(request.form['lower of CDO Tranche'])
    port1 = prt.Portfolio(maturity)
    port1.set_Credits()
    port1.MC_Sim(n_sim)
    result = {'Var' : port1.Var() , 'CDO Tranche Price ': port1.Price_Gauss2d(s,l)}
    return render_template("result.html",result = result)


@app.route('/parameters1',  methods=['POST'])
def parameters1():
    coef = []
    maturity = int(request.form['Maturity'])
    r = float(request.form['Discount rate'])
    corr = float(request.form['Correlation'])
    n_sim = int(request.form['Simulation Number'])
    k = int(request.form['K-default CDS'])
    s = float(request.form['Size of CDO Tranche'])
    l = float(request.form['lower of CDO Tranche'])
    method = session['Intensity']
    if session['Intensity'] == "HP" :
        geuss = float(request.form['Geuss'])
        coef.append(geuss)
        print('checking session: ' + session['Intensity'])
    elif session['Intensity'] == "IHP" :
        geuss1 = float(request.form['Geuss 1'])
        coef.append(geuss1)
        geuss2 = float(request.form['Geuss 2'])
        coef.append(geuss2)
        geuss3 = float(request.form['Geuss 3'])
        coef.append(geuss3)
    else :
        geuss1 = float(request.form['Geuss 1'])
        coef.append(geuss1)
        geuss2 = float(request.form['Geuss 2'])
        coef.append(geuss2)
        geuss3 = float(request.form['Geuss 3'])
        coef.append(geuss3)
        geuss4 = float(request.form['Geuss 4'])
        coef.append(geuss4)
        #session.pop('select1', None)
    coefs = np.asarray(coef)
    mc = MC.MC()
    result = mc.MC_intens( coefs, maturity,r,corr ,n_sim ,k ,s ,l ,method)
    plt.style.use('seaborn-darkgrid')
    plt.figure()
    X = range(len(mc.get_MNCDS_prices()))
    plt.plot(X, mc.get_MNCDS_prices(), label='CDO Tranche prices')
    plt.plot(X, mc.get_CDO_Prices(), label='Multi Name CDS prices')
    plt.legend()
    # strFile = '../static/graph.png'
    if os.path.isfile('C:/Users/MIRO/Desktop/ProjetB/APP/static/graph.png'):
        os.remove('C:/Users/MIRO/Desktop/ProjetB/APP/static/graph.png')  # Opt.: os.system("rm "+strFile)
    plt.savefig('C:/Users/MIRO/Desktop/ProjetB/APP/static/graph.png')
    return render_template("result.html",result = result)
@app.route('/graph')
def graph():
    return render_template('graph.html')



if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.debug = True
    app.run()