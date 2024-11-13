
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
        :return: List of successfully added technician names.
        """
        if len(self.technicians) + len(technician_names) > Technician.MAX_TECHNICIANS:
            return []  # Exceeds maximum, return an empty list

        hired_technicians = []
        for name in technician_names:
            if len(self.technicians) < Technician.MAX_TECHNICIANS:
                new_technician = Technician(name)
                self.technicians.append(new_technician)
                hired_technicians.append(name)
            else:
                break

        return hired_technicians

    def remove_technicians(self, num_to_remove):
        """
        Remove technicians from the hatchery. Ensures the total number of technicians does not fall below the minimum limit.

        :param num_to_remove: Number of technicians to remove.
        :return: List of removed technician names for potential verification/testing.
        """
        removed_technicians = []

        if len(self.technicians) - num_to_remove < Technician.MIN_TECHNICIANS:
            return []  # Cannot remove as it would drop below minimum

        for _ in range(num_to_remove):
            if self.technicians:
                removed_technician = self.technicians.pop()
                removed_technicians.append(removed_technician.name)

        return removed_technicians

    def sell_fish(self):
        """
        Sell fish based on customer demand, available labor, and resources.
        Returns sales results and revenue without direct output to the console.

        :return: Dictionary with sale quantities, revenues, and unmet demand details.
        """
        total_revenue = 0
        available_labor = Technician.calculate_total_labour(len(self.technicians))
        sales_results = []

        for fish_type, demand_data in self.CUSTOMER_DEMAND.items():
            demand = demand_data["demand"]
            price = demand_data["price"]
            resource_needs = Fish.calculate_resource_needs(fish_type, demand)
            maintenance_time = Fish.calculate_total_maintenance_time(fish_type, demand)
            sell_quantity = demand

            if available_labor < maintenance_time * demand:
                max_labor_based_quantity = int(available_labor // maintenance_time)
                sell_quantity = min(sell_quantity, max_labor_based_quantity)

            for resource, amount_needed_per_unit in resource_needs.items():
                total_amount_needed = sell_quantity * amount_needed_per_unit
                available_amount = self.warehouse.main_stock.get(resource, 0) + self.warehouse.aux_stock.get(resource,
                                                                                                             0)

                if available_amount < total_amount_needed:
                    possible_quantity_based_on_resource = int(available_amount // amount_needed_per_unit)
                    sell_quantity = min(sell_quantity, possible_quantity_based_on_resource)

            for resource, amount_needed_per_unit in resource_needs.items():
                self.warehouse.check_and_deduct_resources(resource, sell_quantity * amount_needed_per_unit)

            revenue = sell_quantity * price
            total_revenue += revenue
            available_labor -= sell_quantity * maintenance_time

            sales_results.append({
                "fish_type": fish_type,
                "demand": demand,
                "sell_quantity": sell_quantity,
                "revenue": revenue
            })

        self.cash_balance += total_revenue
        return {"total_revenue": total_revenue, "sales_details": sales_results}

    def pay_technicians(self):
        """
        Pays each technician based on their quarterly wage and updates the hatchery's cash balance.
        Returns a list of payment details for each technician without console output.

        :return: Total payment amount and a list of individual payment details.
        """
        total_payment = Technician.calculate_total_wages(self.technicians)
        payments = [{"name": technician.name, "amount": technician.get_wage()} for technician in self.technicians]

        # Deduct total payment from cash balance
        self.cash_balance -= total_payment

        return {"total_payment": total_payment, "individual_payments": payments}

    def calculate_storage_costs(self):
        """
        Calculate storage costs for both main and auxiliary warehouses.
        Returns detailed storage costs per resource without printing.

        :return: Dictionary with total storage costs and detailed costs per resource.
        """
        main_costs, aux_costs = self.warehouse.get_storage_costs()
        total_storage_cost = sum(main_costs.values()) + sum(aux_costs.values())

        return {
            "total_storage_cost": total_storage_cost,
            "main_costs": main_costs,
            "aux_costs": aux_costs
        }

    def restock_resources(self, vendor_name):
        """
        Restocks resources in the main and auxiliary warehouses based on the given vendor and available funds.
        Updates the hatchery's cash balance after restocking.

        :param vendor_name: Name of the selected vendor.
        :return: Dictionary containing restock cost and updated stock levels.
        """
        total_restock_cost = self.warehouse.restock_to_full(vendor_name, self.cash_balance)
        self.cash_balance -= total_restock_cost

        return {
            "total_restock_cost": total_restock_cost,
            "remaining_cash_balance": self.cash_balance,
            "main_stock": self.warehouse.main_stock,
            "aux_stock": self.warehouse.aux_stock
        }

    def end_of_quarter_summary(self, supplier_name):
        """
        Calculates and deducts end-of-quarter expenses, including fixed costs, technician wages,
        warehouse storage costs, and restocking costs. Updates the hatchery's cash balance accordingly
        and returns a detailed summary of all expenses.

        :param supplier_name: Name of the selected supplier for restocking costs.
        :return: Dictionary containing a detailed breakdown of expenses, total expenses, and remaining cash balance.
        """
        # Retrieve fixed quarterly cost from class attribute
        fixed_costs = Hatchery.FIXED_QUARTERLY_COST

        # Calculate technician wages for the quarter
        technician_wages = Technician.calculate_total_wages(self.technicians)

        # Get storage costs from the warehouse
        storage_cost_data = self.warehouse.get_storage_costs()
        storage_costs = sum(storage_cost_data[0].values()) + sum(storage_cost_data[1].values())  # Summing main and aux

        # Restock resources using the supplier and retrieve the cost
        restocking_data = self.warehouse.restock_to_full(supplier_name, self.cash_balance)
        restocking_costs = restocking_data

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




