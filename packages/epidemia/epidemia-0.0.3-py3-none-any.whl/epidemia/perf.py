import numpy as np

from epidemic import *

t0 = np.datetime64('2020-04-04')
y0 = {'S': 1e7, 'E': 200, 'Im': 200, 'I': 20, 'H': 0, 'Hc': 0, 'R': 0, 'D': 0}

params = lambda t: {
    'βE': 0.062015625,
    'βIm': 0.12403125,
    'βI': 0.165375,
    'βH': 0.0,
    'βHc': 0.0,
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

model = ModelReport2()
epidemic = Epidemic(model, t0, tmax=np.datetime64('2020-06-01'))

for i in range(1000):
    epidemic.run(y0, params)
