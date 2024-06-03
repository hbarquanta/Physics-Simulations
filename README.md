# Physics Simulations

## Overview
Welcome to the Physics Simulations repository! This collection includes various physics simulations that do not belong to any of my other themed repositories. These simulations are created using Python and Jupyter Notebooks, providing an interactive and visual approach to understanding complex physical phenomena.

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Repository Structure](#repository-structure)
- [Usage](#usage)
- [Contents](#contents)
  - [Double-Slit Experiment](#double-slit-experiment)
  - [Cellular Automata](#cellular-automata)
  - [Double Pendulum](#double-pendulum)
  - [Fluid Dynamics](#fluid-dynamics)
- [Contributing](#contributing)
- [License](#license)


## Introduction
Physics simulations are powerful tools for visualizing and understanding physical processes and phenomena. This repository includes simulations such as the Double-Slit Experiment, Cellular Automata, the Double Pendulum, and Fluid Dynamics, which help illustrate core concepts in quantum mechanics, complex systems, and fluid mechanics.

## Prerequisites
Ensure you have the following software installed:
- Python 3.x
- Jupyter Notebook
- NumPy
- Matplotlib
- Other dependencies as specified in the notebooks

## Installation
Clone the repository and install the required libraries:

```bash
git clone https://github.com/hbarquanta/Physics-Simulations.git
cd Physics-Simulations
```

To install dependencies for a specific application, navigate to the application's directory and install the requirements:

```bash
cd Applications/Double_Pendulum
pip install -r requirements.txt
```

For the Fluid Dynamics application:
```bash
cd Applications/Fluid_Dynamics
pip install -r requirements.txt
```
## Repository Structure

The repository is organized as follows:

```
Physics-Simulations/
├── Animations/
│   ├── automata_simulation.gif
│   ├── double_pendulum_simulation.gif
│   ├── double_slit_simulation.gif
│   └── navier_stokes_simulation.gif
├── Applications/
│   ├── Double_Pendulum/
│   │   ├── Double_Pendulum_App.py
│   │   └── requirements.txt
│   ├── Fluid_Dynamics/
│   │   ├── Fluid_Dynamics_App.py
│   │   ├── requirements.txt
│   │   └── car.png
│   └── ...
├── Cellular Automata.ipynb
├── Double_Slit_Experiment.ipynb
├── Double_Pendulum.ipynb
├── Fluid_Dynamics.ipynb
└── README.md
```

## Usage
To run the Jupyter notebooks, navigate to the repository directory and start Jupyter Notebook:

```bash
jupyter notebook
```

Open the notebook you are interested in from the Jupyter interface.

## Contents

### Double-Slit Experiment
- **Double_Slit_Experiment.ipynb**: This notebook simulates the famous double-slit experiment, demonstrating the wave-particle duality of light and matter.
  - **Animations**: View the animations [here](https://github.com/hbarquanta/Physics-Simulations/tree/main/Animations/schroedinger_equation_2d_evolution_double_slit.gif).

### Cellular Automata
- **Celular Automata.ipynb**: This notebook explores cellular automata, including the Game of Life, illustrating how simple rules can lead to complex behaviors.
  - **Animations**: View the animations [here](https://github.com/hbarquanta/Physics-Simulations/tree/main/Animations/automata_simulation.gif).

### Double Pendulum
- **Double_Pendulum.ipynb**: This notebook describes the theoretical framework of the (chaotic) Double Pendulum, explores how a slight change of initial conditions leads to completely different solutions after a certain time span i.e. chaotic behavior, and also includes the basic code for the standalone application.
- **[Double Pendulum Application](Applications/Double_Pendulum/Double_Pendulum_App.py)**: This application simulates the motion of a double pendulum.
  - **How to Run:**
    ```bash
    cd Applications/Double_Pendulum
    pip install -r requirements.txt
    streamlit run Double_Pendulum_App.py
    ```
  - **Live Demo**: Check out the live demo [here](https://physics-simulations-doublependulum.streamlit.app/).
  - **Animations**: View the animations [here](https://github.com/hbarquanta/Physics-Simulations/tree/main/Animations/double_pendulum_simulation.gif).

### Fluid Dynamics
- **Fluid_Dynamics.ipynb**: This notebook contains a basic implementation of fluid dynamics simulations using the Navier-Stokes equations.
- **[Fluid Dynamics Application](Applications/Fluid_Dynamics/Fluid_Dynamics_App.py)**: This Streamlit application simulates fluid flow around various objects, such as circles, squares, ellipses, cars, and planes.
  - **How to Run:**
    ```bash
    cd Applications/Fluid_Dynamics
    pip install -r requirements.txt
    streamlit run Fluid_Dynamics_App.py
    ```
  - **Live Demo**: Check out the live demo [here](https://physics-simulations-fluiddynamics.streamlit.app/).
  - **Animations**: View the animations [here](https://github.com/hbarquanta/Physics-Simulations/tree/main/Animations/navier_stokes_simulation.gif).

## Contributing
Contributions are welcome! If you would like to improve the simulations or add new ones, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

