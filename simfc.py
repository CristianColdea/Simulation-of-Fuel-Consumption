"""
This is the computation engine for the fuel consumption simulator.
It is meant to be used as a separate module. In order to use it
one must import this file as a module and make use of the functions.
"""

# engine_speed calculation according to vehicle speed

def engine_speed(v_a, xi_f, xi_g, r_d):
    """
    Function to compute engine speed related to vehicle speed.
    Takes as parameters vehicle speed, in m/s, finale gear ratio,
    gearbox ratio and rolling/dynamic radius of the wheel, in m.
    Returns engine speed in rpm.
    """
    return (9.55 * v_a * xi_f * xi_g) / r_d

#print(engine_speed(20, 4.3, 2.1, 0.32))


# rolling_resistance calculation

def rolling_res(v_a):
    """
    Function to compute rolling resistance coefficient.
    Takes as parameter the vehicle speed.
    Returns the rolling resistance coefficient.
    """
    return 0.0136 + 0.4 * 10**(-7) * v_a**2

#print(rolling_res(20))

# frontal area calculation (if not provided)

def frontal_area(m_a):
    """
    Function to compute the vehicle frontal area for air resistance.
    Takes as parameter the vehicle mass, in kg.
    Returns the frontal area, in squared meters.
    """
    return 1.6 + 0.00056 * (m_a - 765)

#print(frontal_area(1100))

# mu_n function for continuous generation of mu

def mu_n(n, n_max):
    """
    Function to continuously compute mu N fraction required for fuel consumption
    calculation. Takes as parameters the instantaneous engine speed and engine speed
    at rated/nominal output, computes mu N coefficient through linear intepolation
    and returns it.
    Mu N coefficient is meant to highlight engine efficiency distribution over the
    engine speed domain.
    """
    nmu_dict = {0.1:0.88, 0.15:0.895, 0.2:0.91, 0.25:0.92, 0.3:0.93, 0.35:0.94,
                0.4:0.95, 0.45:0.96, 0.5:0.97, 0.55:0.98, 0.6:0.99, 0.65:0.995,
                0.7:1.0, 0.75:1.0, 0.8:1.0, 0.825:1.0, 0.85:1.0, 0.875:1.0,
                0.9:0.995, 0.925:0.995, 0.95:0.99, 0.975:0.98, 1.0:0.97,
                1.025:0.96, 1.05:0.955, 1.075:0.95, 1.1:0.93}

    keys = list(nmu_dict.keys())
    
    for i in range(len(keys) - 1):
        if n/n_max >= keys[i] and n/n_max < keys[i+1]:
            rep = (n/n_max - keys[i])/(keys[i+1] - keys[i])
            return nmu_dict[keys[i]] + (nmu_dict[keys[i+1]] - nmu_dict[keys[i]])*rep
            break
     
#print(mu_n(2800, 5000), '\n')


# mu_P function for continuous generation of mu

def mu_P(P_i, P_max, type = 'SIE'):
    """
    Function to continuously compute mu P fraction required for fuel consumption
    calculation. Takes as parameters the instantaneous engine output, computes mu P
    coefficient according to maximum output at a certain engine speed and engine type,
    gasoline or diesel, and returns it.
    Mu P coefficient is meant to highlight engine efficiency distribution over the
    engine output domain.
    """
    PmuS_dict = {0.1:0.38, 0.2:0.47, 0.3:0.59, 0.4:0.71, 0.5:0.81, 0.6:0.9,
    0.7:0.98,0.8:1.0, 0.9:0.97, 1.0:0.9, 1.1:0.83}

    PmuC_dict = {0.1:0.57, 0.2:0.64, 0.3:0.73, 0.4:0.79, 0.5:0.86, 0.6:0.92,
    0.7:0.97,0.8:1.0, 0.9:0.94, 1.0:0.8, 1.1:0.63}

    keys_S = list(PmuS_dict.keys())
    keys_C = list(PmuC_dict.keys())
    
    if type == 'SIE':
        for i in range(len(keys_S) - 1):
            if P_i/P_max >= keys_S[i] and P_i/P_max < keys_S[i+1]:
                rep = (P_i/P_max - keys_S[i])/(keys_S[i+1] - keys_S[i])
                return PmuS_dict[keys_S[i]] + (PmuS_dict[keys_S[i+1]] -
                       PmuS_dict[keys_S[i]])*rep
                break
    else:
        for i in range(len(keys_C) - 1):
            if P_i/P_max >= keys_C[i] and P_i/P_max < keys_C[i+1]:
                rep = (P_i/P_max - keys_C[i])/(keys_C[i+1] - keys_C[i])
                return PmuC_dict[keys_C[i]] + (PmuC_dict[keys_C[i+1]] -
                       PmuC_dict[keys_C[i]])*rep
                break

#print(mu_P(95, 130, 'CIE'), '\n')
#print(mu_P(95, 130, 'SIE'))


# p_maxn - maximum engine output for a given engine speed

def p_maxn(P_max, n_i, n_max, type = 'SIE'):
    """
    Function to compute engine output according to engine speed.
    The formula used is a polynomial type of third degree, with
    a, b and c coefficients, different for each engine type.
    Takes as parameters maximum engine output, engine speed,
    engine speed at maximum output and engine type.
    Returns the maximum engine output for the given speed.
    """
    if type == 'SIE':
        return P_max * ((n_i/n_max) + (n_i/n_max)**2 - (n_i/n_max)**3)
    else:
        return P_max * ((n_i/n_max) + 0.5 * (n_i/n_max)**2 - 0.5 * (n_i/n_max)**3)

#print(p_maxn(100, 5900, 5700, 'SIE'))


# e_const - the required energy to overcome resistances at a certain speed

def e_const(eta_t, eta_max, mu_n, mu_P, m_a, c_r, C_d, A_f, v_a, S, ro_a):
    """
    Function to compute required energy for constant speed movement.
    Takes as parameters transmission efficiency, the engine peak efficiency,
    engine output coefficient, engine speed coefficient, vehicle mass, in kg,
    rolling resistance coefficient, aerodynamic drag coefficient, frontal
    area of the vehicle, in squared meters, vehicle constant speed, in m/s
    distance, in m and air density.
    Returns the required energy, in J/100 km.
    """
    eta_pen = eta_max * mu_n * mu_P
    E1 = 1/(eta_t * eta_max * mu_n * mu_P) * (m_a * 9.81 * c_r + (ro_a/2) * C_d * A_f *
    v_a**2) * S
    return E1

#print(e_const(0.91, 0.33, 0.92, 0.81, 1150, 0.009, 0.26, 2.16, 20, 100000, 1.225))


# required_power - instant power to be delivered by the engine

def required_power(eta_t, m_a, c_r, C_d, A_f, v_a, a, ro_a):
    """
    Function to compute the required power from the engine, at a given
    moment. Takes as parameters transmission efficiency, vehicle mass, in kg,
    rolling resistance coefficient, aerodynamic drag coefficient, frontal area
    of the vehicle, in squared meters, vehicle speed, in m/s, 
    acceleration, in m/s2 and air density, in kg/m3.
    Returns the required power, in kW.
    """
    P_i = (1/(eta_t * 1000)) * (m_a * 9.81 * c_r + (ro_a/2) * C_d * A_f * v_a**2 +
    m_a * a * 1.08) * v_a
    return P_i
    

#print(required_power(0.91, 1150, 0.009, 0.26, 2.16, 20, 0, 1.225))    

# fuel_cons - fuel consumption

def fuel_cons(E, Q_f, v_a, P_i, ro_f):
    """
    Function to compute vehicle fuel consumption per one hundred km,
    hourly and specific.
    Takes as parameters energy required for vehicle movement and fuel
    calorific value, in J/liter, vehicle speed, in m/s, required power
    and fuel density, in kg/l.
    Returns fuel consumptions in a tuple, in liters/100 km, in kg/hour
    and in kg/kWh.
    """
    fc_100 = E/Q_f
    fc_hour = 0.036 * v_a * fc_100 * ro_f
    fc_s = fc_hour / P_i
    return (fc_100, fc_hour, fc_s)

#print(fuel_cons(106855704, 34200000, 20, 5.255, 0.74))
