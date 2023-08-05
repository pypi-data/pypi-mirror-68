import inspect
import time
import logging
logging.basicConfig(format='%(message)s')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import networkx as nx

import scipy
import skopt
from skopt.plots import plot_convergence
from pyswarms.single.global_best import GlobalBestPSO
from pyswarms.single.local_best import LocalBestPSO
from pyswarms.single.general_optimizer import GeneralOptimizerPSO

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

if not 'profile' in dir():
    def profile(f):
        return f

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
tableau20 = [(0, 107, 164), (255, 128, 14), (171, 171, 171), (89, 89, 89),
             (95, 158, 209), (200, 82, 0), (137, 137, 137), (163, 200, 236),
             (255, 188, 121), (207, 207, 207)]
tableau20 = [(color[0]/255.0, color[1]/255.0, color[2]/255.0) for color in tableau20]

def absolute_error(y_true, y_pred):
    mask = ~np.isnan(y_true)
    return np.sum(np.abs(y_true[mask]-y_pred[mask]))

def squared_error(y_true, y_pred):
    mask = ~np.isnan(y_true)
    return np.sum((y_true[mask]-y_pred[mask])**2)

def absolute_percentage_error(y_true, y_pred):
    mask = ~np.isnan(y_true) & ~np.isclose(y_true, 0.0)
    return np.sum(np.abs((y_true[mask]-y_pred[mask])/y_true[mask]))

def squared_percentage_error(y_true, y_pred):
    mask = ~np.isnan(y_true) & ~np.isclose(y_true, 0.0)
    return np.sum(((y_true[mask]-y_pred[mask])/y_true[mask])**2)

def mean_absolute_error(y_true, y_pred):
    mask = ~np.isnan(y_true)
    if np.sum(mask) == 0:
        return 0
    return np.average(np.abs(y_true[mask]-y_pred[mask]))

def mean_squared_error(y_true, y_pred):
    mask = ~np.isnan(y_true)
    if np.sum(mask) == 0:
        return 0
    return np.average((y_true[mask]-y_pred[mask])**2)

def mean_absolute_percentage_error(y_true, y_pred):
    mask = ~np.isnan(y_true) & ~np.isclose(y_true, 0.0)
    if np.sum(mask) == 0:
        return 0
    return np.average(np.abs((y_true[mask]-y_pred[mask])/y_true[mask]))

def mean_squared_percentage_error(y_true, y_pred):
    mask = ~np.isnan(y_true) & ~np.isclose(y_true, 0.0)
    if np.sum(mask) == 0:
        return 0
    return np.average(((y_true[mask]-y_pred[mask])/y_true[mask])**2)

#def Epidemic:
#    def __init__(self):
#        self.G = nx.DiGraph()
#
#    def add_compartment(name):
#        pass
#
#def CancinoCOVID19():
#    G = nx.DiGraph()
#    G.add_node('S',  rate=lambda p,y: (y['N']/y['S'])*p['μb']-p['μd'])
#    G.add_node('E',  rate=lambda p,y: -p['μd'])
#    G.add_node('Im', rate=lambda p,y: -p['μd'])
#    G.add_node('I',  rate=lambda p,y: -p['μd'])
#    G.add_node('H',  rate=lambda p,y: -p['μd'])
#    G.add_node('Hc', rate=lambda p,y: -p['μd'])
#    G.add_node('R',  rate=lambda p,y: -p['μd'])
#    G.add_node('D',  rate=lambda p,y: 0)
#    #G.add_node('N',  value=lambda p,y: y['S']+y['E']+y['Im']+y['I']+y['H']+y['Hc']+y['R'])
#
#    G.add_edge('S', 'E',  t='', Λ=lambda Λ: p['βE'])
#    G.add_edge('E', 'S',  t='infect', λ=lambda p: p['βE'])
#    G.add_edge('Im', 'S', t='infect', λ=lambda p: p['βIm'])
#    G.add_edge('I', 'S',  λ=lambda p: p['βI'])
#    G.add_edge('H', 'S',  λ=lambda p: p['βH'])
#    G.add_edge('Hc', 'S', λ=lambda p: p['βHc'])
#
#    G.add_edge('S', 'E',  rate=lambda p,y: y['Λ']/y['N'])
#    G.add_edge('E', 'Im', rate=lambda p,y: (1.0-p['φEI'])*p['γE'])
#    G.add_edge('Im', 'R', rate=lambda p,y: p['γIm'])
#    G.add_edge('E', 'I',  rate=lambda p,y: p['φEI']*p['γE'])
#    G.add_edge('I', 'R',  rate=lambda p,y: p['φIR']*p['γI'])
#    G.add_edge('I', 'H',  rate=lambda p,y: (1.0-p['φIR'])*p['γI'])
#    G.add_edge('H', 'Hc', rate=lambda p,y: (1.0-p['φHR'])*p['γH'])
#    G.add_edge('Hc', 'H', rate=lambda p,y: (1.0-p['φD'])*p['γHc'])
#    G.add_edge('Hc', 'D', rate=lambda p,y: p['φD']*p['γHc'])
#    return G
#
#    return Model(G, t0, y0, params)
#
#class Model:
#    def __init__(self, G, t0, y0, params):
#        #nx.draw_spectral(G, with_labels=True, node_size=500)
#        #plt.show()
#        
#        self.G = G
#        self.t0 = t0
#        self.params = params
#
#        data = {}
#        for name, attr in G.nodes.items():
#            data[name] = 0
#            if name in y0:
#                data[name] = y0[name]
#        self.Y = pd.DataFrame(data, index=pd.date_range(t0, t0, freq='D'))
#
#    def _params(self, t):
#        p = self.params(t, self.Y.to_dict('list'))
#        y = self.Y.loc[t].to_dict()
#
#        Λ = 0.0
#        for (u, v, λ) in self.G.edges.data('λ'):
#            if λ is not None:
#                Λ += λ(p,y)
#        y['Λ'] = Λ
#        return p, y
#
#    def R_0(self, t):
#        cols = [n for n in self.G]
#        cols = ['S', 'E', 'Im', 'I', 'H', 'Hc', 'R', 'D']
#        V = np.zeros((len(cols),len(cols)))
#        F = np.zeros((len(cols),len(cols)))
#
#        p, y = self._params(t)
#        print(cols)
#        # V are the transitions, F the transmissions
#        for (u, rate) in self.G.nodes.data('rate'):
#            if rate is not None:
#                ui = cols.index(u)
#                V[ui,ui] = -rate(p,y)
#        for (u, v, rate) in self.G.edges.data('rate'):
#            if rate is not None:
#                ui = cols.index(u)
#                vi = cols.index(v)
#                V[ui,ui] = -rate(p,y)
#                V[ui,vi] = rate(p,y)
#        for (u, v, λ) in self.G.edges.data('λ'):
#            if λ is not None:
#                ui = cols.index(u)
#                vi = cols.index(v)
#                F[ui,vi] = λ(p,y)
#
#        print(V)
#        print(F)
#
#        print(nx.nodes(G))
#        print(nx.edges(G))
#        print(nx.to_dict_of_dicts(G))

#def __getitem__(self, t):
#    if type(t) is pd.Timestamp:
#        t = t.to_numpy()
#    t = np.datetime64(t, 'h')
#    if t < self.T[0] or t > self.T[-1]:
#        raise IndexError()
#        
#    idx = np.abs(self.T-t).argmin()
#    if not np.isclose(t, self.T[idx]):
#        raise IndexError()
#
#
#    y = self.Y[idx,:]      
#    if t < self.T[idx]:
#        y = ((t-self.T[idx-1])*y + (self.T[idx]-t)*self.Y[idx-1]) / (self.T[idx]-self.T[idx-1])
#    elif t > self.T[idx]:
#        y = ((self.T[idx+1]-t)*y + (t-self.T[idx])*self.Y[idx+1]) / (self.T[idx+1]-self.T[idx])
#
#    return {col: y[idx] for idx, col in enumerate(self.cols)}

class Model:
    def __init__(self):
        pass
    
    def first(self, y, p):
        raise NotImplementedError()

    def step(self, y, p):
        raise NotImplementedError()

    @profile
    def simulate(self, T, y0, params, fast=False):
        for key, val in y0.items():
            if np.isnan(val):
                logging.error('y0 for %s is NaN' % key)

        i = 0
        Y = np.zeros((len(T),len(self.cols)))
        Y[0,:] = self.first(y0)

        args = []
        if len(inspect.getfullargspec(params)[0]) == 2:
            cols = self.cols
            class Data: 
                def __getitem__(self, t):
                    if type(t) is pd.Timestamp or isinstance(t, np.datetime64):
                        if t > T[i-1]:
                            t = T[i-1]
                        y = Y[T==t,:][0,:]
                    else:
                        y = Y[:i,:][t,:]
                    return {col: y[idx] for idx, col in enumerate(cols)}
                    #return pd.Series(y, index=cols)
                
                def __len__(self):
                    return i
            args.append(Data())

        k = np.zeros((4,len(self.cols)))
        if fast:
            for i in range(1,len(T)):
                t = T[i-1]
                y = Y[i-1,:]
                Y[i,:] = y + self.step(y, params(t, *args))
        else:
            for i in range(1,len(T)):
                # Runge-Kutta 4
                t = T[i-1]
                h = T[i]-t
                y = Y[i-1,:]

                f = h / np.timedelta64(1,'D')
                k[0,:] = f * self.step(y,              params(t,         *args))
                k[1,:] = f * self.step(y + k[0,:]/2.0, params(t + h/2.0, *args))
                k[2,:] = f * self.step(y + k[1,:]/2.0, params(t + h/2.0, *args))
                k[3,:] = f * self.step(y + k[2,:],     params(t + h,     *args))

                Y[i,:] = y + (1.0/6.0)*(k[0,:] + 2.0*k[1,:] + 2.0*k[2,:] + k[3,:])
        return Y

class ModelReport2(Model):
    def __init__(self):
        self.cols = ['S', 'E', 'Im', 'I', 'H', 'Hc', 'R', 'D',
                     'Im_cases', 'I_cases', 'H_cases', 'Hc_cases', 'R_cases', 'D_cases',
                     'H_total']

        self.names = {
            'S': '$S$', 'E': '$E$', 'Im': '$I^m$', 'I': '$I$', 'H': '$H$', 'Hc': '$H^c$', 'R': '$R$', 'D': '$D$',
            'Im_cases': r'$I^m_{\mathrm{cases}}$', 'I_cases': r'$I_{\mathrm{cases}}$', 'H_cases': r'$H_{\mathrm{cases}}$',
            'Hc_cases': r'$H^c_{\mathrm{cases}}$', 'R_cases': r'$R_{\mathrm{cases}}$', 'D_cases': r'$D_{\mathrm{cases}}$',
            'H_total': r'$H + H^c$',
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
            'Hc_cases': 'tab:orange', 'R_cases': 'tab:green', 'D_cases': 'tab:red',
            'H_total': 'tab:brown',
        }
        self.y = np.zeros((len(self.cols),))

        Model.__init__(self)

    def first(self, y):
        if 'Im_cases' not in y:
            y['Im_cases'] = y['Im']
        if 'I_cases' not in y:
            y['I_cases'] = y['I']
        if 'H_cases' not in y:
            y['H_cases'] = y['H']
        if 'Hc_cases' not in y:
            y['Hc_cases'] = y['Hc']
        if 'R_cases' not in y:
            y['R_cases'] = y['R']
        if 'D_cases' not in y:
            y['D_cases'] = y['D']
        if 'H_total' not in y:
            y['H_total'] = y['H'] + y['Hc']
        return [y[col] for col in self.cols]
    
    @profile
    def step(self, y, p):
        S, E, Im, I, H, Hc, R = y[0], y[1], y[2], y[3], y[4], y[5], y[6]
        βE, βIm, βI, βH, βHc = p['βE'], p['βIm'], p['βI'], p['βH'], p['βHc']
        γE, γIm, γI, γH, γHc = p['γE'], p['γIm'], p['γI'], p['γH'], p['γHc']
        μb, μd = p['μb'], p['μd']
        φEI, φIR, φHR, φD = p['φEI'], p['φIR'], p['φHR'], p['φD']

        N = S + E + Im + I + H + Hc + R
        ROC = (1.0/N) * (βE*E + βIm*Im + βI*I + βH*H + βHc*Hc)

        # S, E, Im, I, H, Hc, R, D
        self.y[0] = μb*N - S*ROC - μd*S
        self.y[1] = S*ROC - (γE+μd)*E
        self.y[2] = (1.0-φEI)*γE*E - (γIm+μd)*Im
        self.y[3] = φEI*γE*E - (γI+μd)*I
        self.y[4] = (1.0-φIR)*γI*I + (1-φD)*γHc*Hc - (γH+μd)*H
        self.y[5] = (1.0-φHR)*γH*H - (γHc+μd)*Hc
        self.y[6] = γIm*Im + φIR*γI*I + φHR*γH*H - μd*R
        self.y[7] = φD*γHc*Hc
        
        # Im_cases, I_cases, H_cases, Hc_cases, R_cases, D_cases
        self.y[8] = (1.0-φEI)*γE*E
        self.y[9] = φEI*γE*E
        self.y[10] = (1.0-φIR)*γI*I
        self.y[11] = (1.0-φHR)*γH*H
        self.y[12] = φIR*γI*I + φHR*γH*H
        self.y[13] = φD*γHc*Hc

        # H_total
        self.y[14] = (1.0-φIR)*γI*I + (1-φD)*γHc*Hc - (γH+μd)*H + (1.0-φHR)*γH*H - (γHc+μd)*Hc
        return self.y

    def N(self, t, data):
        y = data[t]
        return y['S'] + y['E'] + y['Im'] + y['I'] + y['H'] + y['Hc'] + y['R']
    
    def Fatality(self, t, data):
        y = data[t]
        if y['I_cases'] == 0:
            return 0
        return y['D_cases'] / y['I_cases']
    
    def R(self, p):
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
    
    def R_effective(self, t, data, params):
        y = data[t]
        if len(inspect.getfullargspec(params)[0]) == 2:
            p = params(t, data)
        else:
            p = params(t)
        return self.R(p) * y['S'] / self.N(t, data)

class Epidemic:
    def __init__(self, model, t0, tmax=200, step_size=np.timedelta64(24,'h'), data=None, verbose=False):
        self.verbose = verbose
        self.model = model

        if type(t0) is pd.Timestamp:
            t0 = t0.to_numpy()
        t0 = np.datetime64(t0, 'h')
        if type(tmax) is pd.Timestamp:
            tmax = tmax.to_numpy()
        if isinstance(tmax, np.datetime64):
            tmax = np.datetime64(tmax, 'h')
        elif isinstance(tmax, np.timedelta64):
            tmax = t0 + tmax
        else:
            tmax = t0 + np.timedelta64(int(tmax),'D')
        self.T = np.arange(t0, tmax+step_size, step_size, dtype='datetime64[h]')

        self.pred = None
        self.data = None
        if data is not None:
            if ~np.all(np.mod(data.index.to_series().diff()[1:], np.timedelta64(1,'D')) == np.timedelta64(0)):
                raise ValueError('data indices must be in (multiples of) days, use data.index.normalize()')
            if data.index.max() < t0:
                raise ValueError('data must have data points after t0 =', np.datetime_as_string(t0))
            data = data.copy().sort_index().filter(self.model.cols)
            if len(data.columns) == 0:
                raise ValueError('data must have column names that match the model')
            self.data = data

    def _check_y0_params(self, y0, params):
        if not isinstance(y0, dict):
            raise ValueError('y0 must be a dictionary')
        if not callable(params):
            raise ValueError('params must be a function')
        names = inspect.getfullargspec(params)[0]
        if len(names) != 1 and len(names) != 2:
            raise ValueError('params function may have two arguments: time and data (optional)')

    def _check_x(self, x, x_bounds, x_params):
        if not isinstance(x, (list, np.ndarray)) or len(x) == 0:
            raise ValueError('x must be list and have a length bigger than zero')
        if not isinstance(x_bounds, list) or len(x_bounds) != len(x) or not all(isinstance(item, tuple) for item in x_bounds) or not all(len(item) == 2 for item in x_bounds):
            raise ValueError('x bounds must be list of tuples (lower and upper boundaries) and have the same length as x')
        if not callable(x_params):
            raise ValueError('x params must be a function')
        names = inspect.getfullargspec(x_params)[0]
        if len(names) != len(x):
            raise ValueError('x params function must have the same number of parameters as x')

        ret = x_params(*x)
        if len(ret) != 2:
            raise ValueError('x params function must return y0 and params function')
        self._check_y0_params(*ret)

    def extend(self, tmax=200, step_size=np.timedelta64(24,'h')):
        epidemic = Epidemic(self.model, self.T[0], tmax, step_size, self.data)
        if self.y0 is not None and self.params is not None:
            epidemic.run(self.y0, self.params)

    @profile
    def run(self, y0, params, tag=None):
        # Run simulation with given y0 and params. If tag is not None, empty or 'mean', it will instead be appended to self.pred where the column names have _tag appended. This is mainly useful for 'lower' and 'upper' curves to display confidence intervals.
        
        self._check_y0_params(y0, params)

        if tag is None or tag == '' or tag == 'mean':
            start = time.time()
            Y = self.model.simulate(self.T, y0, params)
            if self.verbose:
                print('Simulation time:', time.time()-start)
            self.pred = pd.DataFrame(Y, index=self.T, columns=self.model.cols)
            self.y0 = y0
            self.params = params
            self.i_ = len(self.pred)
        else:
            Y = self.model.simulate(self.T, y0, params)
            pred = pd.DataFrame(Y, index=self.T, columns=self.model.cols)
            pred.columns = [col + '_' + tag for col in pred.columns]
            self.pred = pd.concat([self.pred[self.pred.columns.difference(pred.columns)], pred], axis=1)

    def run_parameter(self, name, f):
        if not callable(f):
            raise ValueError('f must be a function')
        names, _, _, defaults, _, _, _ = inspect.getfullargspec(f)
        if inspect.ismethod(f):
            names = names[1:]
        if defaults is not None:
            names = names[:-len(defaults)]

        if len(names) == 0 or len(names) > 3:
            raise ValueError('function must have the following arguments: time t, data (optional), and parameter function params (optional)')

        x = [None] * len(names)
        if len(names) > 1:
            x[1] = self
        if len(names) > 2:
            x[2] = self.params

        v = np.zeros((len(self.T),))
        for i, t in enumerate(self.T):
            self.i_ = i+1
            x[0] = t
            v[i] = f(*x)
        self.pred[name] = v

    def __getitem__(self, t):
        if self.pred is None:
            logging.error('Epidemic hasn\'t been run yet')
            return

        if type(t) is pd.Timestamp or isinstance(t, np.datetime64):
            return self.pred.loc[t]
        return self.pred.iloc[:self.i_].iloc[t]
    
    def __len__(self):
        if self.pred is None:
            logging.error('Epidemic hasn\'t been run yet')
            return

        return self.i_
    
    def max(self, col):
        if self.pred is None:
            logging.error('Epidemic hasn\'t been run yet')
            return

        t = self.pred[col].idxmax()
        return t, self.pred[col].loc[t]

    def error(self, y0=None, params=None):
        if self.pred is None:
            logging.error('Epidemic hasn\'t been run yet')
            return
        if self.data is None:
            logging.error('Epidemic doesn\'t have training data')
            return

        if y0 is None:
            y0 = self.y0
        if params is None:
            params = self.params

        tmax = self.data.index.max()
        step_size = np.timedelta64(1,'D')
        T = np.arange(self.T[0], tmax+step_size, step_size)
        Y = self.model.simulate(T, y0, params)

        # mask is the mask we apply to the output of the model
        # data gets masked to match the mask, the masked output of the model
        mask_model = np.isin(T, self.data.index, assume_unique=True)
        mask_data = np.isin(self.data.index, T, assume_unique=True)

        y_true = {col: self.data[col].to_numpy()[mask_data] for col in self.data.columns}
        y_pred = {col: Y[mask_model,self.model.cols.index(col)] for col in self.data.columns}
        y_true['*'] = np.array([v for v in y_true.values()]).ravel()
        y_pred['*'] = np.array([v for v in y_pred.values()]).ravel()

        df = pd.DataFrame(columns=['*']+list(self.data.columns))
        df.loc['N'] = [np.sum(~np.isnan(y_true[col])) for col in df.columns]
        df.loc['AE'] = [absolute_error(y_true[col], y_pred[col]) for col in df.columns]
        df.loc['SE'] = [squared_error(y_true[col], y_pred[col]) for col in df.columns]
        df.loc['APE'] = [absolute_percentage_error(y_true[col], y_pred[col]) for col in df.columns]
        df.loc['SPE'] = [squared_percentage_error(y_true[col], y_pred[col]) for col in df.columns]
        df.loc['MAE'] = [mean_absolute_error(y_true[col], y_pred[col]) for col in df.columns]
        df.loc['MSE'] = [mean_squared_error(y_true[col], y_pred[col]) for col in df.columns]
        df.loc['MAPE'] = [mean_absolute_percentage_error(y_true[col], y_pred[col]) for col in df.columns]
        df.loc['MSPE'] = [mean_squared_percentage_error(y_true[col], y_pred[col]) for col in df.columns]
        return df

    def cost_function(self, x_params, Reff=None, Reff_weight=0.5, fn=absolute_percentage_error, fast=False):
        if self.data is None:
            logging.error('Epidemic doesn\'t have training data')
            return

        tmax = self.data.index.max()
        step_size = np.timedelta64(1,'D')
        T = np.arange(self.T[0], tmax+step_size, step_size)

        # mask is the mask we apply to the output of the model
        # data gets masked to match the mask, the masked output of the model
        mask_model = np.isin(T, self.data.index, assume_unique=True)
        mask_data = np.isin(self.data.index, T, assume_unique=True)

        cols = [self.model.cols.index(col) for col in self.data.columns]
        data = self.data.to_numpy()
        data = data[mask_data,:]

        def cost(x):
            y0, params = x_params(*x)
            Y = self.model.simulate(T, y0, params, fast=fast)
            Y = Y[mask_model,:]
            if fn is None:
                err = np.array([data[:,idx] - Y[:,col] for idx, col in enumerate(cols)]).ravel()
                #if R0 is not None:
                    #r0 = self._R(params(self, self.t0))
                    #err = np.append(err, np.repeat(np.abs(R0 - r0), int(len(err)*R0_weight)))
                return err[~np.isnan(err)]

            err = np.sum([fn(data[:,idx], Y[:,col]) for idx, col in enumerate(cols)])
            if Reff is not None:
                reff = self.Reff(self.T[0])
                err *= 1.0 + Reff_weight*np.abs(Reff-reff)
            return err
        return cost

    def optimize(self, x0, x_bounds, x_params, method='L-BFGS-B', Reff=None, Reff_weight=0.5, fn=absolute_percentage_error, fast=False, tag=None, **kwargs):
        self._check_x(x0, x_bounds, x_params)
        x = x0
        start = time.time()
        cost = self.cost_function(x_params, Reff=Reff, Reff_weight=Reff_weight, fn=fn, fast=fast)
        if method in ['Nelder-Mead', 'Powell', 'CG', 'BFGS', 'Newton-CG', 'COBYLA', 'trust-constr', 'dogleg', 'trust-ncg', 'trust-exact', 'trust-krylov']:
            logging.error('Optimization method doesn\'t use bounds')
            if 'disp' not in kwargs:
                kwargs['disp'] = True
            res = scipy.optimize.minimize(cost, x0, method=method, options=kwargs)
            if not res.success:
                logging.error('Optimization failed: ' + res.message.decode('utf-8'))
            x = res.x
        elif method in ['L-BFGS-B', 'TNC', 'SLSQP']:
            if 'disp' not in kwargs:
                kwargs['disp'] = True
            res = scipy.optimize.minimize(cost, x0, bounds=x_bounds, method=method, options=kwargs)
            if not res.success:
                logging.error('Optimization failed: ' + res.message.decode('utf-8'))
            x = res.x
        elif method in ['lm']:
            logging.error('Optimization method doesn\'t use bounds')
            cost = self.cost_function(x_params, Reff=Reff, Reff_weight=Reff_weight, fn=None, fast=fast)
            res = scipy.optimize.least_squares(cost, x0, method=method, **kwargs)
            if not res.success:
                logging.error('Optimization failed: ' + res.message.decode('utf-8'))
            x = res.x
        elif method in ['trf', 'dogbox']:
            cost = self.cost_function(x_params, Reff=Reff, Reff_weight=Reff_weight, fn=None, fast=fast)
            lbounds = [b[0] for b in x_bounds]
            ubounds = [b[1] for b in x_bounds]
            res = scipy.optimize.least_squares(cost, x0, bounds=(lbounds,ubounds), method=method, **kwargs)
            if not res.success:
                logging.error('Optimization failed: ' + res.message.decode('utf-8'))
            x = res.x
        elif method == 'annealing':
            res = scipy.optimize.dual_annealing(cost, x_bounds, x0=x0, **kwargs)
            if not res.success:
                logging.error('Optimization failed: ' + res.message.decode('utf-8'))
            x = res.x
        elif method == 'bayesian':
            res = skopt.gp_minimize(cost, x_bounds, x0=x0, **kwargs)
            x = res.x
        elif method == 'gbrt':
            res = skopt.gbrt_minimize(cost, x_bounds, x0=x0, **kwargs)
            x = res.x
        elif method == 'forest':
            res = skopt.forest_minimize(cost, x_bounds, x0=x0, **kwargs)
            x = res.x
        elif method == 'PSO':
            lbounds = np.array([b[0] for b in x_bounds])
            ubounds = np.array([b[1] for b in x_bounds])
            options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}
            optimizer = GlobalBestPSO(n_particles=100, dimensions=len(x0), options=options, bounds=(lbounds,ubounds), **kwargs)

            cost2 = lambda xs: [cost(x) for x in xs]
            res = optimizer.optimize(cost2, iters=1000) 
            x = res[1]
        else:
            raise ValueError('unknown optimization method %s' % method)
        if self.verbose:
            print('Optimization time:', time.time()-start)
            print('Function evaluations:', res.nfev)
        
        if np.array_equal(x0, x):
            logging.warning('Optimization unsuccessful: unable to find more optimal point')

        self.run(*x_params(*x), tag)
        return x

    def param_sensitivity(self, x0, x_bounds, x_params, error_name='MAPE', eps=1e-12):
        self._check_x(x0, x_bounds, x_params)
        orig_error = self.error(*x_params(*x0))

        sensitivity = {}
        names = inspect.getfullargspec(x_params)[0]
        for i in range(len(x0)):
            ran = (x_bounds[i][1] - x_bounds[i][0])
            val = x0[i] + eps
            if val > x_bounds[i][1]:
                val = x0[i] - eps
                if val < x_bounds[i][0]:
                    continue
            x = x0.copy()
            x[i] = val

            error = self.error(*x_params(*x))
            sensitivity[names[i]] = np.abs((error.loc[error_name]-orig_error.loc[error_name]) / (x[i]-x0[i]))
        return pd.DataFrame(sensitivity).T

    def print_params(self, t=None):
        if self.pred is None:
            logging.error('Epidemic hasn\'t been run yet')
            return

        from IPython.core.display import display, HTML

        if t is None:
            t = self.T[0]
        
        args = []
        if len(inspect.getfullargspec(self.params)[0]) == 2:
            args.append(self)

        s = '<table>'
        s += '<tr><th>Parameter</th><th>Value</th>'
        for name, value in self.params(t, *args).items():
            s += '<tr><td>%s</td><td><b>%.4g</b></td></tr>' % (name, value)
        s += '</table>'
        display(HTML(s))
    
    def print_x_params(self, x, x_bounds, x_params):
        self._check_x(x, x_bounds, x_params)

        from IPython.core.display import display, HTML

        s = '<table>'
        s += '<tr><th>Parameter</th><th>Value</th><th>Range</th>'
        names = inspect.getfullargspec(x_params)[0]
        for i in range(len(x)):
            s += '<tr><td>%s</td><td><b>%.4g</b></td><td>[%g, %g]</td></tr>' % (names[i], x[i], x_bounds[i][0], x_bounds[i][1])
        s += '</table>'
        display(HTML(s))

    def print_stats(self):
        if self.pred is None:
            logging.error('Epidemic hasn\'t been run yet')
            return

        from IPython.core.display import display, HTML

        s = '<table>'
        s += '<tr><th>Parameter</th><th>Value</th><th>Date</th></tr>'
        if 'R_effective' in self.pred.columns:
            s += '<tr><td>R effective</td><td><b>%.2f</b></td><td>%s</td></tr>' % (self.pred['R_effective'].iloc[0], np.datetime64(self.pred.index[0],'D'))
            s += '<tr><td>R effective</td><td><b>%.2f</b></td><td>%s</td></tr>' % (self.pred['R_effective'].iloc[-1], np.datetime64(self.pred.index[-1],'D'))
        if 'Fatality' in self.pred.columns:
            s += '<tr><td>Fatality</td><td><b>%.2f</b></td><td>%s</td></tr>' % (self.pred['Fatality'].iloc[-1], np.datetime64(self.pred.index[-1],'D'))
        s += '<tr><td>max(I)</td><td><b>%d</b></td><td>%s</td></tr>' % (self.max('I')[1], np.datetime64(self.max('I')[0],'D'))
        s += '<tr><td>max(H)</td><td><b>%d</b></td><td>%s</td></tr>' % (self.max('H')[1], np.datetime64(self.max('H')[0],'D'))
        s += '<tr><td>max(Hc)</td><td><b>%d</b></td><td>%s</td></tr>' % (self.max('Hc')[1], np.datetime64(self.max('Hc')[0],'D'))
        s += '<tr><td>max(D)</td><td><b>%d</b></td><td>%s</td></tr>' % (self.max('D')[1], np.datetime64(self.max('D')[0],'D'))
        s += '</table>'
        display(HTML(s))
    
    def plot(self, title=None, cols=None, max=[], filename=None):
        if self.pred is None:
            logging.error('Epidemic hasn\'t been run yet')
            return

        if cols is None:
            if self.data is not None:
                cols = [col for col in self.model.cols if col in self.data.columns]
            else:
                cols = ['I', 'H', 'Hc', 'D']

        fig, ax = plt.subplots(figsize=(15,9))
        fig.autofmt_xdate()

        ax.get_xaxis().tick_bottom()    
        ax.get_yaxis().tick_left()

        if title is not None:
            ax.set_title(title, fontsize=20)

        i_color = 0 
        y_max = np.max(self.pred[cols].max())
        for col in cols:
            name = col
            style = '-'
            if col in self.model.names:
                name = self.model.names[col]
            if col in self.model.styles:
                style = self.model.styles[col]
            if col in self.model.colors:
                color = self.model.colors[col]
            else:
                color = tableau20[i_color % len(tableau20)]
                i_color += 1

            if col + '_lower' in self.pred.columns and col + '_upper' in self.pred.columns:
                alpha = 0.2
                if style == '-.':
                    alpha = 0.1
                ax.fill_between(self.pred.index, self.pred[col + '_lower'], self.pred[col + '_upper'], color=color, alpha=alpha)
            ax.plot(self.pred.index, self.pred[col], color=color, lw=3.0, ls=style, label=name)

            if col in max:
                max_t, max_y = self.max(col)
                text_dy = 30
                connection = 'angle,angleA=0,angleB=60'
                if max_y > 0.5*y_max:
                    text_dy = -30
                    connection = 'angle,angleA=0,angleB=120'
                ax.annotate(r'$\mathrm{max}(%s)=%d$' % (col,max_y), xy=(max_t,max_y), xytext=(50,text_dy), textcoords='offset points',
                    arrowprops=dict(arrowstyle='->', connectionstyle=connection, color=color),
                    fontsize=14,
                )
        
        for col in cols:
            if self.data is not None and col in self.data.columns:
                name = col
                if col in self.model.names:
                    name = self.model.names[col]
                if col in self.model.colors:
                    color = self.model.colors[col]
                else:
                    color = tableau20[i_color % len(tableau20)]
                    i_color += 1
                ax.plot(self.data.index, self.data[col], ls='none', marker='.', ms=13, mfc=color, mew=1, mec='white', label=name+' data')

        ax.set_xlim(self.pred.index.min(), self.pred.index.max())
        ax.set_ylim(0, None)
        ax.set_ylabel("# of people", fontsize=14)
        ax.tick_params(bottom=False, top=False, left=False, right=False, labelsize=14)
        
        ax.legend(frameon=False, prop={'size': 14})
        ax.grid()
  
        if filename is not None:
            plt.savefig(filename, bbox_layout='tight')
        plt.show()

    def plot_params(self, title=None, cols=['R_effective'], filename=None):
        if self.pred is None:
            logging.error('Epidemic hasn\'t been run yet')
            return

        fig, ax = plt.subplots(figsize=(15,9))
        fig.autofmt_xdate()

        ax.get_xaxis().tick_bottom()    
        ax.get_yaxis().tick_left()

        if title is not None:
            ax.set_title(title, fontsize=20)

        i_color = 0 
        for col in cols:
            name = col
            style = '-'
            if col in self.model.names:
                name = self.model.names[col]
            if col in self.model.styles:
                style = self.model.styles[col]
            if col in self.model.colors:
                color = self.model.colors[col]
            else:
                color = tableau20[i_color % len(tableau20)]
                i_color += 1

            if col + '_lower' in self.pred.columns and col + '_upper' in self.pred.columns:
                ax.fill_between(self.pred.index, self.pred[col + '_lower'], self.pred[col + '_upper'], color=color, alpha=0.2)
            ax.plot(self.pred.index, self.pred[col], color=color, lw=3.0, ls=style, label=name)
        
        ax.set_xlim(self.pred.index.min(), self.pred.index.max())
        ax.set_ylim(0, None)
        ax.tick_params(bottom=False, top=False, left=False, right=False, labelsize=14)
        
        ax.legend(frameon=False, prop={'size': 14})
        ax.grid()
  
        if filename is not None:
            plt.savefig(filename, bbox_layout='tight')
        plt.show()

    def export(self, filename):
        if not filename.endswith('.csv'):
            filename += ".csv"

        df = pd.DataFrame()
        if self.pred is not None:
            df = pd.concat([df, self.pred], axis=1)
        if self.data is not None:
            data = self.data.copy()
            columns = []
            for col in data.columns:
                columns.append(col + '_data')
            data.columns = columns
            df = pd.concat([df, data], axis=1)
        df.to_csv(filename, index_label='Date', float_format='%.0f')

    # TODO: remove
    #def adjust_betas_to_Reff(self, Reff, Reff_range=None, t=None):
    #    if self.pred is None:
    #        logging.error('Epidemic hasn\'t been run yet')
    #        return

    #    if t is None:
    #        t = self.T[0]
    #    Reff_orig = self.pred['R_effective'].loc[t]

    #    params = self.params
    #    #p = params(self, t)
    #    def adjust(Reff, tag=None):
    #        f = Reff / Reff_orig
    #        #dIm = ((1-f)/f) * (1/p['βIm']) * (p['βE']*y0['E'] + p['βIm']*y0['Im'] + p['βI']*y0['I'] + p['βH']*y0['H'] + p['βHc']*y0['Hc'])
    #        #y0['Im'] += dIm
    #        def adjusted_params(model, t):
    #            p = params(model, t)
    #            p['βE'] *= f
    #            p['βIm'] *= f
    #            p['βI'] *= f
    #            p['βH'] *= f
    #            p['βHc'] *= f
    #            return p
    #        self.run(self.y0, adjusted_params, tag)

    #    adjust(Reff)
    #    if Reff_range is not None:
    #        adjust(Reff_range[0], tag='lower')
    #        adjust(Reff_range[1], tag='upper')

