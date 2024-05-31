import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import streamlit as st
from matplotlib.animation import FuncAnimation, PillowWriter
from IPython.display import HTML

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
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x1, y1, 'r-', label='Pendulum 1', lw=2)
    ax.plot(x2, y2, 'b-', label='Pendulum 2', lw=2)
    ax.scatter(x1, y1, c='r', s=50, label='Mass 1')
    ax.scatter(x2, y2, c='b', s=50, label='Mass 2')
    ax.legend()
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_title('Double Pendulum Simulation')
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)

def animate_double_pendulum(solution, L1, L2):
    theta1, theta2 = solution.y[0], solution.y[2]
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    x2 = x1 + L2 * np.sin(theta2)
    y2 = y1 - L2 * np.cos(theta2)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.grid(True, linestyle='--', alpha=0.7)
    line, = ax.plot([], [], 'o-', lw=2, color='black')
    trace1, = ax.plot([], [], 'r-', lw=1, alpha=0.5)
    trace2, = ax.plot([], [], 'b-', lw=1, alpha=0.5)
    
    def init():
        line.set_data([], [])
        trace1.set_data([], [])
        trace2.set_data([], [])
        return line, trace1, trace2
    
    def update(frame):
        thisx = [0, x1[frame], x2[frame]]
        thisy = [0, y1[frame], y2[frame]]
        line.set_data(thisx, thisy)
        trace1.set_data(x1[:frame], y1[:frame])
        trace2.set_data(x2[:frame], y2[:frame])
        return line, trace1, trace2
    
    ani = FuncAnimation(fig, update, frames=range(len(x1)), init_func=init, blit=True, interval=20)
    return ani

# Streamlit App
st.title('Double Pendulum Simulation')

theta1_initial = st.slider('Theta1 Initial (radians)', 0.0, 2 * np.pi, np.pi / 2)
theta2_initial = st.slider('Theta2 Initial (radians)', 0.0, 2 * np.pi, np.pi / 2)
L1 = st.number_input('Length 1 (m)', min_value=0.1, value=1.0, step=0.1)
L2 = st.number_input('Length 2 (m)', min_value=0.1, value=1.0, step=0.1)
m1 = st.number_input('Mass 1 (kg)', min_value=0.1, value=1.0, step=0.1)
m2 = st.number_input('Mass 2 (kg)', min_value=0.1, value=1.0, step=0.1)

if st.button('Simulate'):
    y0 = [theta1_initial, 0, theta2_initial, 0]
    t_span = [0, 10]
    t_eval = np.linspace(0, 10, 1000)
    
    solution = simulate_double_pendulum(y0, t_span, t_eval, L1, L2, m1, m2)
    plot_double_pendulum(solution, L1, L2)
    ani = animate_double_pendulum(solution, L1, L2)
    ani_html = ani.to_jshtml()
    st.components.v1.html(ani_html, height=700)
