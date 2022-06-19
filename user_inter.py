"""
Within this script the user interaction is going to take place.
Just for now data needed to a full employment of the calculation engine
is introduced here together with a complete secquence o functions calls.
Usefull information is going to be displayed in the terminal.
In order to make use of simfc.py (SIMulate Fuel Consumption) and its
functions the just mentioned file must be treated as a python module
and imported as such.
For now only fuel consumption at constant speed is simulated.
"""

import simfc as sfc

"""
Values required are provided as following, contained in one of three
categories: given by Kevin, available (found in tables on the internet,
such as gasoline calorific value) and contrived (for instance, gearbox
ratio).
"""

# vehicle speed (aprox 130 km/h) (contrived)
v_a = 36

# transmission finale ratio (given)
xi_f = 4.18

# gearbox ratio (cruising speed) (contrived)
xi_g = 0.92

# slip factor (given)
s_f = 1.05

# wheel rolling radius (given)
r_d = 0.32

# engine maximum speed (given)
n_max = 7000

# engine maximum output/power (given)
P_max = 213

# engine type (given)
type = 'SIE'

# transmission overall efficiency (given)
eta_t = 0.91

# engine peak efficiency (contrived)
eta_max = 0.36

# vehicle mass (contrived)
m_a = 1250

# rolling resistance coefficient (given)
c_r = 0.009

# coefficient of aerodynamic drag (wind coefficient) (given)
C_d = 0.26

# vehicle frontal area (given)
A_f = 2.16

# distance (100 km) (contrived)
S = 200000

# air density (available)
ro_a = 1.225

# acceleration at constant speed (obvious)
a = 0

# gasoline calorific value (available)
Q_f = 34200000

# gasoline density (available)
ro_f = 0.74


"""
Functions calls and results display
"""

# engine speed
n_i = sfc.engine_speed(v_a, xi_f, xi_g, r_d, s_f)
print("Engine speed is: ", n_i, "rpm")

# mu_n
mu_n = sfc.mu_n(n_i, n_max)
print("mu_n is: ", mu_n)

# engine maximum power at the given engine speed
p_maxn = sfc.p_maxn(P_max, n_i, n_max, type)
print("Engine maximum power at the given speed is: ", p_maxn, "kW")

# engine instantaneous power
P_i = sfc.required_power(eta_t, m_a, c_r, C_d, A_f, v_a, a, ro_a)
print("Engine instantaneous power is: ", P_i, "kW")

# mu_P calculation
mu_P = sfc.mu_P(P_i, p_maxn, type)
print("mu_P is: ", mu_P)

# energy required to overcome resistances at the given constant speed
E_const = sfc.e_const(eta_t, eta_max, mu_n, mu_P, m_a, c_r, C_d, A_f, v_a, S,
ro_a)
print("Energy required to move the vehicle at 130 km/h is: ", E_const, "J/100 km")

# fuel consumption
fuel_cons = sfc.fuel_cons(E_const, Q_f, v_a, P_i, ro_f)
print("Fuel consumed per 100 km is: ", fuel_cons[0], "liters")
print("Fuel consumed per hour is: ", fuel_cons[1], "kg/hour")
print("Specific fuel consumption is: ", fuel_cons[2], "kg/kWh")
