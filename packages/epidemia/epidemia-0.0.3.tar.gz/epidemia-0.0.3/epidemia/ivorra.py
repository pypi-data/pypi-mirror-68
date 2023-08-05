df_confirmed = pd.read_csv('data_confirmed.csv')
df_confirmed.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
df_confirmed = df_confirmed.groupby('Country/Region').sum()
df_confirmed = df_confirmed.transpose()
df_confirmed.index = pd.to_datetime(df_confirmed.index)

df_recovered = pd.read_csv('data_recovered.csv')
df_recovered.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
df_recovered = df_recovered.groupby('Country/Region').sum()
df_recovered = df_recovered.transpose()
df_recovered.index = pd.to_datetime(df_recovered.index)

df_deaths = pd.read_csv('data_deaths.csv')
df_deaths.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
df_deaths = df_deaths.groupby('Country/Region').sum()
df_deaths = df_deaths.transpose()
df_deaths.index = pd.to_datetime(df_deaths.index)

I = df_confirmed['China'].copy()
R = df_recovered['China'].copy()
D = df_deaths['China'].copy()

# adjust infection data
idx_adj = pd.date_range(I.index.min(), '2020-02-13', freq='D')
data_adj = [17410*(I[I.index.min():t].sum()/I[idx_adj].sum()) for t in idx_adj]
I_adj = pd.Series(data_adj, index=idx_adj)
I_adj['2020-02-13'] -= 14000
I = I.add(I_adj, fill_value=0)

#jan24 = np.datetime64('2020-01-24')
#feb08 = np.datetime64('2020-02-08')
#θ = lambda t: 0.14 if t < jan24 else (
#              0.65 if t >= feb08 else (
#              0.14 + (0.65-0.14)*((t-jan24)/np.timedelta64(1,'D')/16)))

data = pd.DataFrame({'I_cases': df_confirmed['China'], 'R_cases': df_recovered['China'], 'D_cases': df_deaths['China']})


ivorra21M_x0 = [0.3373, 0.8450, 0.3622, 7.0004, 0.1815, 0.0050, 0.1200, 0.9515, 0.665]
ivorra25F_x0 = [0.2771, 0.9426, 0.6336, 13.9, 0.1070, 0.0458, 0.1272, 0.9515, 0.665]
ivorra8F_x0 = [0.4526, 0.2665, 0.9255, 13.2, 0.1476, 0.0330, 0.1647, 0.9515, 0.665]
ivorra29J_x0 = [0.5000, 0.1543, 0.9988, 13.7, 0.1128, 0.0500, 0.2354, 0.9515, 0.665]

ivorra_x_bounds = [(1e-6,0.5), (0.0,1.0), (0.0,1.0), (7.0,14.0),
                   (0.0,0.2), (0.005,0.05), (0.0,1.0),
                   (0.0,1.0), (0.0,1.0)]

def ivorra_x_params(βI, CE, CIm, δR, δω, ωc, κ1, φIR, φHR):
    # notation differences with Ivorra paper:
    # βIu, γInf, dIu => βIm, γIm, dIm
    # βId, dId => βI, dI
    # βHR, γHR => βH, γH
    # βHD, γHD => βHc, γHc
    # ω top bar => ωnc
    # ω bottom bar => ωc
    # φIR and φHR are not known in Ivorra
    
    λ1 = np.datetime64('2020-02-01')
    m = lambda t: 1.0 if t < λ1 else np.exp(-κ1*(t-λ1)/np.timedelta64(1,'D'))
    
    ωnc = ωc + δω
    ω = lambda t: m(t)*ωnc + (1-m(t))*ωc
    
    θt0 = np.datetime64('2020-01-24')
    θt1 = np.datetime64('2020-02-08')
    θ = lambda t: 0.86 if t < θt0 else (0.35 if t > θt1 else 0.86+(0.35-0.86)*(t-θt0)/(θt1-θt0))
        
    dg = 5.7
    dE = 5.5
    dI = 6.7
    dIm = 14
    dH = (dIm-dI)
    g = lambda t: dg*(1-m(t))
    γE = 1/ dE
    γIm = 1/ dIm
    γI = lambda t: 1 / (dI - g(t))
    γH = lambda t: 1 / (dIm - dI + g(t))
    γHc = 1 / (dH + δR)    
    
    βE = CE*βI
    βIm = CIm*βI
    CH = lambda t: 0.0275*(βI/γI(t) + βE/γE)/((1-0.0275)*βI*((1-ω(t))/γH(t) + ω(t)/γHc))
    βH = lambda t: CH(t)*βI
    βHc = lambda t: CH(t)*βI
            
    return lambda t: {'βE': m(t)*βE, 
                      'βIm': m(t)*βIm,
                      'βI': m(t)*βI,
                      'βH': m(t)*βH(t),
                      'βHc': m(t)*βHc(t),
                      'γE': γE,
                      'γIm': γIm,
                      'γI': γI(t),
                      'γH': γH(t),
                      'γHc': γHc,
                      'μb': 0.0,
                      'μd': 0.0,
                      'φEI': θ(t),
                      'φIR': φIR,
                      'φHR': φHR,
                      'φD': ω(t)}
