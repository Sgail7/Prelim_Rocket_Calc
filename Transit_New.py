from one_way_funcs import *
import numpy as np 

#Solar Variables
EP = 2e6
panel_eff = 0.3
panel_area = EP_to_area(EP, panel_eff, 1.496e11)
mars_dist = 225e9

#Chemical Variables for Burn 1
m_struct_c_1 = 110e3
m_elec_prop_guess = 80000 # Was 64.9e3
isp_c_1 = 311
thrust_c_1 = 981000 * 2
f_ox_r = 2.5
mass_ox_c_1 = t_b_prop_mass(185, mass_flow_rate(thrust_c_1, isp_c_1)) * (1/(1 + f_ox_r))
mass_prop_c_1= mass_ox_c_1 * f_ox_r
dir_c_1 = 1

#Electrical Variables for Burn 1
m_struct_e_1 = 110e3
isp_e_1 = 2600
eff_e_1 = 0.63
dir_e_1 = 1
turn_percent_e_1 = 0.315 # 0.315 is pretty perfect (if you go below 0.3, it breaks and I don't know why right now)
m_dist_e_1 = mars_dist * turn_percent_e_1

#Electrical Variables for Burn 2
m_struct_e_2 = 110e3
isp_e_2 = 2600
eff_e_2 = 0.63
dir_e_2 = -1
turn_percent_e_2 = 1 - turn_percent_e_1
m_dist_e_2 = mars_dist * turn_percent_e_2

# Chemical Variables for Burn 2
m_struct_c_2 = 110e3
m_elec_prop_c_2 = 0 # Bc all was burned in the transit
isp_c_2 = 311
thrust_c_2 = 981000 * 2
f_ox_r = 2.5
mass_ox_c_2 = t_b_prop_mass(185, mass_flow_rate(thrust_c_2, isp_c_2)) * (1/(1 + f_ox_r))
mass_prop_c_2 = mass_ox_c_2 * f_ox_r
dir_c_2 = -1

t_2, pos_2, v_2, m_ox_2, m_prop_2, v_graph_2, t_graph_2, m_graph_2, ox_graph_2, prop_graph_2 = chem_burn(m_struct_c_2, mass_ox_c_2, mass_prop_c_2, m_elec_prop_c_2, isp_c_2, thrust_c_2, f_ox_r, 0, 0, 0, dir_c_2)

# Redefine structure mass for burn 1 after knowing second burn fuel mass
m_struct_c_1 = 110e3 + mass_prop_c_2 + mass_ox_c_2

max_iterations = 100
prop_array = np.zeros(max_iterations, dtype=np.double)
guess_array = np.zeros(max_iterations, dtype=np.double)
tolerance = 0.5
iteration = 0  
elec_fuel_converged = False 

while not elec_fuel_converged and iteration < max_iterations: 
    t, pos, v, m_ox, m_prop, v_graph, t_graph, m_graph, ox_graph, prop_graph = chem_burn(m_struct_c_1, mass_ox_c_1, mass_prop_c_1, m_elec_prop_guess, isp_c_1, thrust_c_1, f_ox_r) # Still doesn't account for extra fuel from second burn
    v_graph_1, t_graph_1, m_graph_1, thrust_graph_1, v_1, t_1, pos_1, m_tot_1, m_elec_prop_1 = elec_burn(m_struct_e_1, mass_ox_c_2 + mass_prop_c_2, m_elec_prop_guess, isp_e_1, eff_e_1, panel_eff, panel_area, t, pos, v, dir_e_1, mars_dist - abs(pos_2))
    prop_array[iteration] = m_elec_prop_1 
    guess_array[iteration] = m_elec_prop_guess
    if iteration > 0 and abs(m_elec_prop_1 -  m_elec_prop_guess) < tolerance:
        elec_fuel_converged = True
    else:
        m_elec_prop_guess = m_elec_prop_1
    iteration += 1


v_graph_1, t_graph_1, m_graph_1, thrust_graph_1, v_1, t_1, pos_1, m_tot_1, m_elec_prop_e_1 = elec_burn(m_struct_e_1, mass_ox_c_2 + mass_prop_c_2, m_elec_prop_1, isp_e_1, eff_e_1, panel_eff, panel_area, t, pos, v, dir_e_1, m_dist_e_1 - abs(pos_2))
v_graph_e_2, t_graph_e_2, m_graph_1, thrust_graph_1, v_e_2, t_e_2, pos_e_2, m_tot_1, m_elec_prop_e_1 = elec_burn(m_struct_e_1, mass_ox_c_2 + mass_prop_c_2, m_elec_prop_e_1, isp_e_1, eff_e_2, panel_eff, panel_area, t_1, pos_1, v_1, dir_e_2, mars_dist - abs(pos_2))

t_2, pos_2, v_2, m_ox_2, m_prop_2, v_graph_2, t_graph_2, m_graph_2, ox_graph_2, prop_graph_2 = chem_burn(m_struct_c_2, mass_ox_c_2, mass_prop_c_2, m_elec_prop_c_2, isp_c_2, thrust_c_2, f_ox_r, t_e_2, pos_e_2, v_e_2, dir_c_2)

print("Total Burn Time:", secs_to_days(t_2), "days")
print("Final Velocity:", v_2, "m/s")

t_graph_total = np.concatenate((t_graph, t_graph_1, t_graph_e_2, t_graph_2), axis=None)
v_graph_total = np.concatenate((v_graph, v_graph_1, v_graph_e_2, v_graph_2), axis=None)
graphing(secs_to_days(t_graph_total), v_graph_total, "Delta V vs Time (Chemical + Ion Thrusters)", 'Time (secs)', 'Velocity (m/s)')
plt.show()

acceleration = np.diff(v_graph_total) / np.diff(t_graph_total)
t_acceleration = t_graph_total[:-1]  # Time points for acceleration are one less than for velocity

graphing(secs_to_days(t_acceleration), acceleration, "Acceleration vs Time (Chemical + Ion Thrusters)", 'Time (secs)', 'Acceleration (m/s^2)')
plt.show()
