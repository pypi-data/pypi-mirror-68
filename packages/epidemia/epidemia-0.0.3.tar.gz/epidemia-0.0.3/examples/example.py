import numpy as np

from epidemic import *

# Initial time and state
t0 = np.datetime64('2020-01-01')
y0 = {'S': 1e7, 'E': 200, 'Im': 200, 'I': 20, 'H': 0, 'Hc': 0, 'R': 0, 'D': 0}

# Our alpha at time 't'
def α(t):
    if t >= np.datetime64('2020-06-01') and t < np.datetime64('2020-09-01'):
        return 0.5
    return 1.0

# Our parameters at time 't'
params = lambda t: {
    'βE': α(t) * 0.062015625,
    'βIm': α(t) * 0.12403125,
    'βI': α(t) * 0.165375,
    'βH': α(t) * 0.0,
    'βHc': α(t) * 0.0,
    'γE': 0.2,
    'γIm': 0.1,
    'γI': 0.1,
    'γH': 0.1666,
    'γHc': 0.1,
    'μb': 3.57e-5,
    'μd': 1.57e-5,
    'φEI': 0.50,
    'φIR': 0.85,
    'φHR': 0.85,
    'φD': 0.50,
}

# Create and run model till time 'tmax'
model = ModelReport2()
epidemic = Epidemic(model, t0, tmax=np.datetime64('2021-06-01'))
epidemic.run(y0, params)
epidemic.run_parameter('R_effective', model.R_effective)
epidemic.run_parameter('α', α)

epidemic.plot('Epidemic', cols=['I', 'H', 'Hc', 'D'], filename='figures/example_plot.png')
epidemic.plot_params('Epidemic (parameters)', cols=['R_effective', 'α'], filename='figures/example_plot_params.png')
