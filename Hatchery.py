
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
        self.cash_balance = 10000  # Starting cash balance for the hatchery
        self.technicians = []
        self.warehouse = Warehouse()
        self.available_labor = 0  # New attribute to track labor per quarter

    def start_new_quarter(self):
        """Reset available labor based on the number of technicians at the start of each quarter."""
        self.available_labor = Technician.calculate_total_labour(len(self.technicians))
        print(f"Starting new quarter with {self.available_labor} weeks of available labor.")

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
        hired_technicians = []
        for name in technician_names:
            if len(self.technicians) < Technician.MAX_TECHNICIANS:
                new_technician = Technician(name)
                self.technicians.append(new_technician)
                hired_technicians.append(name)
            else:
                break  # Stop adding if we reach the max limit

        return hired_technicians

    def remove_technicians(self, num_to_remove):
        """
        Remove technicians from the hatchery. Ensures the total number of technicians does not fall below the minimum limit.

        :param num_to_remove: Number of technicians to remove.
        :return: List of removed technician names for potential verification/testing.
        """
        removed_technicians = []

        for _ in range(num_to_remove):
            if len(self.technicians) > Technician.MIN_TECHNICIANS:
                removed_technician = self.technicians.pop()
                removed_technicians.append(removed_technician.name)
            else:
                break  # Stop removing if we reach the min limit

        return removed_technicians

    def sell_fish(self, fish_type, requested_quantity):
        demand_data = self.CUSTOMER_DEMAND.get(fish_type)
        if not demand_data:
            return {"status": "error", "message": f"{fish_type} is not available for sale."}

        demand = demand_data["demand"]
        price = demand_data["price"]
        sell_quantity = min(requested_quantity, demand)

        # Calculate maintenance time for the requested sale
        maintenance_time = Fish.calculate_total_maintenance_time(fish_type, sell_quantity)

        # Check labor constraint
        labor_issue = self.available_labor < maintenance_time
        insufficient_resources = {}

        # Resource check and deduction
        resource_needs = Fish.calculate_resource_needs(fish_type, sell_quantity)
        for resource, amount_needed in resource_needs.items():
            available_amount = self.warehouse.main_stock.get(resource, 0) + self.warehouse.aux_stock.get(resource, 0)
            if available_amount < amount_needed:
                insufficient_resources[resource] = {
                    "needed": amount_needed,
                    "available": available_amount
                }

        # Determine return status based on labor and resources
        if labor_issue and insufficient_resources:
            # Both labor and resources are insufficient
            return {
                "status": "insufficient_labor_and_resources",
                "required_labor": maintenance_time,
                "available_labor": self.available_labor,
                "resources": insufficient_resources
            }
        elif labor_issue:
            # Only labor is insufficient
            return {
                "status": "insufficient_labor",
                "required_labor": maintenance_time,
                "available_labor": self.available_labor
            }
        elif insufficient_resources:
            # Only resources are insufficient
            return {
                "status": "insufficient_resources",
                "resources": insufficient_resources
            }

        # Deduct labor and resources if both are sufficient
        self.available_labor -= maintenance_time
        print(
            f"Deducted {maintenance_time} weeks of labor for {sell_quantity} of {fish_type}. Remaining labor: {self.available_labor}")

        for resource, amount_needed in resource_needs.items():
            self.warehouse.check_and_deduct_resources(resource, amount_needed)

        # Calculate revenue and update cash balance
        revenue = sell_quantity * price
        self.cash_balance += revenue

        return {
            "status": "success",
            "fish_type": fish_type,
            "sell_quantity": sell_quantity,
            "revenue": revenue
        }

    def pay_technicians(self):
        """
        Pays each technician based on their quarterly wage and updates the hatchery's cash balance.
        Returns a list of payment details for each technician without console output.

        :return: Total payment amount and a list of individual payment details.
        """
        total_payment = Technician.calculate_total_wages(self.technicians)
        payments = []
        for technician in self.technicians:
            payments.append({"name": technician.name, "amount": technician.get_wage()})

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

        # Calculate total storage costs using traditional loops
        total_main_cost = 0
        for cost in main_costs.values():
            total_main_cost += cost

        total_aux_cost = 0
        for cost in aux_costs.values():
            total_aux_cost += cost

        total_storage_cost = total_main_cost + total_aux_cost

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
        :return: Dictionary containing restock cost and updated stock levels, or bankruptcy status if funds are insufficient.
        """
        # Attempt to restock and receive the result
        restock_result = self.warehouse.restock_to_full(vendor_name, self.cash_balance)

        # Check if restocking was successful or led to bankruptcy
        if restock_result.get("status") == "bankrupt":
            # Update cash balance to reflect bankruptcy status
            self.cash_balance = restock_result["available_cash"]
            return {
                "status": "bankrupt",
                "warehouse": restock_result["warehouse"],
                "resource": restock_result["resource"],
                "needed": restock_result["needed"],
                "available_cash": self.cash_balance
            }
        else:
            # Deduct total restock cost from cash balance
            total_restock_cost = restock_result["total_cost"]
            self.cash_balance -= total_restock_cost
            return {
                "status": "success",
                "total_restock_cost": total_restock_cost,
                "available_cash": self.cash_balance,
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
        # Retrieve fixed quarterly cost directly from the class attribute
        fixed_costs = self.FIXED_QUARTERLY_COST

        # Calculate technician wages using existing pay_technicians method
        technician_payments = self.pay_technicians()
        technician_wages = technician_payments["total_payment"]

        # Calculate storage costs using the calculate_storage_costs method
        storage_cost_data = self.calculate_storage_costs()
        storage_costs = storage_cost_data["total_storage_cost"]

        # Perform restocking using the restock_to_full method
        restocking_data = self.warehouse.restock_to_full(supplier_name, self.cash_balance)
        restocking_costs = restocking_data["total_cost"]

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





