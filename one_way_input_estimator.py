from one_way_funcs import *

m_struct = 110e3 + 178518.4635 # Second number is fuel for last burn
m_elec_prop = 80.97e3 # Was 64.9e3
isp = 311
thrust = 981000 * 2
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
print("Mass Flow Rate:", mass_flow_rate(thrust, isp), "kg/s")

graphing(t_graph, v_graph, "Delta V vs Time", 'Time (secs)', 'Velocity (m/s)')
plt.show()
graphing(t_graph, m_graph, "Mass vs Time", 'Time (secs)', 'Mass (kg)')
plt.show()


m_struct = 110e3
isp = 2600
eff = 0.63
panel_eff = 0.3
EP = 3e6
panel_area = EP_to_area(EP, panel_eff, 1.496e11)

v_graph_1, t_graph_1, m_graph_1, thrust_graph_1, v_1, t_1, pos_1, m_tot_1, m_elec_prop_1 = elec_burn(m_struct, m_ox_i + m_prop_i, m_elec_prop, isp, eff, panel_eff, panel_area)

print("Total Burn Time:", secs_to_days(t_1), "days")
print("Final Velocity:", v_1, "m/s")
print("Fuel Used:", m_elec_prop - m_elec_prop_1, "kg") # Guess minus actual number, if goes over, actual is bigger, if goes under, actual is smaller
print("Fuel Guess vs Actual:", abs(m_elec_prop_1), "kg")

graphing(t_graph_1, v_graph_1, "Delta V vs Time (Ion Thrusters)", 'Time (secs)', 'Velocity (m/s)')
plt.show()
graphing(t_graph_1, m_graph_1, "Mass vs Time (Ion Thrusters)", 'Time (secs)', 'Mass (kg)')
plt.show()
graphing(t_graph_1, thrust_graph_1, "Thrust vs Time (Ion Thrusters)", 'Time (secs)', 'Thrust (N)')
plt.show()

m_struct = 110e3
m_elec_prop = m_elec_prop - m_elec_prop_1
isp = 311
thrust = 981000 * 2
f_ox_r = 2.5
mass_ox = t_b_prop_mass(185, mass_flow_rate(thrust, isp)) * (1/(1 + f_ox_r))
mass_prop = mass_ox * f_ox_r
direction = -1

t_2, pos_2, v_2, m_ox_2, m_prop_2, m_ox_i_2, m_prop_i_2, v_graph_2, t_graph_2, m_graph_2, ox_graph_2, prop_graph_2 = chem_burn(m_struct, mass_ox, mass_prop, m_elec_prop, isp, thrust, f_ox_r, 0, 0, 0, direction)

print("Total Burn Time:", t_2, "seconds")
print("Total Distance:", pos_2, "meters")
print("Final Velocity:", v_2, "m/s")
print("Initial Oxidizer Mass:", m_ox_i_2, "kg")
print("Initial Propellant Mass:", m_prop_i_2, "kg")
print("Mass Flow Rate:", mass_flow_rate(thrust, isp), "kg/s")

graphing(t_graph_2, v_graph_2, "Delta V vs Time", 'Time (secs)', 'Velocity (m/s)')
plt.show()
graphing(t_graph_2, m_graph_2, "Mass vs Time", 'Time (secs)', 'Mass (kg)')
plt.show()