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

    # Prompt the user to enter the number of quarters, defaulting to 8 if no input is given
    num_quarters_input = input("Please enter number of quarters (default: 8): ")
    if num_quarters_input.strip() == "":
        num_quarters = 8  # Default to 8 if input is empty
    else:
        num_quarters = min(int(num_quarters_input), 8)  # Cap the number of quarters at 8


    for quarter in range(1, num_quarters + 1):
        print(
            f"\n================================\n====== SIMULATING quarter {quarter} ======\n================================")

        # Prompt for technician management
        technician_change = int(input(
            "To add enter positive, to remove enter negative, no change enter 0.\n>>> Enter number of technicians: "))
        if technician_change > 0:
            technician_details = []
            for _ in range(technician_change):
                name = input(">>> Enter technician name: ")
                specialization = input(">>> Enter specialization (leave blank for none): ").strip() or None
                technician_details.append((name, specialization))
            hired = hatchery.add_technicians(technician_details)
            for name in hired:
                print(f"Hired {name}, weekly rate={Technician.WEEKLY_WAGE} in quarter {quarter}")
        elif technician_change < 0:
            removed = hatchery.remove_technicians(abs(technician_change))
            for name in removed:
                print(f"Let go {name}, weekly rate={Technician.WEEKLY_WAGE} in quarter {quarter}")

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
                        current_quantity = int(
                            input(f"Fish {fish_type}, demand {demand}, sell (default: {demand}): ") or demand)
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
        print("List of Vendors:")
        print(Supplier.list_suppliers())
        vendor_choice = int(input(">>> Enter number of vendor to purchase from: ")) - 1

        # Get the vendor name based on user selection
        vendors = list(Supplier.PRICES.keys())  # Get the list of vendor names
        if 0 <= vendor_choice < len(vendors):
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
                    print(f"  {resource.capitalize()}, {amount} (capacity={Warehouse.CAPACITIES[resource]['main']})")
                print("Warehouse Auxiliary")
                for resource, amount in hatchery.warehouse.aux_stock.items():
                    print(f"  {resource.capitalize()}, {amount} (capacity={Warehouse.CAPACITIES[resource]['aux']})")
                print("Technicians")
                for technician in hatchery.technicians:
                    print(f"  Technician {technician.name}, weekly rate={Technician.WEEKLY_WAGE}")


                # Exit the simulation loop
                break
        else:
            print("Invalid vendor selection.")

        # Debug: End of quarter cash balance
        print(f"DEBUG: End of Quarter {quarter} Cash Balance: {hatchery.cash_balance}")

    print("\nSimulation completed.")
    print(f"Final Cash Balance: {hatchery.cash_balance:.2f}")


# Run the main function
if __name__ == "__main__":
    main()
