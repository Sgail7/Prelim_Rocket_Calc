from one_way_funcs import *
import numpy as np 

#Solar Variables
EP = 2e6
panel_eff = 0.3
panel_area = EP_to_area(EP, panel_eff, 1.496e11)
mars_dist = 225e9

#Chemical Variables for Burn 1
m_struct_c_1 = 110e3
isp_c_1 = 451.3
thrust_c_1 = 2277489.47 * 2
f_ox_r = 6
mass_ox_c_1 = t_b_prop_mass(510, mass_flow_rate(thrust_c_1, isp_c_1)) * (1/(1 + f_ox_r))
mass_prop_c_1= mass_ox_c_1 * f_ox_r
dir_c_1 = 1

#Electrical Variables for Burn 1
m_struct_e_1 = 110e3
m_elec_prop_1_guess = 80000
isp_e_1 = 2600
eff_e_1 = 0.63
dir_e_1 = 1
turn_percent_e_1 = 0.57
m_dist_e_1 = mars_dist * turn_percent_e_1

#Electrical Variables for Burn 2
m_struct_e_2 = 110e3
m_elec_prop_2_guess = 80000
isp_e_2 = 2600
eff_e_2 = 0.63
dir_e_2 = -1
turn_percent_e_2 = 1 - turn_percent_e_1
m_dist_e_2 = mars_dist * turn_percent_e_2

# Chemical Variables for Burn 2
m_struct_c_2 = 110e3
m_elec_prop_c_2 = 0 # Bc all was burned in the transit
isp_c_2 = 451.3
thrust_c_2 = 2277489.47 * 1
f_ox_r = 6
mass_ox_c_2 = t_b_prop_mass(559, mass_flow_rate(thrust_c_2, isp_c_2)) * (1/(1 + f_ox_r))
mass_prop_c_2 = mass_ox_c_2 * f_ox_r
dir_c_2 = -1

t_2, pos_2, v_2, m_ox_2, m_prop_2, v_graph_2, t_graph_2, m_graph_2, ox_graph_2, prop_graph_2 = chem_burn(m_struct_c_2, mass_ox_c_2, mass_prop_c_2, m_elec_prop_c_2, isp_c_2, thrust_c_2, f_ox_r, 0, 0, 0, dir_c_2)

# Redefine structure mass for burn 1 after knowing second burn fuel mass
m_struct_c_1 = 110e3 + mass_prop_c_2 + mass_ox_c_2

max_iterations = 100
prop_array_e_1 = np.zeros(max_iterations, dtype=np.double)
guess_array_e_1 = np.zeros(max_iterations, dtype=np.double)
prop_array_e_2 = np.zeros(max_iterations, dtype=np.double)
guess_array_e_2 = np.zeros(max_iterations, dtype=np.double)
tolerance = .5
iteration = 0  
elec_fuel_converged_1 = False
elec_fuel_converged_2 = False

while not elec_fuel_converged_1 and not elec_fuel_converged_2 and iteration < max_iterations: 
    t, pos, v, m_ox, m_prop, v_graph, t_graph, m_graph, ox_graph, prop_graph = chem_burn(m_struct_c_1, mass_ox_c_1, mass_prop_c_1, m_elec_prop_1_guess + m_elec_prop_2_guess, isp_c_1, thrust_c_1, f_ox_r)
    v_graph_e_1, t_graph_e_1, m_graph_e_1, thrust_graph_e_1, v_e_1, t_e_1, pos_e_1, m_tot_e_1, m_elec_prop_e_1 = elec_burn(m_struct_e_1, mass_ox_c_2 + mass_prop_c_2, m_elec_prop_1_guess + m_elec_prop_2_guess, isp_e_1, eff_e_1, panel_eff, panel_area, t, pos, v, dir_e_1, m_dist_e_1 - abs(pos_2))
    v_graph_e_2, t_graph_e_2, m_graph_e_2, thrust_graph_e_2, v_e_2, t_e_2, pos_e_2, m_tot_e_2, m_elec_prop_e_2 = elec_burn(m_struct_e_2, mass_ox_c_2 + mass_prop_c_2, m_elec_prop_2_guess, isp_e_2, eff_e_2, panel_eff, panel_area, t_e_1, pos_e_1, v_e_1, dir_e_2, mars_dist - abs(pos_2))
    # v_graph_1, t_graph_1, m_graph_1, thrust_graph_1, v_1, t_1, pos_1, m_tot_1, m_elec_prop_1 = elec_burn(m_struct_e_1, mass_ox_c_2 + mass_prop_c_2, m_elec_prop_guess, isp_e_1, eff_e_1, panel_eff, panel_area, t, pos, v, dir_e_1, mars_dist - abs(pos_2))
    prop_array_e_1[iteration] = m_elec_prop_e_1 
    guess_array_e_1[iteration] = m_elec_prop_1_guess
    prop_array_e_2[iteration] = m_elec_prop_e_2
    guess_array_e_2[iteration] = m_elec_prop_2_guess
    if iteration > 0 and abs(m_elec_prop_e_1 - m_elec_prop_1_guess) < tolerance:
        elec_fuel_converged_1 = True
    else:
        m_elec_prop_1_guess = m_elec_prop_e_1
    
    if iteration > 0 and abs(m_elec_prop_e_2 - m_elec_prop_2_guess) < tolerance:
        elec_fuel_converged_2 = True
    else:
        m_elec_prop_2_guess = m_elec_prop_e_2
    
    iteration += 1

print("Iteration:", iteration)
print("Propellant Array for Burn 1:", prop_array_e_1[0:iteration])
print("Guess Array for Burn 1:", guess_array_e_1[0:iteration])
print("Propellant Array for Burn 2:", prop_array_e_2[0:iteration])
print("Guess Array for Burn 2:", guess_array_e_2[0:iteration])
print("Convergence Status for Burn 1:", elec_fuel_converged_1)
print("Convergence Status for Burn 2:", elec_fuel_converged_2)

t_2, pos_2, v_2, m_ox_2, m_prop_2, v_graph_2, t_graph_2, m_graph_2, ox_graph_2, prop_graph_2 = chem_burn(m_struct_c_2, mass_ox_c_2, mass_prop_c_2, m_elec_prop_c_2, isp_c_2, thrust_c_2, f_ox_r, t_e_2, pos_e_2, v_e_2, dir_c_2)

print("Total Burn Time:", secs_to_days(t_2), "days")
print("Final Velocity:", v_2, "m/s")
print("Percent of Distance Completed:", pos_2 / mars_dist * 100, "%")

t_graph_total = np.concatenate((t_graph, t_graph_e_1, t_graph_e_2, t_graph_2), axis=None)
v_graph_total = np.concatenate((v_graph, v_graph_e_1, v_graph_e_2, v_graph_2), axis=None)
m_graph_total = np.concatenate((m_graph, m_graph_e_1, m_graph_e_2, m_graph_2), axis=None)

graphing(secs_to_days(t_graph_total), v_graph_total, "Delta V vs Time (Chemical + Ion Thrusters)", 'Time (secs)', 'Velocity (m/s)')
plt.show()

acceleration = np.diff(v_graph_total) / np.diff(t_graph_total)
t_acceleration = t_graph_total[:-1]  # Time points for acceleration are one less than for velocity

graphing(secs_to_days(t_acceleration), acceleration, "Acceleration vs Time (Chemical + Ion Thrusters)", 'Time (secs)', 'Acceleration (m/s^2)')
plt.show()

graphing(secs_to_days(t_graph_total), m_graph_total, "Mass vs Time (Chemical + Ion Thrusters)", 'Time (secs)', 'Mass (kg)')
plt.show()
