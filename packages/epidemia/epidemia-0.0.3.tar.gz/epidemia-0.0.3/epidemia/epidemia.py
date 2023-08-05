import inspect
import time
import logging
logging.basicConfig(format='%(message)s')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import networkx as nx

from .mcmc import *

import scipy
import skopt
from skopt.plots import plot_convergence
from pyswarms.single.global_best import GlobalBestPSO
from pyswarms.single.local_best import LocalBestPSO
from pyswarms.single.general_optimizer import GeneralOptimizerPSO
import pymc3 as pm

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
        self.params = None
        self.Y = None
        pass
    
    def first(self, y0):
        raise NotImplementedError()

    def step(self, t, y, params):
        raise NotImplementedError()

    @profile
    def simulate(self, T, y0, params, fast=False, with_history=True):
        for key, val in y0.items():
            if np.isnan(val):
                logging.error('y0 for %s is NaN' % key)

        self.params = params
        if with_history:
            i = 0
            Y = np.zeros((len(T),len(self.cols)))
            Y[0,:] = self.first(y0)
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
            self.Y = Data()

        # TODO: use scipy.intergrate.solve_ivp instead?
        k = np.zeros((4,len(self.cols)))
        Y = np.zeros((len(T),len(self.cols)))
        Y[0,:] = self.first(y0)
        if fast:
            for i in range(1,len(T)):
                t = T[i-1]
                y = Y[i-1,:]
                Y[i,:] = y + np.array(self.step(t, y, params))
        else:
            for i in range(1,len(T)):
                # Runge-Kutta 4
                t = T[i-1]
                h = T[i]-t
                y = Y[i-1,:]

                f = h / np.timedelta64(1,'D')
                k[0,:] = f * np.array(self.step(t,         y,              params))
                k[1,:] = f * np.array(self.step(t + h/2.0, y + k[0,:]/2.0, params))
                k[2,:] = f * np.array(self.step(t + h/2.0, y + k[1,:]/2.0, params))
                k[3,:] = f * np.array(self.step(t + h,     y + k[2,:],     params))

                Y[i,:] = y + (1.0/6.0)*(k[0,:] + 2.0*k[1,:] + 2.0*k[2,:] + k[3,:])
        return Y

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

        self.pred = {}
        self.y0 = {}
        self.params = {}

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
        t0 = self.T[0]
        if type(tmax) is pd.Timestamp:
            tmax = tmax.to_numpy()
        if isinstance(tmax, np.datetime64):
            tmax = np.datetime64(tmax, 'h')
        elif isinstance(tmax, np.timedelta64):
            tmax = t0 + tmax
        else:
            tmax = t0 + np.timedelta64(int(tmax),'D')
        self.T = np.arange(t0, tmax+step_size, step_size, dtype='datetime64[h]')

        for tag in self.pred.keys():
            self.run(self.y0[tag], self.params[tag], tag=tag)

    @profile
    def run(self, y0, params, tag='default'):
        # Run simulation with given y0 and params. If tag is not None, empty or 'mean', it will instead be appended to self.pred where the column names have _tag appended. This is mainly useful for 'lower' and 'upper' curves to display confidence intervals.
        
        self._check_y0_params(y0, params)

        start = time.time()
        self.tag_ = tag
        Y = self.model.simulate(self.T, y0, params)
        if self.verbose:
            print('Simulation time:', time.time()-start)

        self.pred[tag] = pd.DataFrame(Y, index=self.T, columns=self.model.cols)
        self.y0[tag] = y0
        self.params[tag] = params

    def run_parameter(self, name, f, tag='default'):
        if self.tag_ not in self.pred:
            logging.error('Epidemic hasn\'t been run yet for tag \'%s\'' % tag)
            return

        if not callable(f):
            raise ValueError('f must be a function')
        names = inspect.getfullargspec(f)[0]
        if inspect.ismethod(f):
            names = names[1:]
        if len(names) != 3:
            raise ValueError('function must have the following arguments: time t, data Y, and parameter function params')

        i = 0
        pred = self.pred[tag]
        class Data: 
            def __getitem__(self, t):
                if type(t) is pd.Timestamp or isinstance(t, np.datetime64):
                    return pred.loc[t]
                return pred.iloc[:i+1].iloc[t]
            
            def __len__(self):
                return i
        Y = Data()
        params = self.params[tag]

        v = np.zeros((len(self.T),))
        for i, t in enumerate(self.T):
            v[i] = f(t, Y, params)
        self.pred[tag][name] = v
    
    def max(self, col, tag='default'):
        if tag not in self.pred:
            logging.error('Epidemic hasn\'t been run yet for tag \'%s\'' % tag)
            return

        t = self.pred[tag][col].idxmax()
        return t, self.pred[tag][col].loc[t]

    def error(self, y0=None, params=None, tag='default'):
        if tag not in self.pred:
            logging.error('Epidemic hasn\'t been run yet for tag \'%s\'' % tag)
            return
        if self.data is None:
            logging.error('Epidemic doesn\'t have training data')
            return

        if y0 is None:
            y0 = self.y0[tag]
        if params is None:
            params = self.params[tag]

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

    def cost_function(self, x_params, fn=absolute_percentage_error, fast=False):
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

        if fn is None:
            def cost(x):
                y0, params = x_params(*x)
                Y = self.model.simulate(T, y0, params, fast=fast)
                Y = Y[mask_model,:]
                err = np.array([data[:,idx] - Y[:,col] for idx, col in enumerate(cols)]).ravel()
                return err[~np.isnan(err)]
        else:
            def cost(x):
                y0, params = x_params(*x)
                Y = self.model.simulate(T, y0, params, fast=fast)
                Y = Y[mask_model,:]
                return np.sum([fn(data[:,idx], Y[:,col]) for idx, col in enumerate(cols)])
        return cost

    def optimize(self, x0, x_bounds, x_params, method='L-BFGS-B', fn=absolute_percentage_error, fast=False, tag='default', **kwargs):
        #TODO: add scipy.optimize.differential_evolution
        self._check_x(x0, x_bounds, x_params)

        x = x0
        cost = self.cost_function(x_params, fn=fn, fast=fast)

        start = time.time()
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
            cost = self.cost_function(x_params, fn=None, fast=fast)
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
            opt1 = {key: val for key, val in kwargs.items() if key in ['n_particles', 'options', 'bh_strategy', 'velocity_clamp', 'vh_strategy', 'center', 'ftol', 'ftol_iter']}
            opt2 = {key: val for key, val in kwargs.items() if key in ['iters', 'n_processes', 'verbose']}
            if 'n_particles' not in opt1:
                opt1['n_particles'] = 100
            if 'options' not in opt1:
                opt1['options'] = {'c1': 0.5, 'c2': 0.3, 'w':0.9}
            if 'iters' not in opt2:
                opt1['iters'] = 1000

            lbounds = np.array([b[0] for b in x_bounds])
            ubounds = np.array([b[1] for b in x_bounds])
            optimizer = GlobalBestPSO(dimensions=len(x0), bounds=(lbounds,ubounds), **opt1)

            cost2 = lambda xs: [cost(x) for x in xs]
            res = optimizer.optimize(cost2, **opt2)
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
    
    def optimize_MCMC(self, x0, x_bounds, x_params, x_sigma, iters=1000, tune=500, method='RK45', tag='default'):
        if self.data is None:
            logging.error('Epidemic doesn\'t have training data')
            return

        self._check_x(x0, x_bounds, x_params)
        if not isinstance(x_sigma, (list, np.ndarray)) or len(x_sigma) != len(x0):
            raise ValueError('x sigma must be list and have the same length as x0')
        y0, _params = x_params(*x0)
        if len(inspect.getfullargspec(_params)[0]) != 1:
            raise ValueError('params function may only have one arguments: time')


        # Observations
        tmax = self.data.index.max()
        step_size = np.timedelta64(1,'D')
        T = np.arange(self.T[0], tmax+step_size, step_size)

        # mask is the mask we apply to the output of the model
        # data gets masked to match the mask, the masked output of the model
        T = T[np.isin(T, self.data.index, assume_unique=True)]
        mask_data = np.isin(self.data.index, T, assume_unique=True)

        cols = [self.model.cols.index(col) for col in self.data.columns]
        data = self.data.to_numpy()
        data = data[mask_data,:]


        # Model
        print('diffeq')
        y0, _ = x_params(*x0)
        y0 = self.model.first(y0)
        options = {'method': method}
        diffeq = DifferentialEquation(func=self.model.step, t0=self.T[0], times=T,
                                      n_states=len(y0), n_theta=len(x0),
                                      model=self.model, x_params=x_params, options=options)


        print('model')
        names = inspect.getfullargspec(x_params)[0]
        with pm.Model():
            print('vars')
            lbounds = np.array([b[0] for b in x_bounds])
            ubounds = np.array([b[1] for b in x_bounds])
            variables = [pm.Bound(pm.Normal, lower=lbounds[i], upper=ubounds[i])(names[i], mu=x0[i], sigma=x_sigma[i]) for i in range(len(x0))]

            print('sigma')
            sigma = pm.HalfCauchy('sigma', 1, shape=len(cols))
            print('model')
            model = diffeq(y0=y0, theta=variables)[cols]
            print('obs')
            pm.Lognormal('Y', mu=pm.math.log(model), sd=sigma, observed=data)

            print('nuts')
            step = pm.NUTS()
            trace = pm.sample(1000, tune=tune)
            pm.traceplot(trace)
            plt.show()
            pm.autocorrplot(trace)
            plt.show()
            pm.summary(trace).round(2)
            plt.show()

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

    def print_params(self, t=None, tag='default'):
        if tag not in self.pred:
            logging.error('Epidemic hasn\'t been run yet for tag \'%s\'' % tag)
            return

        from IPython.core.display import display, HTML

        if t is None:
            t = self.T[0]
        
        args = []
        if len(inspect.getfullargspec(self.params[tag])[0]) == 2:
            args.append(self)

        s = '<table>'
        s += '<tr><th>Parameter</th><th>Value</th>'
        for name, value in self.params[tag](t, *args).items():
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

    def print_stats(self, tag='default'):
        if tag not in self.pred:
            logging.error('Epidemic hasn\'t been run yet for tag \'%s\'' % tag)
            return

        from IPython.core.display import display, HTML

        s = '<table>'
        s += '<tr><th>Parameter</th><th>Value</th><th>Date</th></tr>'
        if 'R_effective' in self.pred[tag].columns:
            s += '<tr><td>R effective</td><td><b>%.2f</b></td><td>%s</td></tr>' % (self.pred[tag]['R_effective'].iloc[0], np.datetime64(self.pred[tag].index[0],'D'))
            s += '<tr><td>R effective</td><td><b>%.2f</b></td><td>%s</td></tr>' % (self.pred[tag]['R_effective'].iloc[-1], np.datetime64(self.pred[tag].index[-1],'D'))
        if 'Fatality' in self.pred[tag].columns:
            s += '<tr><td>Fatality</td><td><b>%.2f</b></td><td>%s</td></tr>' % (self.pred[tag]['Fatality'].iloc[-1], np.datetime64(self.pred[tag].index[-1],'D'))
        s += '<tr><td>max(I)</td><td><b>%d</b></td><td>%s</td></tr>' % (self.max('I', tag)[1], np.datetime64(self.max('I', tag)[0],'D'))
        s += '<tr><td>max(H)</td><td><b>%d</b></td><td>%s</td></tr>' % (self.max('H', tag)[1], np.datetime64(self.max('H', tag)[0],'D'))
        s += '<tr><td>max(Hc)</td><td><b>%d</b></td><td>%s</td></tr>' % (self.max('Hc', tag)[1], np.datetime64(self.max('Hc', tag)[0],'D'))
        s += '<tr><td>max(D)</td><td><b>%d</b></td><td>%s</td></tr>' % (self.max('D', tag)[1], np.datetime64(self.max('D', tag)[0],'D'))
        s += '</table>'
        display(HTML(s))
    
    def plot(self, title=None, cols=None, filename=None, mean='default', lower='lower', upper='upper'):
        if mean not in self.pred:
            logging.error('Epidemic hasn\'t been run yet for tag \'%s\'' % mean)
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
        y_max = np.max(self.pred[mean][cols].max())
        if upper in self.pred:
            y_max = max(y_max, np.max(self.pred[upper][cols].max()))
        if lower in self.pred:
            y_max = max(y_max, np.max(self.pred[lower][cols].max()))

        for col in cols:
            name = '$' + col + '$'
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

            if lower in self.pred and upper in self.pred:
                alpha = 0.2
                if style == '-.':
                    alpha = 0.1
                ax.fill_between(self.T, self.pred[lower][col], self.pred[upper][col], color=color, alpha=alpha)
            ax.plot(self.T, self.pred[mean][col], color=color, lw=3.0, ls=style, label=name)

            #if col in max:
            #    max_t, max_y = self.max(col)
            #    text_dy = 30
            #    connection = 'angle,angleA=0,angleB=60'
            #    if max_y > 0.5*y_max:
            #        text_dy = -30
            #        connection = 'angle,angleA=0,angleB=120'
            #    ax.annotate(r'$\mathrm{max}(%s)=%d$' % (col,max_y), xy=(max_t,max_y), xytext=(50,text_dy), textcoords='offset points',
            #        arrowprops=dict(arrowstyle='->', connectionstyle=connection, color=color),
            #        fontsize=14,
            #    )
        
        for col in cols:
            if self.data is not None and col in self.data.columns:
                name = '$' + col + '$'
                if col in self.model.names:
                    name = self.model.names[col]
                if col in self.model.colors:
                    color = self.model.colors[col]
                else:
                    color = tableau20[i_color % len(tableau20)]
                    i_color += 1
                ax.plot(self.data.index, self.data[col], ls='none', marker='.', ms=13, mfc=color, mew=1, mec='white', label=name+' data')

        ax.set_xlim(np.min(self.T), np.max(self.T))
        ax.set_ylim(0, None)
        ax.set_ylabel("# of people", fontsize=14)
        ax.tick_params(bottom=False, top=False, left=False, right=False, labelsize=14)
        
        ax.legend(frameon=False, prop={'size': 14})
        ax.grid()
  
        if filename is not None:
            plt.savefig(filename, bbox_layout='tight')
        plt.show()

    def plot_params(self, title=None, cols=['R_effective'], filename=None, mean='default', lower='lower', upper='upper'):
        if mean not in self.pred:
            logging.error('Epidemic hasn\'t been run yet for tag \'%s\'' % mean)
            return

        fig, ax = plt.subplots(figsize=(15,9))
        fig.autofmt_xdate()

        ax.get_xaxis().tick_bottom()    
        ax.get_yaxis().tick_left()

        if title is not None:
            ax.set_title(title, fontsize=20)

        i_color = 0 
        for col in cols:
            name = '$' + col + '$'
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

            if lower in self.pred and upper in self.pred:
                ax.fill_between(self.T, self.pred[lower][col], self.pred[upper][col], color=color, alpha=0.2)
            ax.plot(self.T, self.pred[mean][col], color=color, lw=3.0, ls=style, label=name)
        
        ax.set_xlim(np.min(self.T), np.max(self.T))
        ax.set_ylim(0, None)
        ax.tick_params(bottom=False, top=False, left=False, right=False, labelsize=14)
        
        ax.legend(frameon=False, prop={'size': 14})
        ax.grid()
  
        if filename is not None:
            plt.savefig(filename, bbox_layout='tight')
        plt.show()

    def export(self, filename=None, tag='default'):
        df = pd.DataFrame()
        if tag in self.pred:
            df = pd.concat([df, self.pred[tag]], axis=1)
        if self.data is not None:
            data = self.data.copy()
            columns = []
            for col in data.columns:
                columns.append(col + '_data')
            data.columns = columns
            df = pd.concat([df, data], axis=1)

        if filename is not None:
            if not filename.endswith('.csv'):
                filename += ".csv"
            df.to_csv(filename, index_label='Date', float_format='%.0f')
        else:
            return df

