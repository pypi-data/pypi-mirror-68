import numpy as np
import pandas as pd
import epidemia

# el CSV tiene fechas en las columnas y las regiones como indices
df_infectados = pd.read_csv('../data/chile_minsal_infectados.csv', sep=';', index_col=0)
df_infectados = df_infectados.transpose()
df_infectados.index = pd.to_datetime(df_infectados.index, format='%d-%b') + pd.offsets.DateOffset(years=120)

S0 = {
    'Región Metropolitana': 5.624e6,
    # agrega más regiones
}

def predict(region, Reff, N=1):
    global y0
    
    data = pd.DataFrame({
        'I_cases': df_infectados[region],
    })

    today = data['I_cases'].index.max()  # hoy
    t0 = today - np.timedelta64(14,'D')  # usar últimas dos semanas de datos
    tmax = today + np.timedelta64(14,'D')  # predicir dos semanas más

    model = epidemia.ModelReport2()
    epidemic = epidemia.Epidemic(model, t0, tmax, data=data)

    I0_cases = data['I_cases'].loc[t0]
    I0 = I0_cases
    if t0 - np.timedelta64(14,'D') in data['I_cases']:
        I0 -= data['I_cases'].loc[t0 - np.timedelta64(14,'D')]
    Im0_cases = I0_cases/0.4 * 0.6
    y0 = {'S': S0[region] - I0_cases - Im0_cases, 'E': 0, 'Im': 0, 'I': I0, 'H': 0, 'Hc': 0, 'R': 0, 'D': 0, 'I_cases': I0_cases}

    x = [
        129 * S0[region] / S0['Región Metropolitana'],     # E0
        1799 * S0[region] / S0['Región Metropolitana'],    # Im0    
        0.2,     # γE
        0.1,     # γIm
        0.1,     # γI
        0.1667,  # γH
        0.1,     # γHc
    ]

    x_bounds = [
        (0,3000.0),
        (0,3000.0),
        (0.17,0.25),
        (0.07,0.14),
        (0.07,0.14),
        (0.1,0.5),
        (0.0625,0.14),
    ]

    δ = 0.2
    pE = 0.0563
    pIm = 0.1125
    pI = 0.75
    pH = 0.0
    pHc = 0.0

    def x_params(E0, Im0, γE, γIm, γI, γH, γHc):
        global y0
        
        y0 = y0.copy()
        y0['E'] = E0
        y0['Im'] = Im0
        
        urefE = 1.0
        params = lambda t: {
            'βE':  pE * urefE,
            'βIm': pIm * urefE,
            'βI':  pI * δ * urefE,
            'βH':  pH,
            'βHc': pHc,
            'γE': γE,
            'γIm': γIm,
            'γI': γI,
            'γH': γH,
            'γHc': γHc,
            'μb': 3.57e-5,
            'μd': 1.57e-5,
            'φEI': 0.5,
            'φIR': 0.85,
            'φHR': 0.85,
            'φD': 0.1,
        }
        urefE = Reff / model.R(today, None, params)
        return y0, params

    options = {
        'annealing': {
            'seed': 1234567,
            'maxiter': 1000*N,
            'maxfun': 1e7*N,
            'fast': True,
        },
        'L-BFGS-B': {
            'eps': 1e-12,
        },
    }

    for method in ['annealing', 'L-BFGS-B']:
        opt = {}
        if method in options:
            opt = options[method]
        x = epidemic.optimize(x, x_bounds, x_params, method=method, **opt)
    
    epidemic.run_parameter('R effective', epidemic.model.R_effective)
    return epidemic.export()

# predict hace una predicción con argumentos: región, R effectivo, N el "esfuerzo" para encontrar un ajuste (1 es normal, 2 o 3 duran más tiempo para encontrar el mínimo
df = predict('Región Metropolitana', Reff=1.17, N=1)
print(df)
