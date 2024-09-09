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
    print("time to reach Mars:", t/24/3600, "days")
    print("velocity at mars", v, "m/s")
    return(t)

def vary_mass_one_way(m_struct, m_fuel, mars_dist, isp):
    pos = 0
    v = 0 #m/s
    t = 0
    dt = 3600 # time step (seconds)

        
    Mtot = m_struct + m_fuel
    sun_to_craft = 1.5e11 + pos
    isp = 2600
    eff = 0.63

    while pos < mars_dist:
        #update velocity
        thrust = vary_thrust(solar_irradiance(sun_to_craft)*3500*0.4, isp, eff)
        dmdt = mass_flow_rate(thrust, isp)
        v = v + thrust/Mtot*dt #accelerate
           
        Mtot = Mtot - dmdt*dt #update mass
        pos = pos + v*dt #update position
        sun_to_craft = 1.5e11 + pos
        t = t+dt #update time
    print("time to reach Mars:", t/24/3600, "days")
    print("velocity at mars", v, "m/s")
    print("thrust at Mars:", thrust, "N")
    print("solar irradiance at Mars:", solar_irradiance(sun_to_craft), "W/m^2")
    return(t)

#print("Propellent Needed:", mass_propellant(5.4, 2600, vary_mass_one_way(110e3, 126e3, 225e9, 5.4, 2600)), "kg")
#print("Propellent Needed:", mass_propellant(100, 2600, vary_mass(110e3, 0, 225e9, 100, 2600)), "kg")
print("Propellent Needed:", mass_propellant(100, 2600, vary_mass_one_way(110e3, 150e3, 78e9, 2600)), "kg")
#print("Fuel Cost:", fuel_cost(mass_propellant(5.4, 2600, vary_mass(110e3, 126e3, 225e9, 5.4, 2600)), 15000), "USD")
#print("The solar irradiance at earth is", solar_irradiance(1.5e11), "W/m^2")

#thrust = vary_thrust(solar_irradiance(1.5e11)*3500*0.4, 2600, 0.63)
#print("Thrust:", thrust, "N")