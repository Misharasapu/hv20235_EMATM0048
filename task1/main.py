from Hatchery import Hatchery
from Supplier import Supplier
from Technician import Technician
from Warehouse import Warehouse
from Fish import Fish

"""
Author: Mishara Sapukotanage
Section: Data Science 
Description: This script runs the main program for the fish hatchery simulation. It 
manages the overall flow of the simulation, including technician management, 
fish sales, resource handling, and cash flow. The simulation aims to run for a specified 
number of quarters unless the hatchery goes bankrupt.
"""

def main():
    """
    The main function serves as the entry point for the hatchery simulation. It prompts
    the user for inputs such as the number of quarters, manages the quarterly operations
    including technician hiring/firing, fish sales, resource restocking, and cash balance
    management. The simulation runs until the specified number of quarters or until
    bankruptcy occurs.

    Returns:
        None
    """
    # Initialize the Hatchery instance that manages all resources and operations
    hatchery = Hatchery()

    # Initialize num_quarters to store the simulation duration
    num_quarters = None

    # Prompt the user to enter the number of quarters to run the simulation
    while True:
        # Prompt the user for input and strip any unnecessary spaces
        num_quarters_input = input(
            "Please enter the number of quarters (maximum: 8, default: 8 if no input is given): ").strip()

        if not num_quarters_input:  # Handle case where no input is provided
            print("No input was provided.")
            while True:
                # Ask the user if they want to use the default value of 8 quarters
                use_default = input("Would you like to use the default of 8 quarters? (y/n): ").strip().lower()
                if use_default == "y":  # If user confirms, set the default value
                    num_quarters = 8  # Default simulation duration
                    print("Using the default of 8 quarters.")
                    break
                elif use_default == "n":  # If user denies, ask for a valid input again
                    print("Please enter a valid number of quarters.")
                    break
                else:
                    # Inform the user that the input is invalid and reprompt
                    print("Invalid response. Please enter 'y' for yes or 'n' for no.")
            if use_default == "y":  # Exit the outer loop if default is selected
                break
            else:
                continue  # Reprompt the user for a valid number of quarters
        else:
            try:
                # Attempt to convert the user input to an integer
                num_quarters = int(num_quarters_input)
                # Validate that the number is between 1 and 8
                if 1 <= num_quarters <= 8:
                    print(f"Simulation will run for {num_quarters} quarters.")
                    break  # Exit the loop once a valid number is entered
                else:
                    # Inform the user if the number is out of the valid range
                    print("Invalid number. Please enter a value between 1 and 8.")
            except ValueError:
                # Inform the user if the input is not a valid integer
                print("Invalid input. Please enter a valid integer.")

    # Loop through the specified number of quarters
    for quarter in range(1, num_quarters + 1):
        # Print a header for the current quarter to indicate progress
        print(
            f"\n================================\n====== SIMULATING quarter {quarter} ======\n================================")

        # Technician management: Allows hiring or firing of technicians
        while True:
            try:
                # Prompt the user to add, remove, or make no changes to technicians
                technician_change = int(input(
                    "To add enter positive, to remove enter negative, no change enter 0.\n>>> Enter number of technicians: "))
            except ValueError:
                # Inform the user if the input is invalid and reprompt
                print("Invalid input. Please enter a valid integer.")
                continue

            # Get the current number of technicians employed
            current_technicians = len(hatchery.technicians)

            if technician_change > 0:  # Adding technicians
                # Calculate how many more technicians can be added without exceeding the limit
                max_addable = Technician.MAX_TECHNICIANS - current_technicians
                if technician_change > max_addable:
                    # Inform the user if they are trying to add more technicians than allowed
                    print(f"Cannot add {technician_change} technicians. Only {max_addable} more can be added.")
                    continue
                else:
                    # Loop to add the specified number of technicians
                    for _ in range(technician_change):
                        while True:
                            # Prompt the user to enter the name of the technician
                            name = input(">>> Enter technician name: ").strip()
                            # Validate the name to ensure it's not empty or numeric and isn't a duplicate
                            if name.isdigit():
                                print("Technician name cannot be a number. Please enter a valid name.")
                                continue
                            elif not name:
                                print("No valid input given. Please enter a valid name.")
                                continue
                            elif any(tech.name == name for tech in hatchery.technicians):
                                print(
                                    f"A technician with the name '{name}' already exists. Please choose a different name.")
                                continue
                            else:
                                break

                        # Display the list of fish types for specialization
                        print("\nAvailable Fish Types for Specialization:")
                        print(Fish.list_fish_types())

                        while True:
                            try:
                                # Prompt the user to choose a specialization or opt for none
                                specialization_choice = int(
                                    input(">>> Enter the number of the fish type to specialize in (0 for none): ")) - 1
                                if specialization_choice == -1:
                                    # Set specialization to None if the user chooses 0
                                    specialization = None
                                    break
                                # Get the list of available fish types
                                fish_types = list(Hatchery.CUSTOMER_DEMAND.keys())
                                if 0 <= specialization_choice < len(fish_types):
                                    # Assign the selected fish type as specialization
                                    specialization = fish_types[specialization_choice]
                                    break
                                else:
                                    # Inform the user if the selection is out of range
                                    print(f"Invalid choice. Please select a number between 1 and {len(fish_types)}.")
                            except ValueError:
                                # Handle invalid input for specialization choice
                                print("Invalid input. Please enter a valid number.")

                        # Add the technician with the specified name and specialization to the hatchery
                        hired = hatchery.add_technicians([(name, specialization)])
                        if hired:
                            # Confirm the hiring and display details
                            if specialization:
                                print(
                                    f"Hired {name}, weekly rate={Technician.WEEKLY_WAGE}, specialization={specialization} in quarter {quarter}")
                            else:
                                print(f"Hired {name}, weekly rate={Technician.WEEKLY_WAGE} in quarter {quarter}")
                    break

            elif technician_change < 0:  # Removing technicians
                # Calculate how many technicians can be removed without falling below the minimum limit
                max_removable = current_technicians - Technician.MIN_TECHNICIANS
                if abs(technician_change) > max_removable:
                    # Inform the user if they are trying to remove more technicians than allowed
                    print(f"Cannot remove {-technician_change} technicians. Only {max_removable} can be removed.")
                    continue
                else:
                    # Remove the specified number of technicians
                    removed = hatchery.remove_technicians(abs(technician_change))
                    # Confirm the removal and display details
                    for name in removed:
                        print(f"Let go {name}, weekly rate={Technician.WEEKLY_WAGE} in quarter {quarter}")
                    break

            elif technician_change == 0:  # No changes to technician count
                print("No change in technician count.")
                break

            else:
                # Handle unexpected cases
                print("Invalid input. Please try again.")

        # Reset labor availability for the new quarter
        hatchery.start_new_quarter()

        # Fish sales management: Prompt user for sales quantities
        for fish_type, data in hatchery.CUSTOMER_DEMAND.items():  # Loop through all fish types in customer demand
            demand = data["demand"]  # Retrieve the demand for the current fish type
            current_quantity = None  # Initialize the quantity to be sold as None

            while True:  # Loop until a valid quantity is entered or the sale is skipped
                if current_quantity is None:  # Check if no quantity has been set yet
                    try:
                        # Prompt the user to input the quantity to sell
                        user_input = input(f"Fish {fish_type}, demand {demand}, sell: ").strip()
                        if not user_input:  # Handle case where no input is provided
                            print("No input provided. Please enter a valid quantity.")
                            continue
                        else:
                            current_quantity = int(user_input)  # Convert input to an integer
                            if current_quantity < 0:  # Ensure the quantity is not negative
                                print("You cannot sell a negative quantity. Please enter a positive integer.")
                                current_quantity = None  # Reset quantity for re-entry
                                continue
                            if current_quantity > demand:  # Ensure the quantity does not exceed demand
                                print(f"Cannot sell more than the demand ({demand}). Please enter a valid quantity.")
                                current_quantity = None  # Reset quantity for re-entry
                                continue
                    except ValueError:  # Handle invalid input (e.g., non-integer values)
                        print("Invalid input. Please enter a valid integer.")
                        continue

                # Attempt to sell the specified quantity of fish
                sale_result = hatchery.sell_fish(fish_type, current_quantity)

                if sale_result["status"] == "success":  # Check if the sale was successful
                    print(f"Sold {sale_result['sell_quantity']} of {fish_type}")  # Display the quantity sold
                    break  # Exit the loop for this fish type

                elif sale_result["status"] == "skipped":  # Handle case where the sale is skipped
                    print(f"Skipping sale of {fish_type}.")  # Inform the user
                    break  # Exit the loop for this fish type

                elif sale_result["status"] in ["insufficient_labor", "insufficient_resources",
                                               "insufficient_labor_and_resources"]:  # Handle constraints
                    # Display labor constraints if applicable
                    if "required_labor" in sale_result:
                        print(
                            f"Insufficient labour: required {sale_result['required_labor']:.2f} weeks, available {sale_result['available_labor']:.2f}")
                    # Display resource shortages if applicable
                    if "resources" in sale_result:
                        print("Insufficient ingredients:")
                        for resource, info in sale_result["resources"].items():
                            print(f"   {resource} need {info['needed']}, storage {info['available']}")

                    try:
                        # Prompt the user to retry with a different quantity or skip the sale
                        retry = int(input(f"Enter a new quantity for {fish_type} or 0 to skip: "))
                    except ValueError:  # Handle invalid input for retry
                        print("Invalid input. Please enter a valid integer.")
                        continue

                    if retry == 0:  # If the user chooses to skip the sale
                        print(f"Skipping sale of {fish_type}.")
                        break
                    else:
                        current_quantity = retry  # Update the quantity and retry the sale
                        continue

        # Pay technicians and deduct their wages
        technician_payments = hatchery.pay_technicians()  # Calculate and process technician payments
        for payment in technician_payments["individual_payments"]:  # Loop through individual payments
            # Display payment details for each technician
            print(f"Paid {payment['name']}, weekly rate={Technician.WEEKLY_WAGE} amount {payment['amount']}")

        # Deduct fixed costs for the quarter
        print(f"Paid rent/utilities {Hatchery.FIXED_QUARTERLY_COST}")  # Inform the user of fixed cost deduction
        hatchery.cash_balance -= Hatchery.FIXED_QUARTERLY_COST  # Subtract fixed costs from cash balance

        # Calculate and deduct storage costs for warehouses
        storage_costs = hatchery.calculate_storage_costs()  # Calculate storage costs
        hatchery.cash_balance -= storage_costs["total_storage_cost"]  # Subtract total storage costs from cash balance

        # Display storage costs by warehouse
        for resource, cost in storage_costs["main_costs"].items():  # Loop through main warehouse costs
            print(f"Warehouse Main: {resource.capitalize()} cost {cost:.2f}")
        for resource, cost in storage_costs["aux_costs"].items():  # Loop through auxiliary warehouse costs
            print(f"Warehouse Auxiliary: {resource.capitalize()} cost {cost:.2f}")

        # Apply depreciation to warehouse stocks
        hatchery.warehouse.calculate_depreciation()  # Reduce stock levels based on depreciation rates

        # Vendor selection and restocking
        bankrupt = False  # Initialize bankruptcy flag
        while True:  # Loop until resources are restocked or bankruptcy occurs
            print("List of Vendors:")  # Display available vendors
            print(Supplier.list_suppliers())  # List vendor names and indices
            try:
                # Prompt the user to select a vendor for restocking
                vendor_input = input(">>> Enter the number of the vendor to purchase from: ").strip()
                if not vendor_input:  # Handle case where no input is provided
                    print("No input provided. Please enter a valid vendor number.")
                    continue
                vendor_choice = int(vendor_input) - 1  # Convert input to an index
                vendors = list(Supplier.PRICES.keys())  # Retrieve list of available vendors
                if 0 <= vendor_choice < len(vendors):  # Validate vendor choice
                    selected_vendor = vendors[vendor_choice]  # Get the selected vendor's name

                    # Attempt to restock with the selected vendor
                    restock_result = hatchery.restock_resources(selected_vendor)

                    if restock_result["status"] == "bankrupt":  # Check if funds are insufficient
                        # Display bankruptcy details
                        print(
                            f"Can't restock {restock_result['resource']}, insufficient funds. Need {restock_result['needed']:.2f} but only have {restock_result['available_cash']:.2f}")
                        print(f"Went bankrupt restocking warehouse {restock_result['warehouse']} in quarter {quarter}")
                        print(f"\n=== FINAL STATE quarter {quarter + 1} ===")
                        print(f"Hatchery Name: Eastaboga, Cash: {hatchery.cash_balance:.2f}")
                        for resource, amount in hatchery.warehouse.main_stock.items():
                            print(f"Warehouse Main: {resource.capitalize()}, {amount}")
                        for resource, amount in hatchery.warehouse.aux_stock.items():
                            print(f"Warehouse Auxiliary: {resource.capitalize()}, {amount}")
                        for technician in hatchery.technicians:
                            print(f"Technician: {technician.name}, weekly rate={Technician.WEEKLY_WAGE}")
                        bankrupt = True  # Set bankruptcy flag
                        break  # Exit the loop if bankrupt
                    else:
                        # Confirm successful restocking
                        print(
                            f"Restocked successfully with {selected_vendor}. Remaining cash balance: {restock_result['available_cash']:.2f}")
                    break
                else:
                    # Inform the user if the vendor choice is out of range
                    print(f"Invalid choice. Please select a number between 1 and {len(vendors)}.")
            except ValueError:  # Handle invalid input for vendor selection
                print("Invalid input. Please enter a valid vendor number.")

        if bankrupt:  # Exit the simulation loop if bankrupt
            break

        # End-of-quarter summary
        if not bankrupt:  # If the hatchery is not bankrupt
            print(f"\n=== END OF QUARTER {quarter} ===")
            print(f"Hatchery Name: Eastaboga")
            print(f"Cash Balance: {hatchery.cash_balance:.2f}")  # Display the current cash balance
            print("Warehouse Stock:")
            for resource, amount in hatchery.warehouse.main_stock.items():  # Display main warehouse stock
                print(f"  {resource.capitalize()}, {amount} (Main Capacity: {Warehouse.CAPACITIES[resource]['main']})")
            for resource, amount in hatchery.warehouse.aux_stock.items():  # Display auxiliary warehouse stock
                print(f"  {resource.capitalize()}, {amount} (Aux Capacity: {Warehouse.CAPACITIES[resource]['aux']})")
            print("Technicians:")
            for technician in hatchery.technicians:  # Display details of all employed technicians
                print(f"  Technician {technician.name}, weekly rate={Technician.WEEKLY_WAGE}")
            print(f"\n--- END OF QUARTER {quarter} ---\n")

    print("\nSimulation completed.")  # Indicate the end of the simulation


if __name__ == "__main__":
    main()
