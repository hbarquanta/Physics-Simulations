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

# Initialize Streamlit controls
st.title("Navier-Stokes Simulation")
show_streamlines = st.sidebar.checkbox("Show Streamlines", value=True)
reynolds_number = st.sidebar.slider("Reynolds Number", min_value=1, max_value=500, value=100)
shape = st.sidebar.selectbox("Initial Shape", ["Cylinder", "Square"])

# Adjust parameters based on Reynolds number
rho = 1.0  # Density
nu = 1.0 / reynolds_number  # Kinematic viscosity adjusted by Reynolds number
dt = 0.0001  # Time step size

# Define the initial shape parameters
if shape == "Cylinder":
    radius = 0.1
    cylinder_center = (0.5, 0.5)
    cylinder_mask = (X - cylinder_center[0])**2 + (Y - cylinder_center[1])**2 < radius**2
elif shape == "Square":
    side = 0.2
    square_center = (0.5, 0.5)
    cylinder_mask = (abs(X - square_center[0]) < side / 2) & (abs(Y - square_center[1]) < side / 2)

cylinder_indices = np.where(cylinder_mask)

# Initialize velocity and pressure fields
u = np.zeros((Ny, Nx))  # x-velocity
v = np.zeros((Ny, Nx))  # y-velocity
p = np.zeros((Ny, Nx))  # pressure

@jit(nopython=True)
def compute_velocity(u, v, p, dx, dy, dt, rho, nu, Nx, Ny, cylinder_indices):
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
    u[:, 0] = 1.0    # Inlet velocity
    u[:, -1] = 0.0   # Outlet
    v[:, 0] = 0.0
    v[:, -1] = 0.0
    u[0, :] = 0.0
    u[-1, :] = 0.0
    v[0, :] = 0.0
    v[-1, :] = 0.0

    # Apply cylinder boundary condition (no-slip)
    for idx in range(len(cylinder_indices[0])):
        u[cylinder_indices[0][idx], cylinder_indices[1][idx]] = 0.0
        v[cylinder_indices[0][idx], cylinder_indices[1][idx]] = 0.0

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
        p[:, 0] = p[:, 1]    # dp/dx = 0 at inlet
        p[0, :] = p[1, :]    # dp/dy = 0 at top
        p[-1, :] = p[-2, :]  # dp/dy = 0 at bottom

    return p

# Time-stepping loop parameters
nt = 2000  # Number of time steps
n_interval = 10  # Interval for frames in the animation

# Create the animation
def create_animation(u, v, p, X, Y, cylinder_mask, nt, n_interval, show_streamlines):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

    # Initial plot
    contourf1 = ax1.contourf(X, Y, np.sqrt(u**2 + v**2), cmap='jet')
    quiver1 = ax1.quiver(X[::3, ::3], Y[::3, ::3], u[::3, ::3], v[::3, ::3])
    if show_streamlines:
        stream = ax1.streamplot(X, Y, u, v, color='k', linewidth=0.5, density=1.5)
    contourf2 = ax2.contourf(X, Y, p, cmap='jet')

    def update(frame):
        global u, v, p
        for _ in range(n_interval):
            u, v = compute_velocity(u, v, p, dx, dy, dt, rho, nu, Nx, Ny, cylinder_indices)
            p = compute_pressure(u, v, p, dx, dy, dt, rho, Nx, Ny)

        # Update velocity field
        for c in ax1.collections:
            c.remove()
        ax1.clear()
        contourf1 = ax1.contourf(X, Y, np.sqrt(u**2 + v**2), cmap='jet')
        quiver1 = ax1.quiver(X[::3, ::3], Y[::3, ::3], u[::3, ::3], v[::3, ::3])
        if show_streamlines:
            stream = ax1.streamplot(X, Y, u, v, color='k', linewidth=0.5, density=1.5)
        ax1.set_title(f'Velocity Field (Time step: {frame * n_interval})')

        # Update pressure field
        for c in ax2.collections:
            c.remove()
        ax2.clear()
        contourf2 = ax2.contourf(X, Y, p, cmap='jet')
        ax2.set_title(f'Pressure Field (Time step: {frame * n_interval})')

        if show_streamlines:
            return contourf1.collections + contourf2.collections + [quiver1, stream.lines]
        else:
            return contourf1.collections + contourf2.collections + [quiver1]

    ani = FuncAnimation(fig, update, frames=nt // n_interval, blit=True)
    return ani

# Create and display the animation
ani = create_animation(u, v, p, X, Y, cylinder_mask, nt, n_interval, show_streamlines)
ani.save("navier_stokes_simulation.gif", writer=PillowWriter(fps=10))

st.image("navier_stokes_simulation.gif", caption="Navier-Stokes Simulation")
