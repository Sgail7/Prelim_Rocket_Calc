from one_way_funcs import *
from matplotlib import pyplot as plt

m_struct = 110e3
m_fuel = 60e3
mars_dist = 6.41e11
thrust = 110
isp = 2600
v_f = 1365

t = elec_turn(m_struct, m_fuel, mars_dist, thrust, isp, v_f)

# #### Variables
# m_Hermes = 110e3 #kg
# m_Fuel = 126e3 #kg
# marsDist = 225E9 #m
# a_Hermes = 0.002

# Thrust = a_Hermes*(m_Fuel+m_Hermes)

# I_sp = 5000
# dmdt=Thrust/9.8/I_sp

# #### Turn around
# pos = 0
# v = 0 #m/s
# t = 0
# dt = 600 #seconds

# Mtot = m_Hermes + m_Fuel

# for dturn in range(55,100): #search over possible values for the d_turn as a percent of the total trip distance
#     pos = 0
#     v = 0 #m/s
#     t = 0
    
#     Mtot = m_Hermes + m_Fuel
#     while pos < marsDist:
#         #update velocity
#         if pos < dturn/100*marsDist:
#             v = v + Thrust/Mtot*dt #accelerate
#         else:
#             v = v - Thrust/Mtot*dt #deaccelerate
#         if v < 0:
#             print("fail--didn't reach Mars with turnaround at", dturn, "percent of journey") #stop if Hermes starts to turn around
#             break
               
#         Mtot = Mtot - dmdt*dt #update mass
#         pos = pos + v*dt #update position
#         t = t+dt #update time
        
#     if pos > marsDist:
#         print("success--reached Mars with turnaround at", dturn, "percent of journey")
#         break

# print("time to reach Mars:", t/24/3600, "days")
# print("velocity at mars", v, "m/s")

# ### Makea da plots
# RHermes_v=[]
# RHermes_t=[]

# pos = 0
# v = 0
# t = 0
# Mtot = m_Hermes + m_Fuel
# while pos < marsDist:
#     if pos < .593*marsDist:
#          v = v + Thrust/Mtot*dt
#     else:
#          v = v - Thrust/Mtot*dt
#     if v < 0:            
#         break
#     Mtot = Mtot - dmdt*dt
#     pos = pos + v*dt
#     t = t+dt     
#     RHermes_v.append(v)
#     RHermes_t.append(t/3600/24)
#     if pos > marsDist: 
#         break

# print("time to reach Mars:", t/24/3600, "days")
# print("velocity at mars", v, "m/s")
# print("final mass", Mtot, "kg")

# plt.plot(RHermes_t,RHermes_v)
# plt.title('Plot of Hermes Velocity as a Function of Time')
# plt.xlabel('Time (days)')
# plt.ylabel('Velocity (m/s)')
# plt.show()