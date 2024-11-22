from Hatchery import Hatchery
from Technician import Technician
from Fish import Fish

# Create Hatchery instance
hatchery = Hatchery()

# Add technicians
hatchery.technicians.append(Technician("Alice", "Clef Fins"))  # Specialized in Clef Fins
hatchery.technicians.append(Technician("Bob"))  # Regular technician

# Start a new quarter to initialize labor
hatchery.start_new_quarter()

# Case 1: Labor and Resources Constraint
print("\n--- Test Case 1: Labor and Resources Constraint ---")
# Deplete the warehouse resources to simulate insufficient resources
hatchery.warehouse.main_stock["fertiliser"] = 0
hatchery.warehouse.main_stock["feed"] = 0
hatchery.warehouse.main_stock["salt"] = 0
result1 = hatchery.sell_fish("Clef Fins", 50)  # Demand exceeds available labor and resources
print("Result:", result1)

# Reset resources for next test
hatchery.warehouse.main_stock["fertiliser"] = 10000  # Partial refill
hatchery.warehouse.main_stock["feed"] = 200  # Partial refill
hatchery.warehouse.main_stock["salt"] = 50  # Partial refill

# Case 2: Only Resources Constraint
print("\n--- Test Case 2: Resources Constraint Only ---")
result2 = hatchery.sell_fish("Clef Fins", 50)  # Sufficient labor but insufficient resources
print("Result:", result2)

# Reset resources to full capacity for next test
hatchery.warehouse.main_stock = {
    "fertiliser": 20000,
    "feed": 400,
    "salt": 200
}
hatchery.available_labor = 5  # Reduce labor to simulate a labor constraint

# Case 3: Only Labor Constraint
print("\n--- Test Case 3: Labor Constraint Only ---")
result3 = hatchery.sell_fish("Clef Fins", 10)  # Insufficient labor but sufficient resources
print("Result:", result3)
