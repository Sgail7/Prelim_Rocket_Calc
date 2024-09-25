import matplotlib.pyplot as plt
from math import sqrt

def f_ma_calc(mars_dist, accel):
    # Calculate the time it takes to travel to Mars
    # Assumes a you turn around at the halfway point and decelerate 
    return 2*sqrt(mars_dist/accel)

def secs_to_days(secs):
    return secs/3600/24

def mass_flow_rate(thrust, isp):
    return thrust/(isp*9.8066)

def mass_propellant(thrust, isp, t_burn):
    return mass_flow_rate(thrust, isp)*t_burn

def fuel_cost(mass_propellent, cost_per_kg):
    return mass_propellent*cost_per_kg

def vary_thrust(EP, isp, eff):
    return (EP*2*eff)/(isp*9.8066)

def solar_irradiance(distance):
    return (6.95e8**2/distance**2)*6.4e7

def vary_mass(m_struct, m_fuel, mars_dist, thrust, isp):
    pos = 0
    v = 0 #m/s
    t = 0
    dt = 3600 # time step (seconds)

    for dturn in range(45,100): #search over possible values for the d_turn as a percent of the total trip distance
        pos = 0
        v = 0 #m/s
        t = 0
        
        Mtot = m_struct + m_fuel
        dmdt = mass_flow_rate(thrust, isp)

        while pos < mars_dist:
            #update velocity
            if pos < dturn/100*mars_dist:
                v = v + thrust/Mtot*dt #accelerate
            else:
                v = v - thrust/Mtot*dt #deaccelerate
            if v < 0:
                print("fail--didn't reach Mars with turnaround at", dturn, "percent of journey") #stop if Hermes starts to turn around
                break
            pos = pos + v*dt #update position
            EP = 2000000
            Mtot = Mtot - dmdt*dt #update mass
            t = t+dt #update time
            
        if pos > mars_dist:
            print("success--reached Mars with turnaround at", dturn, "percent of journey")
            break
    print("time to reach Mars:", secs_to_days(t), "days")
    print("velocity at mars", v, "m/s")

    return(t)

def prop_burn_time(burn_time, m_dot):
    return burn_time*m_dot

def vary_mass_one_way(m_struct, m_fuel, mars_dist, isp, t=0, pos=0, v=0):
    v_graph = []
    t_graph = []
    m_graph = []
    thrust_graph = []
    dt = 3600 # time step (seconds)

        
    m_tot = m_struct + m_fuel
    sun_to_craft = 1.5e11 + pos
    isp = 2600
    eff = 0.63

    while pos < mars_dist:
        #update velocity
        thrust = vary_thrust(solar_irradiance(sun_to_craft)*3500*0.4, isp, eff) # Was 3500
        dmdt = mass_flow_rate(thrust, isp)
        v = v + thrust/m_tot*dt #accelerate
           
        m_tot = m_tot - dmdt*dt #update mass
        pos = pos + v*dt #update position
        sun_to_craft = 1.5e11 + pos
        t = t+dt #update time
        v_graph.append(v)
        t_graph.append(t)
        m_graph.append(m_tot)
        thrust_graph.append(thrust)

    #print("time to reach Mars:", t/24/3600, "days")
    #print("velocity at mars", v, "m/s")
    #print("thrust at Mars:", thrust, "N")
    #print("solar irradiance at Mars:", solar_irradiance(sun_to_craft), "W/m^2")
    return(v_graph, t_graph, m_graph, v, t, pos, m_tot, thrust_graph)

def chemical_positive(isp, thrust, m_ox, m_struct, f_ox_r, t=0, pos=0, v=0):
    dt = 1 #Seconds
    m_prop = m_ox * f_ox_r

    v_graph = []
    t_graph = []
    m_graph = []
    ox_graph = []
    prop_graph = []

    while m_ox >= 0 and m_prop >= 0:
        m_tot = m_prop + m_ox + m_struct
        dm_dt = mass_flow_rate(thrust, isp)
        v = v + thrust/m_tot*dt

        m_tot = m_tot - dm_dt*dt #update mass
        m_ox = m_ox - dm_dt*dt*(1 / (f_ox_r + 1))
        m_prop = m_prop - dm_dt*dt*(f_ox_r / (f_ox_r + 1))
        pos = pos + v*dt #update position
        t = t+dt #update time
        v_graph.append(v)
        t_graph.append(t)
        m_graph.append(m_tot)
        ox_graph.append(m_ox)
        prop_graph.append(m_prop)
    
    return(v_graph, t_graph, m_graph, v, t, pos, m_ox, m_prop)

def chemical_negaitive(isp, thrust, m_ox, m_struct, f_ox_r, t=0, pos=0, v=0):
    dt = 1 #Seconds
    m_prop = m_ox * f_ox_r

    v_graph = []
    t_graph = []
    m_graph = []
    ox_graph = []
    prop_graph = []

    while m_ox >= 0 and m_prop >= 0:
        m_tot = m_prop + m_ox + m_struct
        dm_dt = mass_flow_rate(thrust, isp)
        v = v - thrust/m_tot*dt ### THIS MINUS SIGN IS THE ONLY DIFFERENCE BETWEEN THIS FUNCTION AND THE ONE ABOVE
        # MAKE THIS ONE FUNCTION WITH CHEMICAL POSITIVE AND NEGATIVE AS INPUTS
        m_tot = m_tot - dm_dt*dt #update mass
        m_ox = m_ox - dm_dt*dt*(1 / (f_ox_r + 1))
        m_prop = m_prop - dm_dt*dt*(f_ox_r / (f_ox_r + 1))
        pos = pos + v*dt #update position
        t = t+dt #update time
        v_graph.append(v)
        t_graph.append(t)
        m_graph.append(m_tot)
        ox_graph.append(m_ox)
        prop_graph.append(m_prop)

    return(v_graph, t_graph, m_graph, v, t, pos, m_ox, m_prop)

def graphing(x, y, title, x_label, y_label):
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

mass_ox = prop_burn_time(185, mass_flow_rate(981000 * 2, 311)) * (1/3.5)
v_graph_0, t_graph_0, m_graph_0, v_0, t_0, pos_0, m_ox_0, m_prop_0 = chemical_positive(311, 981000 * 2, mass_ox, 120e3 + 60e3, 2.5)
v_graph_1, t_graph_1, m_graph_1, v_1, t_1, pos_1, m_tot_1, thrust_graph_1 = vary_mass_one_way(110e3, 150e3, 78e9, 2600, t_0, pos_0, v_0)
v_graph_2, t_graph_2, m_graph_2, v_2, t_2, pos_2, m_ox_2, m_prop_2 = chemical_negaitive(311, 981000 * 2, mass_ox, 120e3 + 60e3, 2.5, t_1, pos_1, v_1)

#graphing(t_graph_0, v_graph_0, "Delta V vs Time", 'Time (secs)', 'Velocity (m/s)')
#graphing(t_graph_1, v_graph_1, "Delta V vs Time", 'Time (secs)', 'Velocity (m/s)')
graphing(t_graph_2, v_graph_2, "Delta V vs Time", 'Time (secs)', 'Velocity (m/s)')
plt.show()
graphing(t_graph_0, m_graph_0, "Mass vs Time", 'Time (secs)', 'Mass (kg)')
graphing(t_graph_1, m_graph_1, "Mass vs Time", 'Time (secs)', 'Mass (kg)')
graphing(t_graph_2, m_graph_2, "Mass vs Time", 'Time (secs)', 'Mass (kg)')
plt.show()
print("Total Burn Time:", t_2 / 60, "Minutes")
print("Position after Burn:", pos_2 / 1000, "km")
print("Total Delta V:", v_2, "m/s")
print("Oxidizer Mass Remaining:", m_ox_2, "kg")
print("Propellant Mass Remaining:", m_prop_2, "kg")
print(mass_flow_rate(981000 * 2, 311))
print("Oxidizer Mass Start:", mass_ox, "kg")
print("Propellant Mass Start:", mass_ox * 3.5 * (2.5/3.5), "kg")



# fig, (ax1, ax2, ax3) = plt.subplots(3)
# ax1.plot(t_graph, v_graph)
# ax1.set_title("Velocity vs. Time")
# ax1.set(xlabel="Time (Days)", ylabel="Velocity (m/s)")
# ax3.plot(t_graph, m_graph)
# ax3.set(xlabel="Time (Days)", ylabel="Mass (kg)")
# ax3.set_title("Mass vs. Time")
# ax2.plot(t_graph, thrust_graph)
# ax2.set_title("Thrust vs. Time")
# ax2.set(xlabel="Time (Days)", ylabel="Thrust (N)")
# plt.show()

# print("Total Transit Time:", secs_to_days(t), "Days")
# print("Velocity @ Mars:", v_end, "m/s")
# print("Electric Propellent Mass Required:", 260000 - m_tot, "kg")
# print("Xenon Propellent Cost:", fuel_cost(260000 - m_tot, 5000),"USD")
# print("Krypton Propellent Cost:", fuel_cost(260000 - m_tot, 2100),"USD")
# print(solar_irradiance(1.5e11) * 5500 * 0.4)