import matplotlib.pyplot as plt
from math import sqrt

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

def t_b_prop_mass(burn_time, m_dot):
    return burn_time*m_dot

def graphing(x, y, title, x_label, y_label):
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

def chem_burn(m_struct, m_ox, m_prop, m_elec_prop, isp, thrust, f_ox_r, t=0, pos=0, v=0, dir=1):
    # Define time step
    dt = 1 #seconds

    # Log Initial Oxidizer and Propellant Mass
    m_ox_i = m_ox
    m_prop_i = m_prop

    # Define direction of thrust
    if dir >= 0:
        dir = 1
    elif dir < 0:
        dir = -1

    # Initalize arrays
    v_graph = []
    t_graph = []
    m_graph = []
    ox_graph = []
    prop_graph = []

    # Since Thrust is 100% right now, mass flow is assumed constant
    m_dot = mass_flow_rate(thrust, isp)

    if m_ox + m_prop < mass_flow_rate(thrust, isp):
        ratio = (m_ox + m_prop) / mass_flow_rate(thrust, isp)
        dt = ratio*dt

        m_tot = m_prop + m_ox + m_struct + m_elec_prop
        v = v + (dir * thrust)/m_tot*dt # Dir is 1 or -1, defines either accel or decel

        m_tot = m_tot - m_dot*dt #update mass
        m_ox = m_ox - m_dot*dt*(1 / (f_ox_r + 1))
        m_prop = m_prop - m_dot*dt*(f_ox_r / (f_ox_r + 1))
        pos = pos + v*dt #update position
        t = t+dt #update time
        v_graph.append(v)
        t_graph.append(t)
        m_graph.append(m_tot)
        ox_graph.append(m_ox)
        prop_graph.append(m_prop)
        
    else:
        while m_ox > 0.1 and m_prop > 0.1:
            m_tot = m_prop + m_ox + m_struct + m_elec_prop
            v = v + (dir * thrust)/m_tot*dt # Dir is 1 or -1, defines either accel or decel

            m_tot = m_tot - m_dot*dt #update mass
            m_ox = m_ox - m_dot*dt*(1 / (f_ox_r + 1))
            m_prop = m_prop - m_dot*dt*(f_ox_r / (f_ox_r + 1))
            pos = pos + v*dt #update position
            t = t+dt #update time
            v_graph.append(v)
            t_graph.append(t)
            m_graph.append(m_tot)
            ox_graph.append(m_ox)
            prop_graph.append(m_prop)

    return(t, pos, v, m_ox, m_prop, m_ox_i, m_prop_i, v_graph, t_graph, m_graph, ox_graph, prop_graph)

def elec_burn(m_struct, m_chem_prop, m_elec_prop, isp, thrust, t=0, pos=0, v=0, dir=1, mars_dist = 78e9):
    # Define time step
    dt = 3600 #seconds

    # Define direction of thrust
    if dir >= 0:
        dir = 1
    elif dir < 0:
        dir = -1

    # Initalize arrays
    v_graph = []
    t_graph = []
    m_graph = []
    thrust_graph = []

    m_tot = m_struct + m_chem_prop + m_elec_prop
    sun_to_craft = 1.5e11 + pos
    isp = 2600
    eff = 0.63

    while pos < mars_dist:
        #update velocity
        thrust = vary_thrust(solar_irradiance(sun_to_craft)*3500*0.4, isp, eff) # Was 3500
        m_dot = mass_flow_rate(thrust, isp)
        v = v + thrust/m_tot*dt #accelerate
           
        m_tot = m_tot - m_dot*dt #update mass
        m_elec_prop = m_elec_prop - m_dot*dt
        pos = pos + v*dt #update position
        sun_to_craft = 1.5e11 + pos
        t = t+dt #update time
        v_graph.append(v)
        t_graph.append(t)
        m_graph.append(m_tot)
        thrust_graph.append(thrust)
    
    return(v_graph, t_graph, m_graph, thrust_graph, v, t, pos, m_tot, m_elec_prop)

m_struct = 110e3 + 178518.4635 # Second number is fuel for last burn
m_elec_prop = 60e3
isp = 311
thrust = 981000 * 3
f_ox_r = 2.5
mass_ox = t_b_prop_mass(185, mass_flow_rate(thrust, isp)) * (1/(1 + f_ox_r))
mass_prop = mass_ox * f_ox_r
direction = -1
t, pos, v, m_ox, m_prop, m_ox_i, m_prop_i, v_graph, t_graph, m_graph, ox_graph, prop_graph = chem_burn(m_struct, mass_ox, mass_prop, m_elec_prop, isp, thrust, f_ox_r)


print("Total Burn Time:", t, "seconds")
print("Total Distance:", pos, "meters")
print("Final Velocity:", v, "m/s")
print("Initial Oxidizer Mass:", m_ox_i, "kg")
print("Initial Propellant Mass:", m_prop_i, "kg")
print("Final Oxidizer Mass:", m_ox, "kg")
print("Final Propellant Mass:", m_prop, "kg")
print("Mass Flow Rate:", mass_flow_rate(thrust, isp), "kg/s")
print("Overflow Mass Chemical:", -(m_ox + m_prop), "kg")

m_elec_prop = 0
m_struct = 110e3

t_1, pos_1, v_1, m_ox_1, m_prop_1, m_ox_i_1, m_prop_i_1, v_graph_1, t_graph_1, m_graph_1, ox_graph_1, prop_graph_1 = chem_burn(m_struct, mass_ox, mass_prop, m_elec_prop, isp, thrust, f_ox_r, t, pos, v, direction)

m_elec_prop = 60e3
v_graph_2, t_graph_2, m_graph_2, thrust_graph_2, v_2, t_2, pos_2, m_tot_2, m_elec_prop_2 = elec_burn(m_struct, m_ox_i + m_prop_i, m_elec_prop, isp, thrust, t, pos_1, v)

t_graph_1_adjusted = [t + t_2 for t in t_graph_1]
v_graph_1_adjusted = [v + v_2 for v in v_graph_1]
v_graph_1_adjusted = [v + v_1 for v in v_graph_1_adjusted]

graphing(t_graph, v_graph, "Delta V vs Time", 'Time (secs)', 'Velocity (m/s)')
graphing(t_graph_2, v_graph_2, "Delta V vs Time", 'Time (secs)', 'Velocity (m/s)')
graphing(t_graph_1_adjusted, v_graph_1_adjusted, "Delta V vs Time", 'Time (secs)', 'Velocity (m/s)')
plt.show()
graphing(t_graph, m_graph, "Mass vs Time", 'Time (secs)', 'Mass (kg)')
graphing(t_graph_2, m_graph_2, "Mass vs Time", 'Time (secs)', 'Mass (kg)')
graphing(t_graph_1_adjusted, m_graph_1, "Mass vs Time", 'Time (secs)', 'Mass (kg)')
plt.show()