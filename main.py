from Hatchery import Hatchery
from Supplier import Supplier
from Technician import Technician
from Warehouse import Warehouse
from Fish import Fish


def main():
    # Initialize the Hatchery instance
    hatchery = Hatchery()

    # Initialize num_quarters with None to prevent IDE warnings
    num_quarters = None

    # Prompt the user to enter the number of quarters, with proper error handling
    while True:
        num_quarters_input = input(
            "Please enter the number of quarters (maximum: 8, default: 8 if no input is given): ").strip()

        if not num_quarters_input:  # If no input is given
            print("No input was provided.")
            while True:
                use_default = input("Would you like to use the default of 8 quarters? (y/n): ").strip().lower()
                if use_default == "y":
                    num_quarters = 8
                    print("Using the default of 8 quarters.")
                    break
                elif use_default == "n":
                    print("Please enter a valid number of quarters.")
                    break
                else:
                    print("Invalid response. Please enter 'y' for yes or 'n' for no.")
            if use_default == "y":
                break  # Exit the outer loop after using the default
            else:
                continue  # Reprompt for number of quarters
        else:
            try:
                num_quarters = int(num_quarters_input)
                if 1 <= num_quarters <= 8:
                    print(f"Simulation will run for {num_quarters} quarters.")
                    break
                else:
                    print("Invalid number. Please enter a value between 1 and 8.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    for quarter in range(1, num_quarters + 1):
        print(
            f"\n================================\n====== SIMULATING quarter {quarter} ======\n================================")

        # Technician management
        while True:
            try:
                technician_change = int(input(
                    "To add enter positive, to remove enter negative, no change enter 0.\n>>> Enter number of technicians: "))
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
                continue  # Reprompt user if input is not an integer

            current_technicians = len(hatchery.technicians)

            if technician_change > 0:  # Adding technicians
                max_addable = Technician.MAX_TECHNICIANS - current_technicians
                if technician_change > max_addable:
                    print(f"Cannot add {technician_change} technicians. Only {max_addable} more can be added.")
                    continue
                else:
                    for _ in range(technician_change):
                        while True:
                            name = input(">>> Enter technician name: ").strip()
                            if name.isdigit():
                                print("Technician name cannot be a number. Please enter a valid name.")
                                continue
                            elif not name:
                                print("No valid input given. Please enter a valid name.")
                                continue
                            elif any(tech.name == name for tech in hatchery.technicians):
                                print(f"A technician with the name '{name}' already exists. Please choose a different name.")
                                continue
                            else:
                                break

                        # Display fish types for specialization
                        print("\nAvailable Fish Types for Specialization:")
                        print(Fish.list_fish_types())

                        while True:
                            try:
                                specialization_choice = int(
                                    input(">>> Enter the number of the fish type to specialize in (0 for none): ")) - 1
                                if specialization_choice == -1:
                                    specialization = None
                                    break
                                fish_types = list(Hatchery.CUSTOMER_DEMAND.keys())
                                if 0 <= specialization_choice < len(fish_types):
                                    specialization = fish_types[specialization_choice]
                                    break
                                else:
                                    print(f"Invalid choice. Please select a number between 1 and {len(fish_types)}.")
                            except ValueError:
                                print("Invalid input. Please enter a valid number.")

                        hired = hatchery.add_technicians([(name, specialization)])
                        if hired:
                            if specialization:
                                print(
                                    f"Hired {name}, weekly rate={Technician.WEEKLY_WAGE}, specialization={specialization} in quarter {quarter}")
                            else:
                                print(f"Hired {name}, weekly rate={Technician.WEEKLY_WAGE} in quarter {quarter}")
                    break

            elif technician_change < 0:  # Removing technicians
                max_removable = current_technicians - Technician.MIN_TECHNICIANS
                if abs(technician_change) > max_removable:
                    print(f"Cannot remove {-technician_change} technicians. Only {max_removable} can be removed.")
                    continue
                else:
                    removed = hatchery.remove_technicians(abs(technician_change))
                    for name in removed:
                        print(f"Let go {name}, weekly rate={Technician.WEEKLY_WAGE} in quarter {quarter}")
                    break

            elif technician_change == 0:
                print("No change in technician count.")
                break

            else:
                print("Invalid input. Please try again.")

        # Reset labor for the new quarter
        hatchery.start_new_quarter()

        # Fish sales management
        for fish_type, data in hatchery.CUSTOMER_DEMAND.items():
            demand = data["demand"]
            current_quantity = None

            while True:
                if current_quantity is None:
                    try:
                        user_input = input(f"Fish {fish_type}, demand {demand}, sell: ").strip()
                        if not user_input:
                            print("No input provided. Please enter a valid quantity.")
                            continue
                        else:
                            current_quantity = int(user_input)
                            if current_quantity < 0:
                                print("You cannot sell a negative quantity. Please enter a positive integer.")
                                current_quantity = None
                                continue
                            if current_quantity > demand:
                                print(f"Cannot sell more than the demand ({demand}). Please enter a valid quantity.")
                                current_quantity = None
                                continue
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")
                        continue

                sale_result = hatchery.sell_fish(fish_type, current_quantity)

                if sale_result["status"] == "success":
                    print(f"Sold {sale_result['sell_quantity']} of {fish_type}")
                    break

                elif sale_result["status"] == "skipped":
                    print(f"Skipping sale of {fish_type}.")
                    break

                elif sale_result["status"] in ["insufficient_labor", "insufficient_resources",
                                               "insufficient_labor_and_resources"]:
                    if "required_labor" in sale_result:
                        print(
                            f"Insufficient labour: required {sale_result['required_labor']:.2f} weeks, available {sale_result['available_labor']:.2f}")
                    if "resources" in sale_result:
                        print("Insufficient ingredients:")
                        for resource, info in sale_result["resources"].items():
                            print(f"   {resource} need {info['needed']}, storage {info['available']}")

                    try:
                        retry = int(input(f"Enter a new quantity for {fish_type} or 0 to skip: "))
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")
                        continue

                    if retry == 0:
                        print(f"Skipping sale of {fish_type}.")
                        break
                    else:
                        current_quantity = retry
                        continue

        # Pay technicians
        technician_payments = hatchery.pay_technicians()
        for payment in technician_payments["individual_payments"]:
            print(f"Paid {payment['name']}, weekly rate={Technician.WEEKLY_WAGE} amount {payment['amount']}")

        # Deduct fixed costs
        print(f"Paid rent/utilities {Hatchery.FIXED_QUARTERLY_COST}")
        hatchery.cash_balance -= Hatchery.FIXED_QUARTERLY_COST

        # Calculate and deduct storage costs
        storage_costs = hatchery.calculate_storage_costs()
        hatchery.cash_balance -= storage_costs["total_storage_cost"]

        # Display storage costs
        for resource, cost in storage_costs["main_costs"].items():
            print(f"Warehouse Main: {resource.capitalize()} cost {cost:.2f}")
        for resource, cost in storage_costs["aux_costs"].items():
            print(f"Warehouse Auxiliary: {resource.capitalize()} cost {cost:.2f}")

        # Apply depreciation
        hatchery.warehouse.calculate_depreciation()

        # Vendor selection and restocking logic
        bankrupt = False  # Flag to track bankruptcy
        while True:
            print("List of Vendors:")
            print(Supplier.list_suppliers())
            try:
                vendor_input = input(">>> Enter the number of the vendor to purchase from: ").strip()
                if not vendor_input:
                    print("No input provided. Please enter a valid vendor number.")
                    continue
                vendor_choice = int(vendor_input) - 1
                vendors = list(Supplier.PRICES.keys())
                if 0 <= vendor_choice < len(vendors):
                    selected_vendor = vendors[vendor_choice]

                    # Attempt to restock with the selected vendor
                    restock_result = hatchery.restock_resources(selected_vendor)

                    if restock_result["status"] == "bankrupt":
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
                        break
                    else:
                        print(
                            f"Restocked successfully with {selected_vendor}. Remaining cash balance: {restock_result['available_cash']:.2f}")
                    break
                else:
                    print(f"Invalid choice. Please select a number between 1 and {len(vendors)}.")
            except ValueError:
                print("Invalid input. Please enter a valid vendor number.")

        if bankrupt:
            break  # Exit the simulation loop if bankrupt

        # End of quarter summary
        if not bankrupt:  # Only display this if not bankrupt
            print(f"\n=== END OF QUARTER {quarter} ===")
            print(f"Hatchery Name: Eastaboga")
            print(f"Cash Balance: {hatchery.cash_balance:.2f}")
            print("Warehouse Stock:")
            for resource, amount in hatchery.warehouse.main_stock.items():
                print(f"  {resource.capitalize()}, {amount} (Main Capacity: {Warehouse.CAPACITIES[resource]['main']})")
            for resource, amount in hatchery.warehouse.aux_stock.items():
                print(f"  {resource.capitalize()}, {amount} (Aux Capacity: {Warehouse.CAPACITIES[resource]['aux']})")
            print("Technicians:")
            for technician in hatchery.technicians:
                print(f"  Technician {technician.name}, weekly rate={Technician.WEEKLY_WAGE}")

    print("\nSimulation completed.")


if __name__ == "__main__":
    main()
