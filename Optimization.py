import matplotlib.pyplot as plt
from math import sqrt, exp
import numpy as np

# Function to calculate the time to reach Mars using basic physics
def f_ma_calc(mars_dist, accel):
    return 2 * sqrt(mars_dist / accel)

# Convert seconds to days
def secs_to_days(secs):
    return secs / 3600 / 24

# Calculate the mass flow rate based on thrust and specific impulse
def mass_flow_rate(thrust, isp):
    return thrust / (isp * 9.8066)

# Calculate the mass of propellant used based on thrust, specific impulse, and burn time
def mass_propellant(thrust, isp, t_burn):
    return mass_flow_rate(thrust, isp) * t_burn

# Calculate fuel cost based on propellant mass and cost per kg
def fuel_cost(mass_propellent, cost_per_kg):
    return mass_propellent * cost_per_kg

# Vary thrust based on electric power (EP), specific impulse (isp), and efficiency
def vary_thrust(EP, isp, eff):
    return (EP * 2 * eff) / (isp * 9.8066)

# Calculate solar irradiance based on distance from the sun
def solar_irradiance(distance):
    return (6.95e8**2 / distance**2) * 6.4e7

def graphing(x, y, title, x_label, y_label):
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

# Setup initial conditions
m_struct = np.linspace(110e3, 210e3, 500) 
v0 = np.linspace(0, 6e3, 500) 
transfer_periods = np.zeros((len(m_struct),), dtype=np.double)
propellant_masses = np.zeros((len(m_struct),), dtype=np.double)
mars_velocities = np.zeros((len(m_struct),), dtype=np.double)
mars_thrusts = np.zeros((len(m_struct),), dtype=np.double)

m_fuel_guess = 1000  # Fuel mass in kg (initially assumed)
mars_dist = 78e9  # Distance to Mars in meters (78 million km)
isp = 2600  # Specific impulse in seconds

# Iterate over each structural mass configuration
for ii in range(len(m_struct)):  
    pos = 0  # initial position
    t = 0  # initial time
    dt = 3600  # time step (1 hour)
    Mtot = m_struct[ii] + m_fuel_guess  # total initial mass (scalar for each iteration)
    sun_to_craft = 1.5e11 + pos  # initial distance from Sun (1 AU = 1.5e11 meters)
    eff = 0.63  # engine efficiency
    
    # Iterative convergence for burn time and propellant mass
    burn_time_converged = False
    tolerance = 1e-3
    max_iterations = 1000
    iteration = 0
    new_burn_time_guess = np.zeros(1000, dtype=np.double)
    
    while not burn_time_converged and iteration < max_iterations:
        propellant_used = 0  # reset propellant mass for each iteration
        pos = 0  # reset position for each iteration (scalar)
        v = 6000  # reset velocity for each iteration (scalar) [Using a constant value because the linspace doesn't work rn]
        Mtot = m_struct[ii] + m_fuel_guess  # reset mass for each iteration (scalar)
        t = 0  # reset time
        total_burn_time = 0  # reset burn time
        
        # Simulate spacecraft travel to Mars
        while pos < mars_dist:  # Ensure pos is a scalar
            solar_power = solar_irradiance(sun_to_craft) * 3500 * 0.4  # Example power scaling
            thrust = vary_thrust(solar_power, isp, eff)
            dmdt = mass_flow_rate(thrust, isp)  # mass flow rate (kg/s)
    
            v = v + (thrust / Mtot) * dt  # accelerate (v is a scalar)
            propellant_used += dmdt * dt  # accumulate propellant usage
            Mtot = Mtot - dmdt * dt  # update mass (scalar)
            pos = pos + v * dt  # update position (scalar)
            sun_to_craft = 1.5e11 + pos  # update distance from the Sun (scalar)
            t += dt  # update time
            total_burn_time += dt  # accumulate burn time
    
        # Check convergence of burn time and propellant mass
        new_burn_time_guess[iteration] = total_burn_time
        if iteration > 0 and abs(new_burn_time_guess[iteration] - new_burn_time_guess[iteration - 1]) < tolerance:
            burn_time_converged = True
        else:
            m_fuel_guess = propellant_used 
        iteration += 1
        
    transfer_periods[ii] = total_burn_time 
    propellant_masses[ii] = propellant_used 
    mars_velocities[ii] = v 
    mars_thrusts[ii] = thrust 


# Print results after convergence for the last iteration
print("Time to reach Mars:", total_burn_time / (24 * 3600), "days")
print("Total propellant used:", propellant_used, "kg")
print("Velocity at Mars:", v, "m/s")
print("Thrust at Mars:", thrust, "N")
print("Solar irradiance at Mars:", solar_irradiance(sun_to_craft), "W/m^2")

graphing(mars_velocities, secs_to_days(transfer_periods), "Mars Velocity vs Thrust", "Mars Velocity (m/s)", "Thrust (N)")
graphing(secs_to_days(transfer_periods), m_struct, "Transfer Period vs Structural Mass", "Transfer Period (Days)", "Structural Mass (kg)")
graphing(m_struct, propellant_masses, "Propellant Mass vs Structural Mass", "Structural Mass (kg)", "Propellant Mass (kg)")
graphing(m_struct, mars_velocities, "Mars Velocity vs Structural Mass", "Structural Mass (kg)", "Mars Velocity (m/s)")

propellant_needed = propellant_used 
print("Propellant Needed:", propellant_needed, "kg")
