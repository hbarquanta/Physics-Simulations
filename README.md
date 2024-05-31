# Physics Simulations

## Overview
Welcome to the Physics Simulations repository! This collection includes various physics simulations that do not belong to any of my other themed repositories. These simulations are created using Python and Jupyter Notebooks, providing an interactive and visual approach to understanding complex physical phenomena.

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contents](#contents)
  - [Double-Slit Experiment](#double-slit-experiment)
  - [Cellular Automata](#cellular-automata)
  - [Double Pendulum](#double-pendulum)
- [Contributing](#contributing)
- [License](#license)

## Introduction
Physics simulations are powerful tools for visualizing and understanding physical processes and phenomena. This repository includes simulations such as the Double-Slit Experiment, Cellular Automata, and the Double Pendulum, which help illustrate core concepts in quantum mechanics and complex systems.

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
cd applications/double_pendulum
pip install -r requirements.txt
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

### Cellular Automata
- **Celular Automata.ipynb**: This notebook explores cellular automata, including the Game of Life, illustrating how simple rules can lead to complex behaviors.
  - **Animations**: View the animations [here](https://github.com/hbarquanta/Physics-Simulations/tree/main/Animations).

### Double Pendulum
- **[Double Pendulum Application](applications/double_pendulum/Double_Pendulum_App.py)**: This application simulates the motion of a double pendulum.
  - **How to Run:**
    ```bash
    cd applications/double_pendulum
    pip install -r requirements.txt
    streamlit run Double_Pendulum_App.py
    ```
  - **Live Demo**: Check out the live demo [here](https://physics-simulations-doublependulum.streamlit.app/).
  - **Animations**: View the animations [here](https://github.com/hbarquanta/Physics-Simulations/tree/main/Animations).

## Contributing
Contributions are welcome! If you would like to improve the simulations or add new ones, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
