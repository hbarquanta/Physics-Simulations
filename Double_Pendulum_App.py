import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import ipywidgets as widgets
from IPython.display import display

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Times New Roman'
plt.rcParams['font.size'] = 14
plt.rcParams['axes.linewidth'] = 1
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 5
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.size'] = 5   
plt.rcParams['ytick.major.size'] = 5   
plt.rcParams['xtick.major.width'] = 1   
plt.rcParams['ytick.major.width'] = 1   
plt.rcParams['legend.fontsize'] = 14
# Constants
g = 9.81  # Acceleration due to gravity (m/s^2)

def equations(t, y, L1, L2, m1, m2):
    theta1, z1, theta2, z2 = y
    c, s = np.cos(theta1 - theta2), np.sin(theta1 - theta2)
    theta1dot = z1
    z1dot = (m2 * g * np.sin(theta2) * c - m2 * s * (L1 * z1**2 * c + L2 * z2**2) -
             (m1 + m2) * g * np.sin(theta1)) / L1 / (m1 + m2 * s**2)
    theta2dot = z2
    z2dot = ((m1 + m2) * (L1 * z1**2 * s - g * np.sin(theta2) + g * np.sin(theta1) * c) +
             m2 * L2 * z2**2 * s * c) / L2 / (m1 + m2 * s**2)
    return [theta1dot, z1dot, theta2dot, z2dot]

def simulate_double_pendulum(y0, t_span, t_eval, L1, L2, m1, m2):
    solution = solve_ivp(equations, t_span, y0, args=(L1, L2, m1, m2), t_eval=t_eval)
    return solution

def plot_double_pendulum(solution, L1, L2):
    theta1, theta2 = solution.y[0], solution.y[2]
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    x2 = x1 + L2 * np.sin(theta2)
    y2 = y1 - L2 * np.cos(theta2)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x1, y1, 'r-', label='Pendulum 1', lw=2)
    plt.plot(x2, y2, 'b-', label='Pendulum 2', lw=2)
    plt.legend()
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Double Pendulum Simulation')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

def interactive_double_pendulum(theta1_initial, theta2_initial, L1, L2, m1, m2):
    y0 = [theta1_initial, 0, theta2_initial, 0]
    t_span = [0, 10]
    t_eval = np.linspace(0, 10, 1000)
    
    solution = simulate_double_pendulum(y0, t_span, t_eval, L1, L2, m1, m2)
    plot_double_pendulum(solution, L1, L2)

def reset_values(b):
    theta1_slider.value = np.pi / 2
    theta2_slider.value = np.pi / 2
    L1_input.value = 1.0
    L2_input.value = 1.0
    m1_input.value = 1.0
    m2_input.value = 1.0

    
reset_button = widgets.Button(description='Reset')
theta1_slider = widgets.FloatSlider(value=np.pi / 2, min=0, max=2 * np.pi, step=0.01, description='Theta1:')
theta2_slider = widgets.FloatSlider(value=np.pi / 2, min=0, max=2 * np.pi, step=0.01, description='Theta2:')
L1_input = widgets.FloatText(value=1.0, description='Length 1:')
L2_input = widgets.FloatText(value=1.0, description='Length 2:')
m1_input = widgets.FloatText(value=1.0, description='Mass 1:')
m2_input = widgets.FloatText(value=1.0, description='Mass 2:')

reset_button.on_click(reset_values)

interactive_plot = widgets.interactive(interactive_double_pendulum, 
                                       theta1_initial=theta1_slider, 
                                       theta2_initial=theta2_slider, 
                                       L1=L1_input, L2=L2_input, 
                                       m1=m1_input, m2=m2_input)

display(interactive_plot, reset_button)
