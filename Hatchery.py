
from Technician import Technician
from Warehouse import Warehouse
from Fish import Fish
from Supplier import Supplier


class Hatchery:
    # Static data related to customer demand and fixed quarterly cost
    CUSTOMER_DEMAND = {
        "Clef Fins": {"demand": 25, "price": 250},
        "Timpani Snapper": {"demand": 10, "price": 350},
        "Andalusian Brim": {"demand": 15, "price": 250},
        "Plagal Cod": {"demand": 20, "price": 400},
        "Fugue Flounder": {"demand": 30, "price": 550},
        "Modal Bass": {"demand": 50, "price": 500}
    }
    FIXED_QUARTERLY_COST = 1500  # Fixed cost incurred each quarter

    def __init__(self):
        # Initialize starting cash balance
        self.cash_balance = 10000  # Starting cash balance for the hatchery
        # Initialize an empty list to hold technician objects
        self.technicians = []
        # Create a single Warehouse instance
        self.warehouse = Warehouse()

    @classmethod
    def get_demand_and_price(cls, fish_type):
        """
        Retrieve the demand and price for a specific fish type.

        :param fish_type: Name of the fish species.
        :return: Dictionary containing 'demand' and 'price' for the specified fish, or None if not found.
        """
        return cls.CUSTOMER_DEMAND.get(fish_type, None)

    @classmethod
    def get_fixed_cost(cls):
        """
        Return the fixed quarterly cost for the hatchery.

        :return: Fixed cost for the quarter.
        """
        return cls.FIXED_QUARTERLY_COST

    def get_cash_balance(self):
        """
        Return the current cash balance of the hatchery.

        :return: Current cash balance.
        """
        return self.cash_balance

    def add_technicians(self, technician_names):
        """
        Add new technicians to the hatchery based on provided names list.
        Ensures total number of technicians does not exceed the maximum limit.

        :param technician_names: List of names for technicians to be added.
        :return: None
        """

        # Check if adding the specified number of technicians exceeds the maximum limit
        if len(self.technicians) + len(technician_names) > Technician.MAX_TECHNICIANS:
            print(f"Cannot add all technicians; exceeds maximum limit of {Technician.MAX_TECHNICIANS}.")
            return

        # Track hired technicians to return this list if needed
        hired_technicians = []
        for name in technician_names:
            if len(self.technicians) < Technician.MAX_TECHNICIANS:
                new_technician = Technician(name)
                self.technicians.append(new_technician)
                hired_technicians.append(name)
                print(f"Hired {name}, weekly rate={Technician.WEEKLY_WAGE} in this quarter")
            else:
                break

        return hired_technicians  # Return list of successfully added technician names

    def remove_technicians(self, num_to_remove):
        """
        Remove technicians from the hatchery. Ensures the total number of technicians does not fall below the minimum limit.

        :param num_to_remove: Number of technicians to remove.
        :return: List of removed technician names for potential verification/testing.
        """
        removed_technicians = []

        # Check if removing the specified number of technicians is allowed
        if len(self.technicians) - num_to_remove < Technician.MIN_TECHNICIANS:
            print(f"Cannot remove {num_to_remove} technicians; minimum of {Technician.MIN_TECHNICIANS} required.")
            return removed_technicians  # Return empty list if removal fails

        # Remove the specified number of technicians from the end of the list
        for _ in range(num_to_remove):
            if self.technicians:
                removed_technician = self.technicians.pop()  # Remove the last technician
                print(f"Let go {removed_technician.name}, weekly rate={Technician.WEEKLY_WAGE} in this quarter")
                removed_technicians.append(removed_technician.name)

        return removed_technicians

    def sell_fish(self):
        """
        Sell fish based on customer demand, available labor, and resources.
        Updates cash balance with revenue from fish sales, allowing partial sales if resources or labor are insufficient.

        :return: None
        """
        total_revenue = 0
        available_labor = Technician.calculate_total_labour(len(self.technicians))  # Calculate available labor

        # Iterate over each fish type to check demand and resource requirements
        for fish_type, demand_data in self.CUSTOMER_DEMAND.items():
            demand = demand_data["demand"]
            price = demand_data["price"]

            # Calculate resource and labor needs for the demanded quantity
            resource_needs = Fish.calculate_resource_needs(fish_type, demand)  # Assuming this returns a dictionary
            maintenance_time = Fish.calculate_total_maintenance_time(fish_type, demand)

            # Initialize sell_quantity as full demand
            sell_quantity = demand

            # Adjust sell_quantity based on available labor
            if available_labor < maintenance_time * demand:
                max_labor_based_quantity = int(available_labor // maintenance_time)
                print(f"Insufficient labour: required {maintenance_time * demand}, available {available_labor}")
                sell_quantity = min(sell_quantity, max_labor_based_quantity)

            # Adjust sell_quantity based on available resources
            for resource, amount_needed_per_unit in resource_needs.items():
                total_amount_needed = sell_quantity * amount_needed_per_unit
                available_amount = self.warehouse.main_stock.get(resource, 0) + self.warehouse.aux_stock.get(resource,
                                                                                                             0)

                # If resources are insufficient for full demand, calculate feasible quantity based on resource
                if available_amount < total_amount_needed:
                    possible_quantity_based_on_resource = int(available_amount // amount_needed_per_unit)
                    print(
                        f"Insufficient ingredients for {resource}: need {total_amount_needed}, available {available_amount}")
                    sell_quantity = min(sell_quantity, possible_quantity_based_on_resource)

            # Deduct resources based on the final sell_quantity
            for resource, amount_needed_per_unit in resource_needs.items():
                self.warehouse.check_and_deduct_resources(resource, sell_quantity * amount_needed_per_unit)

            # Calculate revenue and adjust labor based on the final sell_quantity
            revenue = sell_quantity * price
            total_revenue += revenue
            available_labor -= sell_quantity * maintenance_time  # Deduct labor used for this sale

            # Print sales results
            print(f"Fish {fish_type}, demand {demand}, sell {sell_quantity}: {sell_quantity}")

        # Update the hatchery's cash balance with total revenue
        self.cash_balance += total_revenue
        print(f"Total revenue from fish sales: {total_revenue}")

    def pay_technicians(self):
        """
        Pays each technician based on their quarterly wage and updates the hatchery's cash balance.
        Logs each payment made.

        :return: Total payment amount for all technicians.
        """
        total_payment = Technician.calculate_total_wages(
            self.technicians)  # Use the class method to calculate total wages

        # Iterate through each technician to log individual payments
        for technician in self.technicians:
            payment = technician.get_wage()
            print(f"Paid {technician.name}, weekly rate={Technician.WEEKLY_WAGE} amount {payment}")

        # Deduct total payment from cash balance
        self.cash_balance -= total_payment
        print(f"Total payment for all technicians: {total_payment}")

        return total_payment

    def calculate_storage_costs(self):
        """
        Calculate and log storage costs for both main and auxiliary warehouses.

        :return: Total storage cost.
        """
        # Retrieve detailed storage costs for main and auxiliary warehouses
        main_costs, aux_costs = self.warehouse.get_storage_costs()

        # Log each resource's cost for main and auxiliary warehouses
        for resource, cost in main_costs.items():
            print(f"Warehouse Main: {resource.capitalize()} cost {cost:.2f}")

        for resource, cost in aux_costs.items():
            print(f"Warehouse Auxiliary: {resource.capitalize()} cost {cost:.2f}")

        # Calculate and return total storage cost
        total_storage_cost = sum(main_costs.values()) + sum(aux_costs.values())
        return total_storage_cost

    def restock_resources(self, vendor_name):
        """
        Restocks resources in the main and auxiliary warehouses based on the given vendor and available funds.
        Updates the hatchery's cash balance after restocking.

        :param vendor_name: Name of the selected vendor.
        :return: Total cost of restocking.
        """
        # Attempt to restock with the provided vendor
        total_restock_cost = self.warehouse.restock_to_full(vendor_name, self.cash_balance)

        # Update the balance if restocking cost is within available cash
        if total_restock_cost <= self.cash_balance:
            self.cash_balance -= total_restock_cost
            print(f"Total restocking cost: {total_restock_cost:.2f}")
        else:
            # If funds are insufficient for a full restock, print a message and set cash balance to zero if exhausted
            print(
                f"Unable to fully restock. Restocking cost was limited by available funds to {total_restock_cost:.2f}")
            self.cash_balance = 0

        return total_restock_cost

    def end_of_quarter_summary(self, supplier_name):
        """
        Calculates and deducts end-of-quarter expenses, including fixed costs, technician wages,
        warehouse storage costs, and restocking costs. Updates the hatchery's cash balance accordingly
        and returns a detailed summary of all expenses.

        :param supplier_name: Name of the selected supplier for restocking costs.
        :return: A dictionary containing a detailed breakdown of expenses, total expenses, and remaining cash balance.
        """
        # Fixed quarterly cost (class attribute)
        fixed_costs = self.get_fixed_cost()

        # Calculate technician wages for the quarter
        technician_wages = Technician.calculate_total_wages(self.technicians)

        # Calculate storage costs in the warehouse
        storage_costs = self.calculate_storage_costs()  # This should return the total storage cost

        # Calculate restocking costs using the selected supplier (for demonstration, can be adjusted based on requirements)
        restocking_costs = self.restock_resources(supplier_name)["total_restock_cost"]

        # Total expenses for the quarter
        total_expenses = fixed_costs + technician_wages + storage_costs + restocking_costs

        # Deduct total expenses from cash balance
        self.cash_balance -= total_expenses

        # Return a summary dictionary with detailed expenses
        return {
            "fixed_costs": fixed_costs,
            "technician_wages": technician_wages,
            "storage_costs": storage_costs,
            "restocking_costs": restocking_costs,
            "total_expenses": total_expenses,
            "remaining_cash_balance": self.cash_balance
        }



