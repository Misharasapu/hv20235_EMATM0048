# Fish Hatchery Simulation - Task 1

## Overview
The Fish Hatchery Simulation is a program designed to model the operations of a fish hatchery. **Task 1** focuses on implementing the core functionality of the simulation, including technician management, fish sales, resource handling, and financial operations. The simulation runs for a user-specified number of quarters or until the hatchery goes bankrupt.

The primary goal of this simulation is to balance cash flow, resource management, and labour allocation while meeting customer demand for various fish types.

---

## Key Features
1. **Technician Management**:
   - Hire or fire technicians each quarter.
   - Assign specialisations to technicians for specific fish types, improving efficiency.
   - Pay technician wages at the end of each quarter.

2. **Fish Sales**:
   - Sell fish based on customer demand for each species.
   - Calculate sales revenue while considering resource availability and labour constraints.

3. **Resource Management**:
   - Track resource stock levels (fertiliser, feed, salt) in both main and auxiliary warehouses.
   - Apply depreciation to resources each quarter.
   - Restock resources from suppliers based on pricing and available cash.

4. **Financial Management**:
   - Deduct fixed costs (e.g., rent and utilities) each quarter.
   - Calculate and deduct storage costs for resources.
   - Monitor cash flow to avoid bankruptcy.

---

## How the Simulation Works
The simulation is structured around user-defined quarters, with operations carried out sequentially in each quarter:
1. Specify the number of quarters (1–8) for the simulation.
2. Manage technicians (hire/fire) at the start of each quarter.
3. Sell fish based on customer demand, ensuring sufficient resources and labour are available.
4. Restock resources from selected suppliers while managing cash flow.
5. Pay technician wages, deduct fixed costs, and calculate storage costs.
6. Apply depreciation to resources at the end of each quarter.
7. Repeat the process for the remaining quarters or until bankruptcy.

---

## Running the Simulation
### Prerequisites
- **Python 3.x** installed on your system.
- All required Python files must be in the same directory:
  - `main.py` (entry point for the simulation)
  - `Hatchery.py`
  - `Technician.py`
  - `Warehouse.py`
  - `Fish.py`
  - `Supplier.py`

### Steps to Run
1. Clone or download the project repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
2. Open a terminal in the project directory.
3. Run the main script:
   ```bash
   python main.py
4. Follow the on-screen prompts:
   - Enter the number of quarters for the simulation.
   - Manage technicians by hiring or firing them.
   - Input quantities of fish to sell for each type.
   - Choose a supplier for resource restocking.


	
### Example Commands
- Input `8` to run the simulation for 8 quarters.
- Hire 2 technicians in the first quarter, with one specialising in "Clef Fins."
- Sell fish based on demand while ensuring sufficient resources are available.
- Restock resources from "Slippery Lakes" as required.

### Example Console Output
```
Please enter the number of quarters (maximum: 8, default: 8 if no input is given): 8
Simulation will run for 8 quarters.

================================
====== SIMULATING quarter 1 ======
================================
To add enter positive, to remove enter negative, no change enter 0.
>>> Enter number of technicians: 2
>>> Enter technician name: Alice
Hired Alice, weekly rate=500
...
Simulation completed.
Final Cash Balance: $9600.00
```

### Project Structure
- **main.py**: Entry point for the simulation
- **Hatchery.py**: Manages overall operations and financials
- **Technician.py**: Handles technician hiring, wages, and specialisation
- **Warehouse.py**: Manages resource stock, costs, and depreciation
- **Fish.py**: Provides fish-related operations and data
- **Supplier.py**: Handles supplier information and pricing
- **README.md**: Documentation for Task 1


### Example Simulation Flow
1. **Quarter 1**:
   - Hire 2 technicians, one specialising in "Clef Fins."
   - Sell 20 units of "Clef Fins" and 10 units of "Timpani Snapper."
   - Restock fertiliser and feed from "Slippery Lakes."
   - Deduct fixed costs, pay technician wages, and calculate storage costs.

2. **Quarter 2**:
   - Hire 1 additional technician specialising in "Plagal Cod."
   - Sell fish based on demand and available resources.
   - Apply depreciation to warehouse resources.

3. **Quarter 3–8**:
   - Repeat the above steps while monitoring cash flow and avoiding bankruptcy.



### Notes
- The simulation ends early if the hatchery goes bankrupt.
- Ensure all required files are in the same directory before running the program.
- Results, including the hatchery's final state, are displayed at the end of the simulation.

---

### Author
**Mishara Sapukotanage**  
Data Science, University of Bristol  
Contact: [misharasapu@gmail.com](mailto:misharasapu@gmail.com)

---

### Additional Information

#### Suppliers
- The simulation uses two suppliers for resource restocking:
  - **Slippery Lakes**: Offers lower prices for feed and salt.
  - **Scaly Wholesaler**: Offers lower prices for fertiliser.

#### Resources
- `Fertiliser`: Measured in millilitres (ml).
- `Feed`: Measured in kilograms (kg).
- `Salt`: Measured in kilograms (kg).

#### Labour
- Each technician provides **9 weeks** of labour per quarter. Specialised technicians are more efficient when working with their assigned fish types.

### License
This project is for educational purposes only and is not licensed for commercial use.

