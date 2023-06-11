"""
This is the computation engine for the fuel consumption simulator.
It is meant to be used as a separate module. In order to use it
one must import this file as a module and make use of the functions
and methods.
"""

# engine_speed calculation according to vehicle speed

def engine_speed(v_a, xi_f, xi_g, r_d, s_f, n_max, n_idle=800):
    """
    Function to compute engine speed related to vehicle speed.
    Takes as parameters vehicle speed, in m/s, final gear ratio,
    gearbox ratio, rolling/dynamic radius of the wheel, in m,
    the slip factor, the engine max speed, in rpm,
    and the idle speed, in rpm.
    Returns engine speed in rpm.
    CAVEAT: Actual engine speed cannot exceed maximum value
    """
    n_i = (9.55 * v_a * xi_f * xi_g * s_f) / r_d

    if n_i < n_idle:
        return n_idle

    if n_i <= n_max and n_i >= n_idle:
        return n_i
    else:
        print("The engine speed exceeded MAX.\n"
              "Please readjust!")
        exit()


# rolling_resistance calculation (if not provided)

def rolling_res(v_a):
    """
    Function to compute rolling resistance coefficient.
    Takes as parameter the vehicle speed.
    Returns the rolling resistance coefficient.
    """
    return 0.0136 + 0.4 * 10**(-7) * v_a**2


# frontal area calculation (if not provided)

def frontal_area(m_a):
    """
    Function to compute the vehicle frontal area for air resistance.
    Takes as parameter the vehicle mass, in kg.
    Returns the frontal area, in squared meters.
    """
    return 1.6 + 0.00056 * (m_a - 765)


"""
class to compute the engine penalties over speed and output domains
"""

class Mus:
    def __init__(self, P_max, n_max, n_i, engine_tp):
        self.P_max = P_max
        self.n_max = n_max
        self.n_i = n_i
        self.engine_tp = engine_tp

    # p_maxn - maximum engine output for a given engine speed (if not available)

    def p_maxn(P_max, n_i, n_max, engine_tp = 'SIE'):
        """
        Method to compute engine output according to engine speed.
        The formula used is a polynomial type of third degree, with
        a, b and c coefficients, different for each engine type.
        Takes as parameters maximum engine output, engine speed,
        engine speed at maximum output and engine type.
        Returns the maximum engine output for the given speed.
        """
        if engine_tp == 'SIE':
            return P_max * ((n_i/n_max) + (n_i/n_max)**2 - (n_i/n_max)**3)
        else:
            return P_max * ((n_i/n_max) + 0.5 * (n_i/n_max)**2 - 0.5 * (n_i/n_max)**3)

    # mu_n function for continuous generation of muN

    def mu_n(n, n_max, n_idle=800):
        """
        Method to continuously compute mu N fraction required for fuel consumption
        calculation. Takes as parameters the instantaneous engine speed, engine speed
        at rated/nominal output and the engine idle speed, computes mu N coefficient
        through linear intepolation and returns it.
        Mu N coefficient is meant to highlight engine efficiency distribution over the
        engine speed domain.
        """
        nmu_dict = {0.1:0.88, 0.15:0.895, 0.2:0.91, 0.25:0.92, 0.3:0.93,
                    0.35:0.94, 0.4:0.95, 0.45:0.96, 0.5:0.97, 0.55:0.98,
                    0.6:0.99, 0.65:0.995, 0.7:1.0, 0.75:1.0, 0.8:1.0, 0.825:1.0,
                    0.85:1.0, 0.875:1.0, 0.9:0.995, 0.925:0.995, 0.95:0.99,
                    0.975:0.98, 1.0:0.97, 1.025:0.96, 1.05:0.955, 1.075:0.95,
                    1.1:0.93}

        keys = list(nmu_dict.keys())
        if (n_idle/n_max) <= 0.1:
            return 0.87
        else: 
            for i in range(len(keys) - 1):
                if n/n_max >= keys[i] and n/n_max < keys[i+1]:
                    rep = (n/n_max - keys[i])/(keys[i+1] - keys[i])
                    return nmu_dict[keys[i]] + (nmu_dict[keys[i+1]] -\
                        nmu_dict[keys[i]])*rep
                    break
     

    # mu_P function for continuous generation of muP

    def mu_P(P_i, P_max, engine_tp = 'SIE'):
        """
        Method to continuously compute mu P fraction required for fuel consumption
        calculation. Takes as parameters the instantaneous engine output and the maximum
        output at the given engine speed, computes mu P coefficient according to maximum
        output at a certain engine speed and engine type, gasoline or diesel, and
        returns it.
        Mu P coefficient is meant to highlight engine efficiency distribution over the
        engine output domain.
        """
        PmuS_dict = {0.1:0.38, 0.2:0.47, 0.3:0.59, 0.4:0.71, 0.5:0.81, 0.6:0.9,
                     0.7:0.98,0.8:1.0, 0.9:0.97, 1.0:0.9, 1.1:0.83}

        PmuC_dict = {0.1:0.57, 0.2:0.64, 0.3:0.73, 0.4:0.79, 0.5:0.86, 0.6:0.92,
                     0.7:0.97,0.8:1.0, 0.9:0.94, 1.0:0.8, 1.1:0.63}

        keys_S = list(PmuS_dict.keys())
        keys_C = list(PmuC_dict.keys())

        print("Outputs ratio is: ", P_i/P_max)
        # return fraction if the output is too low
        if P_i/P_max < 0.1:
            return 0.56 

        if engine_tp == 'SIE':
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


"""
class to compute the required energies to overcome resistances
and to accelerate the vehicle to a certain speed
"""

class Energy:
    def __init__(self, eta_t, eta_max, mu_n_init, mu_n_fin, mu_P_init, mu_P_fin,
                 m_a, c_r, C_d, A_f, v_init, ro_a, a, t, gamma_m):

        self.eta_t = eta_t
        self.eta_max = eta_max
        self.mu_n_init = mu_n_init
        self.mu_n_fin = mu_n_fin
        self.mu_P_init = mu_P_init
        self.mu_P_fin = mu_P_fin
        self.m_a = m_a
        self.c_r = c_r
        self.C_d = C_d
        self.A_f = A_f
        self.v_init = v_init
        self.ro_a = ro_a
        self.gamma_m = gamma_m
    
    # e_const - the required energy to overcome resistances during movement
    # at a certain constant speed

    def e_const(eta_t, eta_max, mu_n_init, mu_P_init, m_a, c_r, C_d, A_f, v_init,
                ro_a=1.225):
        """
        Method to compute required energy for constant speed movement.
        Takes as parameters transmission efficiency, the engine peak efficiency,
        engine speed coefficient, engine output coefficient, vehicle mass, in kg,
        rolling resistance coefficient, aerodynamic drag coefficient, frontal
        area of the vehicle, in squared meters, vehicle constant speed, in m/s,
        and air density, in kg/m**3.
        Returns the required energy, in J/100 km.
        """
        Ec = 1/(eta_t * eta_max * mu_n_init * mu_P_init) * (m_a * 9.81 * c_r +
             (ro_a/2) * C_d * A_f * v_init**2) * 100000
     
        return Ec
     
    # e_kin - the required kinetic energy to accelerate the vehicle
    
    def e_kin(eta_t, eta_max, mu_n_init, mu_n_fin, mu_P_init, mu_P_fin, m_a,
              v_init, a, t, gamma_m=1.08):
        """
        Method to compute required kinetic energy to accelerate the vehicle.
        Takes as parameters transmission efficiency, the engine peak efficiency,
        engine speed coefficient initial and final, engine output coefficient,
        initial and final, vehicle mass, in kg, vehicle initial speed, in m/s,
        constant acceleration, in m/s**2, acceleration time, in s and the
        coefficient of rotational masses.
        Returns the required energy, in J/100 km.
        """
        #same multiplier for all three terms
        C1 = (0.5 * m_a * gamma_m)/(eta_t * eta_max) 
        
        # first term of the kinetic energy
        Ek_a = C1 * v_init**2 * ((mu_n_init * mu_P_init - mu_n_fin * mu_P_fin) /
               mu_n_init * mu_P_init) * (100000 / (v_init * t + 0.5 * a * t**2))
        
        # second term
        Ek_b = ((2 *  C1 * v_init * a * t)/( mu_n_fin * mu_P_fin)) * (100000 /
               (v_init * t + 0.5 * a * t**2))

        # third term
        Ek_c = (C1 * a**2 * (t ** 2))/(mu_n_fin * mu_P_fin)* (100000 / (v_init *
               t + 0.5 * a * t**2))

      
        return (Ek_a + Ek_b + Ek_c) 

    # e_roll - the required energy to overcome rolling resistance during
    # acceleration
    
    def e_roll(eta_t, eta_max, mu_n_fin, mu_P_fin, m_a, v_init, c_r, a, t):
        """
        Method to compute required energy to overcome the rolling resistance
        of the vehicle.
        Takes as parameters transmission efficiency, the engine peak efficiency,
        engine speed coefficient final, engine output coefficientfinal,\
        vehicle mass, in kg, vehicle initial speed, in m/s,
        the rolling resistance coefficient, constant acceleration, in m/s**2
        and acceleration time, in s.
        Returns the required energy, in J/100 km.
        """
        #same multiplier for all two terms
        C2 = ( m_a * 9.81 * c_r)/(eta_t * eta_max * mu_n_fin * mu_P_fin)

        # first term of rolling energy
        Er_a = C2 * v_init * t * (100000 / (v_init * t + 0.5 * a * t**2))

        # second term
        Er_b = 0.5 * C2 * a * t**2 * (100000 / (v_init * t + 0.5 * a * t**2))

        return (Er_a + Er_b) 

    # e_air - the required energy to overcome air resistance during acceleration

    def e_air(eta_t, eta_max, mu_n_fin, mu_P_fin, v_init, C_d, A_f, a, t,
              ro_air=1.225):
        """
        Method to compute required energy to overcome the air resistance
        of the vehicle.
        Takes as parameters transmission efficiency, the engine peak efficiency,
        engine speed coefficient final, engine output coefficient
        final, vehicle initial speed, in m/s, the air resistance coefficient,
        the vehicle frontal area, constant acceleration, in m/s**2,
        acceleration time, in s and air density, in kg/m**3.
        Returns the required energy, in J/100 km.
        """
        #same multiplier for all four terms
        C3 = (0.5 * ro_air * C_d * A_f)/(eta_t * eta_max * mu_n_fin * mu_P_fin)
        
        # first term of energy required to overcome air drag
        Ea_a = C3 * t * v_init**3 * (100000 / (v_init * t + 0.5 * a * t**2))

        # second term
        Ea_b = C3 * t**2 * 2.5 * a * v_init**2 * (100000 / (v_init * t + 0.5 *
               a * t**2))

        # third term
        Ea_c = C3 * t**3 * 2 * v_init * a**2 * (100000 / (v_init * t + 0.5 *
               a * t**2))

        # fourth term
        Ea_d = C3 * 0.5 * a**3 * t**3 * (100000 / (v_init * t + 0.5 * a * t**2))

        return (Ea_a + Ea_b + Ea_c + Ea_d)



# required_power - instant power to be delivered by the engine

def required_power(eta_t, m_a, c_r, C_d, A_f, v_a, a, p_maxn, ro_a=1.225):
    """
    Function to compute the required power from the engine, at a given
    moment. Takes as parameters transmission efficiency, vehicle mass, in kg,
    rolling resistance coefficient, aerodynamic drag coefficient, frontal area
    of the vehicle, in squared meters, vehicle speed, in m/s, 
    acceleration, in m/s**2 and air density, in kg/m**3.
    Returns the required power, in kW.
    CAVEAT: The required output of the engine cannot exceed maximum value for the
            given engine speed
    """
    P_i = (1/(eta_t * 1000)) * (m_a * 9.81 * c_r + (ro_a/2) * C_d * A_f * v_a**2 +
          m_a * a * 1.08) * v_a
    if P_i <= p_maxn:
        return P_i
    else:
        print("The engine output exceeded MAX for the given conditions.\n"
              "Please readjust!")
      
        exit()
    
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


"""
Within this second section the functions and methods are called
"""

def simfc_call(fixs, v_init, xi_g, a, t):
    """
    Function to call all functions and methods previously defined.
    The meaning of function parameters is indicated throughout this script 
    and in the 'passing_args' explanatory document.
    Returns the specific fuel consumption, in kg/kWh.
    CAVEAT: Vehicle speed is limited by the engine maximum speed and the
            transsmision overall ratio. Vehicle required power is limited by
            the maximum engine output for the given engine speed.
    """
    
    # unpacking the fixed variables list into a dict
    # vars list
    vars = ['xi_f', 's_f', 'r_d', 'n_max', 'P_max', 'type', 'eta_t',
            'eta_max', 'm_a', 'c_r', 'C_d', 'A_f', 'ro_a', 'Q_f', 'ro_f'] 
    dict_fix = {}
    # dict_fix = dict(zip(vars, fixs))   this approach gives a type error
    for index in range(len(vars)):
        dict_fix[vars[index]] = fixs[index]
    
    # vehicle maximum speed
    v_max = (dict_fix['n_max'] * dict_fix['r_d']) / (9.55 * dict_fix['xi_f'] *
            xi_g * dict_fix['s_f'])
    if v_init >= v_max:
        v_init = v_max
        print("Initial speed is too high.\n",
              "It was automatically readjusted to MAX value possible!")

    
    # 1) the case of uniform vehicle movement (i.e., a = 0)
    if a == 0:
        # engine speed
        n_i = engine_speed(v_init, dict_fix['xi_f'], xi_g, dict_fix['r_d'],
                           dict_fix['s_f'], dict_fix['n_max'])

        
        # engine speed penalty mu_n
        mu_n = Mus.mu_n(n_i, dict_fix['n_max'])
        
        # engine maximum power at the given engine speed
        p_maxn = Mus.p_maxn(dict_fix['P_max'], n_i, dict_fix['n_max'])

        # engine instantaneous power
        P_i = required_power(dict_fix['eta_t'], dict_fix['m_a'], dict_fix['c_r'],
                             dict_fix['C_d'], dict_fix['A_f'], v_init, a,
                             dict_fix['P_max'])

        
        # engine output penalty mu_P
        mu_P = Mus.mu_P(P_i, p_maxn)

        # energy required to overcome resistances at the given constant speed
        e_const = Energy.e_const(dict_fix['eta_t'], dict_fix['eta_max'], mu_n,
                                 mu_P, dict_fix['m_a'], dict_fix['c_r'],
                                 dict_fix['C_d'], dict_fix['A_f'], v_init)

        # fuel consumption
        f_cons = fuel_cons(e_const, dict_fix['Q_f'], v_init, P_i,
                              dict_fix['ro_f'])
    
    else:
        # vehicle actual speed after acceleration a applied during time t
        v = int(v_init + (a * t))
        if v > v_max:
            v = v_max
            print("The vehicle speed is too high.\n",
                  "It was automatically readjusted to MAX value possible!")
            
        # engine speed at initial vehicle speed
        n_i_init = engine_speed(v_init, dict_fix['xi_f'], xi_g, dict_fix['r_d'],
                                dict_fix['s_f'], dict_fix['n_max'])
        #print(n_i_init)
        
        # engine speed initial penalty
        mu_n_init = Mus.mu_n(n_i_init, dict_fix['n_max'])
        
        # engine initial maximum power at the given engine speed
        p_maxn_init = Mus.p_maxn(dict_fix['P_max'], n_i_init, dict_fix['n_max'])

        # engine initial instantaneous power
        P_i_init = required_power(dict_fix['eta_t'], dict_fix['m_a'],
                                  dict_fix['c_r'], dict_fix['C_d'],
                                  dict_fix['A_f'], v_init, a, p_maxn_init)
        
        # engine initial output penalty
        mu_P_init = Mus.mu_P(P_i_init, p_maxn_init)
        
        # engine speed at final vehicle speed
        n_i_fin = engine_speed(v, dict_fix['xi_f'], xi_g, dict_fix['r_d'],
                               dict_fix['s_f'], dict_fix['n_max'])
        
        # engine speed final penalty
        mu_n_fin = Mus.mu_n(n_i_fin, dict_fix['n_max'])
        
        # engine final maximum power at the given engine speed
        p_maxn_fin = Mus.p_maxn(dict_fix['P_max'], n_i_fin, dict_fix['n_max'])

        # engine final instantaneous power
        P_i_fin = required_power(dict_fix['eta_t'], dict_fix['m_a'],
                                 dict_fix['c_r'], dict_fix['C_d'],
                                 dict_fix['A_f'], v, a, p_maxn_fin)

        # engine final output penalty
        mu_P_fin = Mus.mu_P(P_i_fin, p_maxn_fin)

        # energy required to accelerate the vehicle
        e_kin = Energy.e_kin(dict_fix['eta_t'], dict_fix['eta_max'], mu_n_init,
                             mu_n_fin, mu_P_init, mu_P_fin, dict_fix['m_a'],
                             v_init, a, t)

        # energy required to overcome rolling resistance
        e_roll = Energy.e_roll(dict_fix['eta_t'], dict_fix['eta_max'], mu_n_fin,
                               mu_P_fin, dict_fix['m_a'], v, dict_fix['c_r'],a, t)

        # energy required to overcome air resistance
        e_air = Energy.e_air(dict_fix['eta_t'], dict_fix['eta_max'], mu_n_fin,
                             mu_P_fin, v, dict_fix['C_d'], dict_fix['A_f'], a, t)

        # total energy required for accelerated vehicle movement
        e = e_kin + e_roll + e_air
        # fuel consumption
        f_cons = fuel_cons(e, dict_fix['Q_f'], v, P_i_fin, dict_fix['ro_f'])
 
    return(f_cons)
