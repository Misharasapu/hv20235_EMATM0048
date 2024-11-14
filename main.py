# main.py

from Hatchery import Hatchery
from Supplier import Supplier
from Technician import Technician
from Warehouse import Warehouse
from Fish import Fish

def main():
    # Initialize the hatchery instance
    hatchery = Hatchery()
    num_quarters = int(input(">>> Please enter number of quarters: "))

    # Begin the quarterly simulation loop
    for quarter in range(1, num_quarters + 1):
        print("=" * 32)
        print(f"====== SIMULATING quarter {quarter} ======")
        print("=" * 32)

        # Step 1: Technician Management
        tech_change = int(input(
            "To add enter positive, to remove enter negative, no change enter 0.\n>>> Enter number of technicians: "))

        if tech_change > 0:
            technician_names = [input(">>> Enter technician name: ") for _ in range(tech_change)]
            added_technicians = hatchery.add_technicians(technician_names)
            for name in added_technicians:
                print(f"Hired {name}, weekly rate=500 in quarter {quarter}")
            if len(added_technicians) < tech_change:
                print("Reached max technician limit; couldn't hire additional technicians.")
        elif tech_change < 0:
            removed_technicians = hatchery.remove_technicians(abs(tech_change))
            for name in removed_technicians:
                print(f"Let go {name}, weekly rate=500 in quarter {quarter}")
            if len(removed_technicians) < abs(tech_change):
                print("Reached min technician limit; couldn't remove additional technicians.")



# Run the main function
if __name__ == "__main__":
    main()
