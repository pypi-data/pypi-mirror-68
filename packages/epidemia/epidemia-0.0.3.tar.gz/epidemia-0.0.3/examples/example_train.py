import numpy as np
import pandas as pd

from epidemic import *

# Load our training data
df_infectados = pd.read_csv('data/chile_minsal_infectados.csv', sep=';', index_col=0)
df_infectados = df_infectados.transpose()
df_infectados.index = pd.to_datetime(df_infectados.index, format='%d-%b') + pd.offsets.DateOffset(years=120)

df_fallecidos = pd.read_csv('data/chile_minsal_fallecidos.csv', sep=';', index_col=0)
df_fallecidos = df_fallecidos.transpose()
df_fallecidos.index = pd.to_datetime(df_fallecidos.index, format='%d-%b') + pd.offsets.DateOffset(years=120)

data = pd.DataFrame({
    'I_cases': df_infectados['Región Metropolitana'],
    'D': df_fallecidos['Región Metropolitana'],
})

# Initial time and state
t0 = np.datetime64('2020-04-04')

I0 = data['I_cases'].loc[t0]
D0 = data['D'].loc[t0]

# Define our training parameters: initial value, bounds, and mapping function to model parameters
x = [
    0.74,   # E0
    10.3,   # Im0
    0.38,   # CE
    0.75,   # CIm
    0.165,  # βI
    0.2,    # γE
    0.1,    # γIm
    0.1,    # γI
    0.1667, # γH
    0.1,    # γHc
]

x_bounds = [
    (0,20),        # E0
    (0,20),        # Im0
    (0.0,0.4),     # CE
    (0.0,0.9),     # CIm
    (0.0,0.75),    # βI
    (0.17,0.25),   # γE
    (0.07,0.14),   # γIm
    (0.07,0.14),   # γI
    (0.1,0.5),     # γH
    (0.0625,0.14), # γHc
]

def x_params(E0, Im0, CE, CIm, βI, γE, γIm, γI, γH, γHc):
    y0 = {
        'S': 1e7,
        'E': E0 * I0,
        'Im': Im0 * I0,
        'I': I0,
        'H': 0,
        'Hc': 0,
        'R': 0,
        'D': D0,
    }
    
    λ1 = np.datetime64('2020-04-15')
    κ1 = 0.05
    α2 = 0.75
    α = lambda t: 1.0 if t < λ1 else α2 + (1.0-α2)*np.exp(-κ1*(t-λ1)/np.timedelta64(1,'D'))
    return y0, lambda t: {
        'βE': α(t)*CE*βI,
        'βIm': α(t)*CIm*βI,
        'βI': α(t)*βI,
        'βH': 0.0,
        'βHc': 0.0,
        'γE': γE,
        'γIm': γIm,
        'γI': γI,
        'γH': γH,
        'γHc': γHc,
        'μb': 3.57e-5,
        'μd': 1.57e-5,
        'φEI': 0.5,
        'φIR': 0.6,
        'φHR': 0.6,
        'φD': 0.2,
    }

# Create model till time 'tmax'
model = ModelReport2()
epidemic = Epidemic(model, t0, tmax=np.datetime64('2020-06-01'), data=data)

# Optimize using dual_annealing and L-BFGS-B subsequently
options = {
    'annealing': {
        'seed': 1234567,
        'fast': True,
    },
    'L-BFGS-B': {
        'disp': True,
    },
}

for method in ['annealing', 'L-BFGS-B']:
    opt = {}
    if method in options:
        opt = options[method]
    x = epidemic.optimize(x, x_bounds, x_params, method=method, **opt)

epidemic.plot(cols=['I_cases', 'I'])
epidemic.plot(cols=['D'])
