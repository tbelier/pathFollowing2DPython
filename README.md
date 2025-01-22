# Path Following Simulation in 2D

![Visualization of Path Following](img/pathFollowing.png)

## Overview
This repository enables users to simulate a Remotely Operated Vehicle (ROV) navigating along a predefined 2D path. The path-following algorithm is based on the seminal paper by L. Lapierre and A. Pascoal: *"Nonsingular Path Following Control of a Unicycle in the Presence of Parametric Modelling Uncertainties".*

To create the paths used in this simulation, refer to my [trajectoryMaker](https://github.com/yourusername/trajectoryMaker) repository.

With this simulation tool, you can:
- Simulate an ROV following a given trajectory.
- Visualize the robot's path-following behavior and its convergence to the path.
- Analyze the performance of the control algorithm through visual outputs.

---

## Features
- **Path Following Simulation:** Observe the ROV joining and following a predefined path.
- **2D Visualization:** Visualize the robot's trajectory and path.
- **Dynamic Behavior Analysis:** Analyze the robot's approach and adherence to the trajectory.
- **Reference Paper:** Implementation inspired by a robust path-following control approach for unicycle models.

---

## Installation
1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd pathFollowing2DPython
   ```

2. Install the required dependencies:
   ```bash
   Nore required dependencies, everything is in the repo.
   ```

3. Run the simulation:
   ```bash
   python3 main.py
   ```

4. Visualize the results using the generated outputs in the `img/` directory.

---

## Example of Visualizations

#### Initial Path Following Visualization:
- Observe the initial setup and trajectory plan:
![Path Following Visualization](img/pathFollowing.png)

#### Robot Joining the Path:
- The ROV begins by navigating towards the path before following it:
![Joining the Path - Step 1](img/pathFollowing2.png)
![Joining the Path - Step 2](img/pathFollowing3.png)

---

## Reference
**Paper:** L. Lapierre, A. Pascoal - *Nonsingular Path Following Control of a Unicycle in the Presence of Parametric Modelling Uncertainties.*

For questions or contributions, feel free to open an issue or submit a pull request.


