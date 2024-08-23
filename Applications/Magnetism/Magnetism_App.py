import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Constants
MU_0 = 4 * np.pi * 1e-7  # Permeability of free space

# Global variables for flipping magnets
flip1 = 1
flip2 = 1

# Initial values for the session state variables
initial_values = {
    "length1": 2.0,
    "width1": 1.0,
    "x_pos1": 0.0,
    "y_pos1": 1.5,
    "length2": 2.0,
    "width2": 1.0,
    "x_pos2": 0.0,
    "y_pos2": -1.5,
    "flip1": 1,
    "flip2": 1
}

# Initialize session state values if they don't exist
for key, value in initial_values.items():
    if key not in st.session_state:
        st.session_state[key] = value
        
# Function to calculate dipole field
def calculate_dipole_field(X, Y, dipole_pos, dipole_moment):
    x0, y0 = dipole_pos
    mx, my = dipole_moment

    Rx = X - x0
    Ry = Y - y0
    R = np.sqrt(Rx**2 + Ry**2)

    # Avoid division by zero at the location of the dipole
    R[R == 0] = np.inf

    Bx = MU_0 / (4 * np.pi) * (3 * (mx * Rx + my * Ry) * Rx / R**5 - mx / R**3)
    By = MU_0 / (4 * np.pi) * (3 * (mx * Rx + my * Ry) * Ry / R**5 - my / R**3)

    return Bx, By

# Function to calculate total magnetic field
def calculate_total_field(X, Y, dipole_grid, dipole_moment, uniform_magnitude):
    X_dipoles, Y_dipoles = dipole_grid
    Bx_total = np.zeros_like(X)
    By_total = np.zeros_like(Y)

    for i in range(X_dipoles.size):
        dipole_pos = (X_dipoles.flat[i], Y_dipoles.flat[i])
        Bx, By = calculate_dipole_field(X, Y, dipole_pos, dipole_moment)
        Bx_total += Bx
        By_total += By

    # Set uniform field inside the magnets
    inside_magnet = (X >= X_dipoles.min()) & (X <= X_dipoles.max()) & (Y >= Y_dipoles.min()) & (Y <= Y_dipoles.max())
    Bx_total[inside_magnet] = uniform_magnitude * dipole_moment[0]
    By_total[inside_magnet] = uniform_magnitude * dipole_moment[1]

    return Bx_total, By_total

# Function to plot magnetic field
def plot_magnetic_field(length1, width1, length2, width2, x_pos1, y_pos1, x_pos2, y_pos2, flip1, flip2):
    dipole_magnitude = 1.0
    uniform_magnitude = 0.5  # Uniform field magnitude inside the magnets
    dipole_moment1 = (dipole_magnitude * flip1, 0)
    dipole_moment2 = (dipole_magnitude * flip2, 0)

    num_dipoles_length = 30
    num_dipoles_width = 15

    # Set grid size to 5x5
    grid_size = 5.0
    x_max = grid_size 
    y_max = grid_size 

    x = np.linspace(-x_max, x_max, 250)
    y = np.linspace(-y_max, y_max, 250)
    X, Y = np.meshgrid(x, y)

    x_dipoles1 = np.linspace(-length1/2, length1/2, num_dipoles_length) + x_pos1
    y_dipoles1 = np.linspace(-width1/2, width1/2, num_dipoles_width) + y_pos1
    X_dipoles1, Y_dipoles1 = np.meshgrid(x_dipoles1, y_dipoles1)
    
    x_dipoles2 = np.linspace(-length2/2, length2/2, num_dipoles_length) + x_pos2
    y_dipoles2 = np.linspace(-width2/2, width2/2, num_dipoles_width) + y_pos2
    X_dipoles2, Y_dipoles2 = np.meshgrid(x_dipoles2, y_dipoles2)

    Bx1, By1 = calculate_total_field(X, Y, (X_dipoles1, Y_dipoles1), dipole_moment1, uniform_magnitude)
    Bx2, By2 = calculate_total_field(X, Y, (X_dipoles2, Y_dipoles2), dipole_moment2, uniform_magnitude)

    Bx_total = Bx1 + Bx2
    By_total = By1 + By2

    fig, ax = plt.subplots(figsize=(6, 6))  # Fixed figure size
    ax.streamplot(X, Y, Bx_total, By_total, color=np.sqrt(Bx_total**2 + By_total**2), cmap='plasma', density=2)

    # Adjust the rectangle patches based on the flipping state
    if flip1 == 1:
        rect_red1 = plt.Rectangle((-length1/2 + x_pos1, -width1/2 + y_pos1), length1/2, width1, linewidth=2, edgecolor='black',
                                  facecolor='#069AF3', alpha=1, zorder=2)
        rect_blue1 = plt.Rectangle((x_pos1, -width1/2 + y_pos1), length1/2, width1, linewidth=2, edgecolor='black',
                                   facecolor='#EF4026', alpha=1, zorder=2)
    else:
        rect_red1 = plt.Rectangle((x_pos1, -width1/2 + y_pos1), length1/2, width1, linewidth=2, edgecolor='black',
                                  facecolor='#069AF3', alpha=1, zorder=2)
        rect_blue1 = plt.Rectangle((-length1/2 + x_pos1, -width1/2 + y_pos1), length1/2, width1, linewidth=2, edgecolor='black',
                                   facecolor='#EF4026', alpha=1, zorder=2)

    if flip2 == 1:
        rect_red2 = plt.Rectangle((-length2/2 + x_pos2, -width2/2 + y_pos2), length2/2, width2, linewidth=2, edgecolor='black',
                                  facecolor='#069AF3', alpha=1, zorder=2)
        rect_blue2 = plt.Rectangle((x_pos2, -width2/2 + y_pos2), length2/2, width2, linewidth=2, edgecolor='black',
                                   facecolor='#EF4026', alpha=1, zorder=2)
    else:
        rect_red2 = plt.Rectangle((x_pos2, -width2/2 + y_pos2), length2/2, width2, linewidth=2, edgecolor='black',
                                  facecolor='#069AF3', alpha=1, zorder=2)
        rect_blue2 = plt.Rectangle((-length2/2 + x_pos2, -width2/2 + y_pos2), length2/2, width2, linewidth=2, edgecolor='black',
                                   facecolor='#EF4026', alpha=1, zorder=2)

    ax.add_patch(rect_red1)
    ax.add_patch(rect_blue1)
    ax.add_patch(rect_red2)
    ax.add_patch(rect_blue2)

    ax.set_xlabel("X", fontsize=14)
    ax.set_ylabel("Y", fontsize=14)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.grid(True)
    ax.set_aspect('equal')

    st.pyplot(fig, use_container_width=False)

# Set page configuration
st.set_page_config(
    page_title="Magnetic Field Simulation",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Title and Overview
st.title("Magnetic Field Simulation")
st.markdown("""
### Project Overview
This project demonstrates a simulation of the magnetic field around bar magnets. 
You can control the dimensions, positions, and orientations of the magnets to observe the resulting magnetic field patterns.

**Instructions:**
1. **Magnet Dimensions**: Use the sliders to adjust the length and width of each magnet.
2. **Magnet Position**: Adjust the sliders to set the X and Y positions of the magnets on the grid.
3. **Flip Magnet**: Click the buttons to flip the polarity of the magnets, switching the north and south poles.
4. **Reset**: Resets the magnets to their default positions and orientations.


#### Theoretical Background
Magnetic fields are generated by moving charges or intrinsic magnetic properties of materials. Bar magnets, which consist of aligned atomic dipoles, create a magnetic field that emanates from the north pole and loops around to the south pole. The strength and direction of this field are influenced by the magnet's dimensions, orientation, and the distance between multiple magnets.

This simulation visualizes the magnetic field by solving the magnetic dipole field equations, which approximate the field created by each bar magnet. 

For a more detailed explanation of magnetic fields and dipoles, please refer to [Wikipedia](https://en.wikipedia.org/wiki/Magnetic_field).

#### Author and Repository
Created by [hbarquanta](https://github.com/hbarquanta).

You can find more of my physics and computational projects on my [GitHub](https://github.com/hbarquanta/Physics-Simulations).
""")

# Preset options with more interesting configurations
preset_options = {
    "Aligned": {"length1": 2.0, "width1": 1.0, "x_pos1": -2.0, "y_pos1": 0.0,
                "length2": 2.0, "width2": 1.0, "x_pos2": 2.0, "y_pos2": 0.0, "flip1": 1, "flip2": 1},
    "Opposite": {"length1": 2.0, "width1": 1.0, "x_pos1": -2.0, "y_pos1": 0.0,
                 "length2": 2.0, "width2": 1.0, "x_pos2": 2.0, "y_pos2": 0.0, "flip1": 1, "flip2": -1},
    "Random": {"length1": np.random.uniform(1.0, 4.0), "width1": np.random.uniform(0.5, 1.5), "x_pos1": np.random.uniform(-4.0, 4.0), "y_pos1": np.random.uniform(-4.0, 4.0),
               "length2": np.random.uniform(1.0, 4.0), "width2": np.random.uniform(0.5, 1.5), "x_pos2": np.random.uniform(-4.0, 4.0), "y_pos2": np.random.uniform(-4.0, 4.0), "flip1": np.random.choice([-1, 1]), "flip2": np.random.choice([-1, 1])}
}

# Sidebar controls
st.sidebar.subheader("🔧 Controls")

# Toggle real-time updates
realtime_update = st.sidebar.checkbox("Real-time Update", value=True)

# Preset selection
selected_preset = st.sidebar.selectbox("Select Preset", list(preset_options.keys()))
preset_values = preset_options[selected_preset]

# Apply preset values
if st.sidebar.button("🔄 Reset to Preset"):
    for key, value in preset_values.items():
        st.session_state[key] = value
    if not realtime_update:
        st.session_state.update_needed = True

# Grouped controls in two columns
col1, col2 = st.sidebar.columns(2)

# Controls for Magnet 1
with col1:
    st.subheader("Magnet 1 Controls")
    st.session_state.length1 = st.slider(
        "Length", 1.0, 4.0, st.session_state.length1, 0.2, help="Adjust the length of Magnet 1"
    )
    st.session_state.width1 = st.slider(
        "Width", 0.5, 1.5, st.session_state.width1, 0.1, help="Adjust the width of Magnet 1"
    )
    st.session_state.x_pos1 = st.slider(
        "X Position", -4.0, 4.0, st.session_state.x_pos1, 0.2, help="Adjust the X position of Magnet 1"
    )
    st.session_state.y_pos1 = st.slider(
        "Y Position", -4.0, 4.0, st.session_state.y_pos1, 0.2, help="Adjust the Y position of Magnet 1"
    )
    if st.button("Flip Magnet 1", help="Flip the polarity of Magnet 1"):
        st.session_state.flip1 *= -1
    if not realtime_update:
        st.session_state.update_needed = True

# Controls for Magnet 2
with col2:
    st.subheader("Magnet 2 Controls")
    st.session_state.length2 = st.slider(
        "Length", 1.0, 4.0, st.session_state.length2, 0.2, help="Adjust the length of Magnet 2"
    )
    st.session_state.width2 = st.slider(
        "Width", 0.5, 1.5, st.session_state.width2, 0.1, help="Adjust the width of Magnet 2"
    )
    st.session_state.x_pos2 = st.slider(
        "X Position", -4.0, 4.0, st.session_state.x_pos2, 0.2, help="Adjust the X position of Magnet 2"
    )
    st.session_state.y_pos2 = st.slider(
        "Y Position", -4.0, 4.0, st.session_state.y_pos2, 0.2, help="Adjust the Y position of Magnet 2"
    )
    if st.button("Flip Magnet 2", help="Flip the polarity of Magnet 2"):
        st.session_state.flip2 *= -1
    if not realtime_update:
        st.session_state.update_needed = True

# Simulate button
if not realtime_update:
    if st.sidebar.button("Simulate"):
        plot_magnetic_field(
            st.session_state.length1, st.session_state.width1,
            st.session_state.length2, st.session_state.width2,
            st.session_state.x_pos1, st.session_state.y_pos1,
            st.session_state.x_pos2, st.session_state.y_pos2,
            st.session_state.flip1, st.session_state.flip2
        )
else:
    plot_magnetic_field(
        st.session_state.length1, st.session_state.width1,
        st.session_state.length2, st.session_state.width2,
        st.session_state.x_pos1, st.session_state.y_pos1,
        st.session_state.x_pos2, st.session_state.y_pos2,
        st.session_state.flip1, st.session_state.flip2
    )

st.success('Simulation completed successfully!')
