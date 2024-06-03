import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from matplotlib.animation import FuncAnimation, PillowWriter
import streamlit as st

# Define the domain dimensions
Lx = 2.0  # Length of the domain in the x-direction
Ly = 1.0  # Length of the domain in the y-direction
Nx = 200  # Number of grid points in the x-direction
Ny = 100  # Number of grid points in the y-direction
dx = Lx / Nx
dy = Ly / Ny

# Create the mesh grid
x = np.linspace(0, Lx, Nx)
y = np.linspace(0, Ly, Ny)
X, Y = np.meshgrid(x, y)

# Streamlit app layout
st.title("Computational Fluid Dynamics (CFD) Simulation")
st.markdown("""
### Project Overview
This project demonstrates a simulation of fluid flow around various objects using the Navier-Stokes equations. 
You can control parameters such as kinematic viscosity and inlet velocity to observe their effects on the flow patterns.

**Instructions:**
1. **Show Streamlines**: Toggle to show/hide streamlines in the velocity field plot.
2. **Kinematic Viscosity**: Adjust the slider to change the kinematic viscosity, which influences the Reynolds number.
3. **Inlet Velocity**: Adjust the slider to set the velocity of the air entering from the left.
4. **Object Shape**: Select the shape of the object within the flow (circle, square, ellipse, car, or plane).

**Click the "Run Simulation" button to start the simulation.**

#### Theoretical Background
The Navier-Stokes equations describe the motion of fluid substances and are a fundamental part of fluid mechanics. 
These equations are derived from Newton's second law, considering the forces acting on a fluid element. 
They are used to simulate a wide range of phenomena such as weather patterns, ocean currents, and airflow around aircraft.

For more detailed information on the Navier-Stokes equations and their applications, 
you can refer to [Wikipedia](https://en.wikipedia.org/wiki/Navier%E2%80%93Stokes_equations).

#### Author and Repository
Created by [hbarquanta](https://github.com/hbarquanta).

You can find more of my physics and computational projects on my [GitHub](https://github.com/hbarquanta/Physics-Simulations).
""")

st.sidebar.header("Simulation Settings")
show_streamlines = st.sidebar.checkbox("Show streamlines", value=True)
nu = st.sidebar.slider("Kinematic viscosity (ν)", min_value=0.001, max_value=0.1, value=0.01, step=0.001)
inlet_velocity = st.sidebar.slider("Inlet velocity", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
shape = st.sidebar.selectbox("Choose object shape", ["circle", "square", "ellipse", "car", "plane"])

if st.sidebar.button("Run Simulation"):
    # Define the object parameters
    object_center = (0.5, 0.5)

    if shape == "circle":
        radius = 0.1
        object_mask = (X - object_center[0])**2 + (Y - object_center[1])**2 < radius**2
    elif shape == "square":
        side = 0.2
        object_mask = (abs(X - object_center[0]) < side / 2) & (abs(Y - object_center[1]) < side / 2)
    elif shape == "ellipse":
        a = 0.2  # Semi-major axis
        b = 0.1  # Semi-minor axis
        object_mask = ((X - object_center[0])**2 / a**2) + ((Y - object_center[1])**2 / b**2) < 1
    elif shape == "car":
        object_mask = (abs(X - object_center[0]) < 0.15) & (abs(Y - object_center[1]) < 0.05)
    elif shape == "plane":
        object_mask = (abs(X - object_center[0]) < 0.2) & (abs(Y - object_center[1]) < 0.1)
    else:
        st.error("Invalid shape! Please choose from circle, square, ellipse, car, or plane.")
        st.stop()

    object_indices = np.where(object_mask)

    # Initialize velocity and pressure fields
    u = np.zeros((Ny, Nx))  # x-velocity
    v = np.zeros((Ny, Nx))  # y-velocity
    p = np.zeros((Ny, Nx))  # pressure

    # Initialize parameters
    rho = 1.0  # Density
    dt = 0.0001  # Time step size

    @jit(nopython=True)
    def compute_velocity(u, v, p, dx, dy, dt, rho, nu, Nx, Ny, object_indices, inlet_velocity):
        un = u.copy()
        vn = v.copy()

        # Compute the velocity field
        for i in range(1, Nx-1):
            for j in range(1, Ny-1):
                u[j, i] = un[j, i] - dt * (un[j, i] * (un[j, i] - un[j, i-1]) / dx +
                                            vn[j, i] * (un[j, i] - un[j-1, i]) / dy) - \
                          dt / (2 * rho * dx) * (p[j, i+1] - p[j, i-1]) + \
                          nu * dt * ((un[j, i+1] - 2 * un[j, i] + un[j, i-1]) / dx**2 +
                                     (un[j+1, i] - 2 * un[j, i] + un[j-1, i]) / dy**2)

                v[j, i] = vn[j, i] - dt * (un[j, i] * (vn[j, i] - vn[j, i-1]) / dx +
                                            vn[j, i] * (vn[j, i] - vn[j-1, i]) / dy) - \
                          dt / (2 * rho * dy) * (p[j+1, i] - p[j-1, i]) + \
                          nu * dt * ((vn[j, i+1] - 2 * vn[j, i] + vn[j, i-1]) / dx**2 +
                                     (vn[j+1, i] - 2 * vn[j, i] + vn[j-1, i]) / dy**2)

        # Apply boundary conditions
        u[:, 0] = inlet_velocity  # Inlet velocity
        u[:, -1] = 0.0  # Outlet
        v[:, 0] = 0.0
        v[:, -1] = 0.0
        u[0, :] = 0.0
        u[-1, :] = 0.0
        v[0, :] = 0.0
        v[-1, :] = 0.0

        # Apply object boundary condition (no-slip)
        for idx in range(len(object_indices[0])):
            u[object_indices[0][idx], object_indices[1][idx]] = 0.0
            v[object_indices[0][idx], object_indices[1][idx]] = 0.0

        return u, v

    @jit(nopython=True)
    def compute_pressure(u, v, p, dx, dy, dt, rho, Nx, Ny):
        pn = np.zeros_like(p)

        for _ in range(50):  # Iterative solver for pressure
            pn = p.copy()
            p[1:-1, 1:-1] = ((pn[1:-1, 2:] + pn[1:-1, :-2]) * dy**2 +
                             (pn[2:, 1:-1] + pn[:-2, 1:-1]) * dx**2) / \
                            (2 * (dx**2 + dy**2)) - \
                            rho * dx**2 * dy**2 / (2 * (dx**2 + dy**2)) * \
                            ((u[1:-1, 2:] - u[1:-1, :-2]) / (2 * dx) +
                             (v[2:, 1:-1] - v[:-2, 1:-1]) / (2 * dy)) / dt

            # Boundary conditions for pressure
            p[:, -1] = p[:, -2]  # dp/dx = 0 at outlet
            p[:, 0] = p[:, 1]  # dp/dx = 0 at inlet
            p[0, :] = p[1, :]  # dp/dy = 0 at top
            p[-1, :] = p[-2, :]  # dp/dy = 0 at bottom

        return p

    # Time-stepping loop parameters
    nt = 2000  # Number of time steps
    n_interval = 10  # Interval for frames in the animation

    # Create the animation
    def create_animation(u, v, X, Y, object_mask, nt, n_interval, show_streamlines, inlet_velocity):
        fig, ax1 = plt.subplots(figsize=(8, 4))
        progress_bar = st.progress(0)

        # Initial plot
        contourf1 = ax1.contourf(X, Y, np.sqrt(u**2 + v**2), cmap='jet', levels=100, extend='both')
        quiver1 = ax1.quiver(X[::3, ::3], Y[::3, ::3], u[::3, ::3], v[::3, ::3])
        if show_streamlines:
            stream = ax1.streamplot(X, Y, u, v, color='k', linewidth=0.5, density=1.5)
        ax1.contour(X, Y, object_mask, colors='k', linewidths=2)  # Black boundary for object

        def update(frame):
            global u, v, p
            for _ in range(n_interval):
                u, v = compute_velocity(u, v, p, dx, dy, dt, rho, nu, Nx, Ny, object_indices, inlet_velocity)
                p = compute_pressure(u, v, p, dx, dy, dt, rho, Nx, Ny)

            # Update velocity field
            for c in ax1.collections:
                c.remove()
            ax1.clear()
            contourf1 = ax1.contourf(X, Y, np.sqrt(u**2 + v**2), cmap='jet', levels=100, extend='both')
            quiver1 = ax1.quiver(X[::3, ::3], Y[::3, ::3], u[::3, ::3], v[::3, ::3])
            if show_streamlines:
                stream = ax1.streamplot(X, Y, u, v, color='k', linewidth=0.5, density=1.5)
            ax1.contour(X, Y, object_mask, colors='k', linewidths=2)  # Black boundary for object
            ax1.set_title(f'Velocity Field (Time step: {frame * n_interval})')

            # Progress indication
            if frame % (nt // n_interval // 10) == 0:  # Update progress every 10% of total frames
                progress_bar.progress(frame * 100 // (nt // n_interval))

            if show_streamlines:
                return contourf1.collections + [quiver1, stream.lines]
            else:
                return contourf1.collections + [quiver1]

        ani = FuncAnimation(fig, update, frames=nt // n_interval, blit=True)
        return ani

    # Create and display the animation
    ani = create_animation(u, v, X, Y, object_mask, nt, n_interval, show_streamlines, inlet_velocity)
    ani.save("navier_stokes_simulation.gif", writer=PillowWriter(fps=10))

    st.image("navier_stokes_simulation.gif", caption="Navier-Stokes Simulation")

    # Display final plot
    fig, ax1 = plt.subplots(figsize=(8, 4))
    contourf1 = ax1.contourf(X, Y, np.sqrt(u**2 + v**2), cmap='jet', levels=100, extend='both')
    quiver1 = ax1.quiver(X[::3, ::3], Y[::3, ::3], u[::3, ::3], v[::3, ::3])
    if show_streamlines:
        stream = ax1.streamplot(X, Y, u, v, color='k', linewidth=0.5, density=1.5)
    ax1.contour(X, Y, object_mask, colors='k', linewidths=2)  # Black boundary for object
    ax1.set_title(f'Final Velocity Field')

    st.pyplot(fig)
