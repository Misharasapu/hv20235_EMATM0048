from Hatchery import Hatchery
from Supplier import Supplier
from Technician import Technician
from Warehouse import Warehouse
from Fish import Fish


def main():
    # Initialize the Hatchery instance
    hatchery = Hatchery()

    # Debug: Initial cash balance
    print(f"DEBUG: Initial Cash Balance: {hatchery.cash_balance}")

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

        while True:
            # Prompt for technician management
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
                    continue  # Reprompt the user
                else:
                    for _ in range(technician_change):
                        while True:
                            name = input(">>> Enter technician name: ").strip()
                            if name.isdigit():  # Check if the input is purely numeric
                                print("Technician name cannot be a number. Please enter a valid name.")
                                continue
                            elif not name:  # Check if input is empty
                                print("No valid input given. Please enter a valid name.")
                                continue
                            elif any(tech.name == name for tech in hatchery.technicians):  # Check for duplicate names
                                print(
                                    f"A technician with the name '{name}' already exists. Please choose a different name.")
                                continue
                            else:
                                break  # Exit the loop if a valid and unique name is provided

                        # Display fish types for specialization
                        print("\nAvailable Fish Types for Specialization:")
                        print(Fish.list_fish_types())

                        while True:
                            try:
                                specialization_choice = int(
                                    input(">>> Enter the number of the fish type to specialize in (0 for none): ")) - 1
                                if specialization_choice == -1:  # User chose '0' for no specialization
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

                        # Add the technician immediately after getting their details
                        hired = hatchery.add_technicians([(name, specialization)])
                        if hired:  # If hiring was successful
                            if specialization:  # Check if a specialization is provided
                                print(
                                    f"Hired {name}, weekly rate={Technician.WEEKLY_WAGE}, specialization={specialization} in quarter {quarter}")
                            else:
                                print(f"Hired {name}, weekly rate={Technician.WEEKLY_WAGE} in quarter {quarter}")
                    break  # Exit the loop after successful addition

            elif technician_change < 0:  # Removing technicians
                max_removable = current_technicians - Technician.MIN_TECHNICIANS
                if abs(technician_change) > max_removable:
                    print(f"Cannot remove {-technician_change} technicians. Only {max_removable} can be removed.")
                    continue  # Reprompt the user
                else:
                    removed = hatchery.remove_technicians(abs(technician_change))
                    for name in removed:
                        print(f"Let go {name}, weekly rate={Technician.WEEKLY_WAGE} in quarter {quarter}")
                    break  # Exit the loop after successful removal

            elif technician_change == 0:
                print("No change in technician count.")
                break  # Exit the loop if no change

            else:
                print("Invalid input. Please try again.")

        # Reset labor for the new quarter
        hatchery.start_new_quarter()

        # Debug: Labor after reset
        print(f"DEBUG: Starting labor after reset: {hatchery.available_labor}")

        # Fish sales management
        for fish_type, data in hatchery.CUSTOMER_DEMAND.items():
            demand = data["demand"]
            current_quantity = None  # Track the latest sell quantity

            while True:
                # Prompt user for sell quantity only if not retrying
                if current_quantity is None:
                    try:
                        user_input = input(f"Fish {fish_type}, demand {demand}, sell (default: {demand}): ").strip()
                        if not user_input:  # Handle no input
                            print("No input provided. Please enter a valid quantity.")
                            continue  # Reprompt the user
                        else:
                            current_quantity = int(user_input)
                            if current_quantity < 0:
                                print("You cannot sell a negative quantity. Please enter a positive integer.")
                                current_quantity = None  # Reset to reprompt the user
                                continue
                            if current_quantity > demand:
                                print(f"Cannot sell more than the demand ({demand}). Please enter a valid quantity.")
                                current_quantity = None  # Reset to reprompt the user
                                continue
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")
                        continue

                sale_result = hatchery.sell_fish(fish_type, current_quantity)

                if sale_result["status"] == "success":
                    # Process successful sale
                    print(f"Sold {sale_result['sell_quantity']} of {fish_type}")
                    print(
                        f"DEBUG: Sold {sale_result['sell_quantity']} of {fish_type} for revenue {sale_result['revenue']}.")
                    print(f"DEBUG: Updated Cash Balance: {hatchery.cash_balance}")
                    break  # Exit loop on successful sale

                elif sale_result["status"] == "skipped":
                    # Handle skipped fish type
                    print(f"Skipping sale of {fish_type}.")
                    break  # Exit loop on skipped status

                elif sale_result["status"] in ["insufficient_labor", "insufficient_resources",
                                               "insufficient_labor_and_resources"]:
                    # Inform the user of the issue
                    if "required_labor" in sale_result:
                        print(
                            f"Insufficient labour: required {sale_result['required_labor']:.2f} weeks, available {sale_result['available_labor']:.2f}")
                    if "resources" in sale_result:
                        print("Insufficient ingredients:")
                        for resource, info in sale_result["resources"].items():
                            print(f"   {resource} need {info['needed']}, storage {info['available']}")

                    # Prompt user for retry
                    try:
                        retry = int(input(f"Enter a new quantity for {fish_type} or 0 to skip: "))
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")
                        continue

                    if retry == 0:
                        print(f"Skipping sale of {fish_type}.")
                        break  # Skip this fish type
                    else:
                        current_quantity = retry  # Update current_quantity for retry
                        continue  # Retry with new input

        # Pay technicians
        technician_payments = hatchery.pay_technicians()
        for payment in technician_payments["individual_payments"]:
            print(f"Paid {payment['name']}, weekly rate={Technician.WEEKLY_WAGE} amount {payment['amount']}")
        # Debug: Cash balance after technician payments
        print(f"DEBUG: Cash Balance after technician payments: {hatchery.cash_balance}")

        # Deduct fixed costs
        print(f"Paid rent/utilities {Hatchery.FIXED_QUARTERLY_COST}")
        hatchery.cash_balance -= Hatchery.FIXED_QUARTERLY_COST
        # Debug: Cash balance after fixed costs
        print(f"DEBUG: Cash Balance after fixed costs: {hatchery.cash_balance}")

        # Calculate and deduct storage costs
        storage_costs = hatchery.calculate_storage_costs()
        hatchery.cash_balance -= storage_costs["total_storage_cost"]

        # Debug: Storage cost details
        print(f"DEBUG: Total Storage Costs: {storage_costs['total_storage_cost']}")
        print(f"DEBUG: Cash Balance after storage costs: {hatchery.cash_balance}")

        # Display storage costs
        for resource, cost in storage_costs["main_costs"].items():
            print(f"Warehouse Main: {resource.capitalize()} cost {cost:.2f}")
        for resource, cost in storage_costs["aux_costs"].items():
            print(f"Warehouse Auxiliary: {resource.capitalize()} cost {cost:.2f}")

        # Apply depreciation at the end of every quarter
        print("\nApplying depreciation to the warehouses...")
        main_stock, aux_stock = hatchery.warehouse.calculate_depreciation()
        print("Depreciation applied. Updated stock levels:")
        for resource, amount in main_stock.items():
            print(f"Warehouse Main: {resource.capitalize()}, {amount}")
        for resource, amount in aux_stock.items():
            print(f"Warehouse Auxiliary: {resource.capitalize()}, {amount}")

        # Display vendor list and prompt user for selection
        while True:
            print("List of Vendors:")
            print(Supplier.list_suppliers())
            try:
                vendor_input = input(">>> Enter the number of the vendor to purchase from: ").strip()
                if not vendor_input:  # Handle no input
                    print("No input provided. Please enter a valid vendor number.")
                    continue
                vendor_choice = int(vendor_input) - 1  # Convert to zero-based index

                vendors = list(Supplier.PRICES.keys())  # Get the list of vendor names
                if 0 <= vendor_choice < len(vendors):  # Validate vendor choice
                    selected_vendor = vendors[vendor_choice]

                    # Call restock function with selected vendor and available cash
                    restock_result = hatchery.restock_resources(selected_vendor)

                    # Handle restocking results
                    if "total_restock_cost" in restock_result:
                        print(
                            f"Restocked successfully with {selected_vendor}. Remaining cash balance: {restock_result['available_cash']:.2f}")
                        # Debug: Restocking details
                        print(f"DEBUG: Total Restocking Costs: {restock_result['total_restock_cost']}")
                        print(f"DEBUG: Cash Balance after restocking: {restock_result['available_cash']}")
                        print("Updated stock levels:")
                        for resource, amount in restock_result["main_stock"].items():
                            print(
                                f"Warehouse Main: {resource.capitalize()}, {amount} (capacity={Warehouse.CAPACITIES[resource]['main']})")
                        for resource, amount in restock_result["aux_stock"].items():
                            print(
                                f"Warehouse Auxiliary: {resource.capitalize()}, {amount} (capacity={Warehouse.CAPACITIES[resource]['aux']})")
                    elif restock_result["status"] == "bankrupt":
                        print(
                            f"Can't restock {restock_result['resource']}, insufficient funds. Need {restock_result['needed']:.2f} but only have {restock_result['available_cash']:.2f}")
                        print(f"Went bankrupt restocking warehouse {restock_result['warehouse']} in quarter {quarter}")

                        # Display final state
                        print(f"\n=== FINAL STATE quarter {quarter + 1} ===")
                        print(f"\nHatchery Name: Eastaboga, Cash: {hatchery.cash_balance:.2f}")
                        print("Warehouse Main")
                        for resource, amount in hatchery.warehouse.main_stock.items():
                            print(
                                f"  {resource.capitalize()}, {amount} (capacity={Warehouse.CAPACITIES[resource]['main']})")
                        print("Warehouse Auxiliary")
                        for resource, amount in hatchery.warehouse.aux_stock.items():
                            print(
                                f"  {resource.capitalize()}, {amount} (capacity={Warehouse.CAPACITIES[resource]['aux']})")
                        print("Technicians")
                        for technician in hatchery.technicians:
                            print(f"  Technician {technician.name}, weekly rate={Technician.WEEKLY_WAGE}")
                    break  # Exit loop after successful restocking or bankruptcy
                else:
                    print(f"Invalid choice. Please select a number between 1 and {len(vendors)}.")
            except ValueError:
                print("Invalid input. Please enter a valid vendor number.")

        # Debug: End of quarter cash balance
        print(f"DEBUG: End of Quarter {quarter} Cash Balance: {hatchery.cash_balance}")

    print("\nSimulation completed.")
    print(f"Final Cash Balance: {hatchery.cash_balance:.2f}")


# Run the main function
if __name__ == "__main__":
    main()
