from one_way_funcs import *

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
isp = 2600
eff = 0.63
panel_eff = 0.3
panel_area = EP_to_area(2e6, panel_eff, 1.496e11)

v_graph_2, t_graph_2, m_graph_2, thrust_graph_2, v_2, t_2, pos_2, m_tot_2, m_elec_prop_2 = elec_burn(m_struct, m_ox_i + m_prop_i, m_elec_prop, isp, eff, panel_eff, panel_area, t, pos_1, v)

# t_graph_1_adjusted = [t + t_2 for t in t_graph_1]
# v_graph_1_adjusted = [v + v_2 for v in v_graph_1]
# v_graph_1_adjusted = [v + v_1 for v in v_graph_1_adjusted]

graphing(t_graph, v_graph, "Delta V vs Time", 'Time (secs)', 'Velocity (m/s)')
graphing(t_graph_2, v_graph_2, "Delta V vs Time", 'Time (secs)', 'Velocity (m/s)')
graphing(t_graph_1, v_graph_1, "Delta V vs Time", 'Time (secs)', 'Velocity (m/s)')
plt.show()

graphing(t_graph, m_graph, "Mass vs Time", 'Time (secs)', 'Mass (kg)')
graphing(t_graph_2, m_graph_2, "Mass vs Time", 'Time (secs)', 'Mass (kg)')
graphing(t_graph_1, m_graph_1, "Mass vs Time", 'Time (secs)', 'Mass (kg)')
plt.show()