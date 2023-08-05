import inspect
import theano
import numpy as np

from .epidemia import Model

if not 'profile' in dir():
    def profile(f):
        return f

class SIR(Model):
    def __init__(self):
        self.cols = ['S', 'I', 'R',
                     'I_cases']

        self.names = {
            'I_cases': r'$I_{\mathrm{cases}}$',
        }
        self.styles = {
            'S': '-.', 'I': '-.', 'R': '-.',
        }
        self.colors = {
            'S': 'tab:gray', 'I': 'tab:blue', 'R': 'tab:green',
            'I_cases': 'tab:blue',
        }

        Model.__init__(self)

    def first(self, y0):
        if 'I_cases' not in y0:
            y0['I_cases'] = y0['I']
        return [y0[col] for col in self.cols]
    
    @profile
    def step(self, t, y, params):
        p = params(t)
        S, I, R = y[0], y[1], y[2]
        β, γ, μb, μd = p['β'], p['γ'], p['μb'], p['μd']

        N = S + I + R

        return [
            # S, I, R
            μb*N - β*I*S/N - μd*S,
            β*I*S/N - γ*I,
            γ*I,

            # I_cases
            β*I*S/N,
        ]

    def N(self, t, Y=None, params=None):
        if Y is None:
            Y = self.Y
        y = Y[t]
        return y['S'] + y['I'] + y['R']
    
    def R(self, t, Y=None, params=None):
        if params is None:
            params = self.params
        p = params(t)
        return p['β'] / p['γ']
    
    def R_effective(self, t, Y=None, params=None):
        if Y is None:
            Y = self.Y
        y = Y[t]
        return self.R(t, Y, params) * y['S'] / self.N(t, Y, params)

class ModelReport2(Model):
    def __init__(self):
        self.cols = ['S', 'E', 'Im', 'I', 'H', 'Hc', 'R', 'D',
                     'Im_cases', 'I_cases', 'H_cases', 'Hc_cases', 'R_cases', 'H_total']

        self.names = {
            'Im_cases': r'$I^m_{\mathrm{cases}}$', 'I_cases': r'$I_{\mathrm{cases}}$', 'H_cases': r'$H_{\mathrm{cases}}$',
            'Hc_cases': r'$H^c_{\mathrm{cases}}$', 'R_cases': r'$R_{\mathrm{cases}}$', 'H_total': r'$H + H^c$',
            'R_effective': '$R_{eff}$', 'Fatality': r'$\mathrm{Fatality}$',
        }
        self.styles = {
            'S': '-.', 'E': '-.', 'Im': '-.', 'I': '-.',
            'H': '-.', 'Hc': '-.', 'R': '-.', 'D': '-.',
            'H_total': '-.',
        }
        self.colors = {
            'S': 'tab:gray', 'E': 'tab:cyan', 'Im': 'tab:purple', 'I': 'tab:blue',
            'H': 'tab:olive', 'Hc': 'tab:orange', 'R': 'tab:green', 'D': 'tab:red',
            'Im_cases': 'tab:purple', 'I_cases': 'tab:blue', 'H_cases': 'tab:olive',
            'Hc_cases': 'tab:orange', 'R_cases': 'tab:green', 'H_total': 'tab:brown',
        }

        Model.__init__(self)

    def first(self, y0):
        if 'Im_cases' not in y0:
            y0['Im_cases'] = y0['Im']
        if 'I_cases' not in y0:
            y0['I_cases'] = y0['I']
        if 'H_cases' not in y0:
            y0['H_cases'] = y0['H']
        if 'Hc_cases' not in y0:
            y0['Hc_cases'] = y0['Hc']
        if 'R_cases' not in y0:
            y0['R_cases'] = y0['R']
        if 'H_total' not in y0:
            y0['H_total'] = y0['H'] + y0['Hc']
        return [y0[col] for col in self.cols]
    
    @profile
    def step(self, t, y, params):
        p = params(t)
        S, E, Im, I, H, Hc, R = y[0], y[1], y[2], y[3], y[4], y[5], y[6]
        βE, βIm, βI, βH, βHc = p['βE'], p['βIm'], p['βI'], p['βH'], p['βHc']
        γE, γIm, γI, γH, γHc = p['γE'], p['γIm'], p['γI'], p['γH'], p['γHc']
        μb, μd = p['μb'], p['μd']
        φEI, φIR, φHR, φD = p['φEI'], p['φIR'], p['φHR'], p['φD']

        N = S + E + Im + I + H + Hc + R
        ROC = (1.0/N) * (βE*E + βIm*Im + βI*I + βH*H + βHc*Hc)

        return [
            # S, E, Im, I, H, Hc, R, D
            μb*N - S*ROC - μd*S,
            S*ROC - (γE+μd)*E,
            (1.0-φEI)*γE*E - (γIm+μd)*Im,
            φEI*γE*E - (γI+μd)*I,
            (1.0-φIR)*γI*I + (1-φD)*γHc*Hc - (γH+μd)*H,
            (1.0-φHR)*γH*H - (γHc+μd)*Hc,
            γIm*Im + φIR*γI*I + φHR*γH*H - μd*R,
            φD*γHc*Hc,
            
            # Im_cases, I_cases, H_cases, Hc_cases, R_cases
            (1.0-φEI)*γE*E,
            φEI*γE*E,
            (1.0-φIR)*γI*I,
            (1.0-φHR)*γH*H,
            φIR*γI*I + φHR*γH*H,

            # H_total
            (1.0-φIR)*γI*I + (1-φD)*γHc*Hc - (γH+μd)*H + (1.0-φHR)*γH*H - (γHc+μd)*Hc,
        ]

    def N(self, t, Y=None, params=None):
        if Y is None:
            Y = self.Y
        y = Y[t]
        return y['S'] + y['E'] + y['Im'] + y['I'] + y['H'] + y['Hc'] + y['R']
    
    def Fatality(self, t, Y=None, params=None):
        if Y is None:
            Y = self.Y
        y = Y[t]
        if y['I_cases'] == 0:
            return 0
        return y['D'] / y['I_cases']
    
    def R(self, t, Y=None, params=None):
        if params is None:
            params = self.params
        p = params(t)

        # see O. Diekmann, J.A.P. Heesterbeek, and M.G. Roberts, "The construction of next-generation matrices for compartmental epidemic models", J R Soc Interface, 2010
        # T are transmissions
        # Σ are transitions
        Σ = np.matrix([
            [-p['γE']-p['μd'], 0, 0, 0, 0],
            [(1.0-p['φEI'])*p['γE'], -p['γIm']-p['μd'], 0, 0, 0],
            [p['φEI']*p['γE'], 0, -p['γI']-p['μd'], 0, 0],
            [0, 0, (1.0-p['φIR'])*p['γI'], -p['γH']-p['μd'], (1.0-p['φD'])*p['γHc']],
            [0, 0, 0, (1.0-p['φHR'])*p['γH'], -p['γHc']-p['μd']],
        ])
        T = np.matrix([
            [p['βE'], p['βIm'], p['βI'], p['βH'], p['βHc']],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        
        # K = -T * Σ^-1  =>  (Σ.T) * (K.T) = -T.T
        K = np.linalg.solve(Σ.T, -T.T).T
        if np.linalg.det(K) != 0.0:
            logging.warn('det(K) = %g != 0' % np.linalg.det(K))
        return K.trace()[0,0]
    
    def R_effective(self, t, Y=None, params=None):
        if Y is None:
            Y = self.Y
        y = Y[t]
        return self.R(t, Y, params) * y['S'] / self.N(t, Y, params)
