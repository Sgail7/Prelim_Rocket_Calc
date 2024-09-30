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
    thrust = (EP*2*eff)/(isp*9.8066)
    return thrust

def solar_irradiance(distance):
    return (6.95e8**2/distance**2)*6.4e7

def t_b_prop_mass(burn_time, m_dot):
    return burn_time*m_dot

def EP_to_area(EP, eff, sun_dis):
    area = EP / (solar_irradiance(sun_dis) * eff)
    return area

def area_to_EP(area, eff, sun_dis):
    EP = area * solar_irradiance(sun_dis) * eff
    return EP

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

def elec_burn(m_struct, m_chem_prop, m_elec_prop, isp, eff, panel_eff, panel_area, t=0, pos=0, v=0, dir=1, mars_dist = 6.41e11): #78e9
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
    sun_to_craft = 1.496e11 + pos

    while pos < mars_dist:
        thrust = vary_thrust(area_to_EP(panel_area, panel_eff, sun_to_craft), isp, eff)
        m_dot = mass_flow_rate(thrust, isp)
        v = v + (dir * thrust)/m_tot*dt # Dir is 1 or -1, defines either accel or decel
           
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

def elec_turn(m_struct, m_fuel, marsDist, Thrust, I_sp, v_f):
    pos = 0
    v = 0 #m/s
    t = 0
    dt = 600 #seconds
    dmdt = mass_flow_rate(Thrust, I_sp)

    for dturn in range(1,100): #search over possible values for the d_turn as a percent of the total trip distance
        pos = 0
        v = 0 #m/s
        t = 0
        
        Mtot = m_struct + m_fuel
        while pos < marsDist:
            #update velocity
            if pos < dturn/100*marsDist:
                v = v + (Thrust/Mtot)*dt #accelerate
            else:
                v = v - (Thrust/Mtot)*dt #deaccelerate
            # if v > v_f:
            #     print("fail--didn't slow down enough with turnaround at", dturn, "percent of journey") #stop if Hermes starts to turn around
            #     print("Speed:", v)
                
            Mtot = Mtot - dmdt*dt #update mass
            pos = pos + v*dt #update position
            t = t+dt #update time
            
        if v <= v_f:
            print("success--reached Mars with turnaround at", dturn, "percent of journey")
            break

    print("time to reach Mars:", t/24/3600, "days")
    print("velocity at mars", v, "m/s")

    return(t)