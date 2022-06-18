"""
Within this script the SFC script call is going to take place.
A total number of 19 variables are needed to be passed as
arguments to the classes and functions within SFC simulator.
Out of this total number of variables 15 are 'fixed', i.e., are
not changing with the conditions at agent/drive train level.
In order to simplify the SFC script invocation the 'fixed'
variables are to be passed as a list build only once.
As for the other mutable variables these must be passed
individually. Please read the explanatory document carefully to
understand which script are belonging to either category and the
order of arguments.
"""

import simfc3 as sfc

#the 'fixed' vars list
fixs = []

# vehicle speed 
v_init = 38

# movement duration in seconds
t = 20

# transmission finale ratio (fixed)
xi_f = 4.18

fixs.append(xi_f)

# gearbox ratio (cruising speed)
xi_g = 0.94

# slip factor (fixed)
s_f = 1.05

fixs.append(s_f)

# wheel rolling radius (fixed)
r_d = 0.32

fixs.append(r_d)

# engine maximum speed (fixed)
n_max = 6200

fixs.append(n_max)

# engine maximum output/power (fixed)
P_max = 120

fixs.append(P_max)

# engine type (fixed)
type = 'SIE'

fixs.append(type)

# transmission overall efficiency (fixed)
eta_t = 0.91

fixs.append(eta_t)

# engine peak efficiency (fixed)
eta_max = 0.34

fixs.append(eta_max)

# vehicle mass (fixed)
m_a = 1250

fixs.append(m_a)

# rolling resistance coefficient (fixed)
c_r = 0.009

fixs.append(c_r)

# coefficient of aerodynamic drag (wind coefficient) (fixed)
C_d = 0.26

fixs.append(C_d)

# vehicle frontal area (fixed)
A_f = 2.16

fixs.append(A_f)

# air density (fixed)
ro_a = 1.225

fixs.append(ro_a)

# acceleration
a = 0.6  

# gasoline calorific value (fixed)
Q_f = 34200000

fixs.append(Q_f)

# gasoline density (fixed)
ro_f = 0.74

fixs.append(ro_f)

if len(fixs) != 15:
    print("The total number of 'fixed' variables is incorrect!\n"
           "There must be 15 'fixed' variables, you collected: ",len(fixs))
    exit()

"""
SFC simulator call and results return
"""
# specific fuel consumption variable

sfc = sfc.simfc_call(fixs, v_init, xi_g, a, t)
print("The 100 km fuel consumption is: ", sfc[0], "l/100 km")
print("The hourly fuel consumption is: ", sfc[1], "l/h")
print("The specific fuel consumption is: ",sfc[2], "kg/kWh")
