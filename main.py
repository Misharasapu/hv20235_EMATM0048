from Hatchery import Hatchery
from Supplier import Supplier
from Technician import Technician
from Warehouse import Warehouse
from Fish import Fish


def main():
    # Initialize the Hatchery instance
    hatchery = Hatchery()

    # Prompt the user to enter the number of quarters
    num_quarters = int(input("Please enter number of quarters: "))

    for quarter in range(1, num_quarters + 1):
        print(
            f"\n================================\n====== SIMULATING quarter {quarter} ======\n================================")

        # Prompt for technician management
        technician_change = int(input(
            "To add enter positive, to remove enter negative, no change enter 0.\n>>> Enter number of technicians: "))
        if technician_change > 0:
            technician_names = [input(f">>> Enter technician name: ") for _ in range(technician_change)]
            hired = hatchery.add_technicians(technician_names)
            for name in hired:
                print(f"Hired {name}, weekly rate={Technician.WEEKLY_WAGE} in quarter {quarter}")
        elif technician_change < 0:
            removed = hatchery.remove_technicians(abs(technician_change))
            for name in removed:
                print(f"Let go {name}, weekly rate={Technician.WEEKLY_WAGE} in quarter {quarter}")

        # Reset labor for the new quarter
        hatchery.start_new_quarter()

        # Fish sales management
        for fish_type, data in hatchery.CUSTOMER_DEMAND.items():
            demand = data["demand"]
            while True:
                sell_quantity = min(demand, int(input(f"Fish {fish_type}, demand {demand}, sell {demand}: ")))
                sale_result = hatchery.sell_fish(fish_type, sell_quantity)

                if sale_result["status"] == "success":
                    print(f"Sold {sale_result['sell_quantity']} of {fish_type}")
                    break  # Successful sale, exit the loop for this fish type

                elif sale_result["status"] == "insufficient_labor_and_resources":
                    print(
                        f"Insufficient labour: required {sale_result['required_labor']:.2f} weeks, available {sale_result['available_labor']:.2f}")
                    print("Insufficient ingredients:")
                    for resource, info in sale_result["resources"].items():
                        print(f"   {resource} need {info['needed']}, storage {info['available']}")
                    retry = input(
                        f"Insufficient resources and labor for {fish_type}. Enter a new quantity or 0 to skip: ")
                    if retry == "0":
                        print(f"Fish {fish_type}, demand {demand}, sell {sell_quantity}: 0")
                        break
                    else:
                        demand = int(retry)  # Update with a new sell quantity based on user input

                elif sale_result["status"] == "insufficient_labor":
                    print(
                        f"Insufficient labour: required {sale_result['required_labor']:.2f} weeks, available {sale_result['available_labor']:.2f}")
                    print(f"Fish {fish_type}, demand {demand}, sell {sell_quantity}: 0")
                    break

                elif sale_result["status"] == "insufficient_resources":
                    print("Insufficient ingredients:")
                    for resource, info in sale_result["resources"].items():
                        print(f"   {resource} need {info['needed']}, storage {info['available']}")
                    retry = input(f"Insufficient resources for {fish_type}. Enter a new quantity or 0 to skip: ")
                    if retry == "0":
                        print(f"Fish {fish_type}, demand {demand}, sell {sell_quantity}: 0")
                        break
                    else:
                        demand = int(retry)  # Update with a new sell quantity based on user input

        # Pay technicians
        technician_payments = hatchery.pay_technicians()
        for payment in technician_payments["individual_payments"]:
            print(f"Paid {payment['name']}, weekly rate={Technician.WEEKLY_WAGE} amount {payment['amount']}")

        # Deduct fixed costs
        print(f"Paid rent/utilities {Hatchery.FIXED_QUARTERLY_COST}")

        # Calculate and display storage costs
        storage_costs = hatchery.calculate_storage_costs()
        for resource, cost in storage_costs["main_costs"].items():
            print(f"Warehouse Main: {resource.capitalize()} cost {cost:.2f}")
        for resource, cost in storage_costs["aux_costs"].items():
            print(f"Warehouse Auxiliary: {resource.capitalize()} cost {cost:.2f}")

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
                    f"Restocked successfully with {selected_vendor}. Remaining cash balance: {restock_result['remaining_cash_balance']:.2f}")
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
        else:
            print("Invalid vendor selection.")







# Run the main function
if __name__ == "__main__":
    main()
