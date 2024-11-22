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

    def add_technicians(self, technician_details):
        """
        Add new technicians to the hatchery based on provided details.
        Ensures total number of technicians does not exceed the maximum limit.

        :param technician_details: List of tuples with technician names and optional specializations.
        :return: List of successfully added technician names.
        """
        hired_technicians = []
        for name, specialization in technician_details:
            if len(self.technicians) < Technician.MAX_TECHNICIANS:
                new_technician = Technician(name, specialization)
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
        """
        Sell a specified quantity of a fish type, prioritizing specialized technicians.
        :param fish_type: Type of fish to sell.
        :param requested_quantity: Quantity of fish to sell.
        :return: Result dictionary with sale status and details.
        """
        demand_data = self.CUSTOMER_DEMAND.get(fish_type)
        if not demand_data:
            return {"status": "error", "message": f"{fish_type} is not available for sale."}

        demand = demand_data["demand"]
        price = demand_data["price"]

        # Exit early if sell_quantity is 0 to skip this fish type without errors
        if requested_quantity == 0:
            return {"status": "skipped", "fish_type": fish_type}

        sell_quantity = min(requested_quantity, demand)

        # Calculate total maintenance time for the requested sale
        base_maintenance_time = Fish.calculate_total_maintenance_time(fish_type, sell_quantity)

        # Split technicians into specialized and regular groups
        specialized_technicians = [
            technician for technician in self.technicians if technician.is_specialised_for(fish_type)
        ]
        regular_technicians = [
            technician for technician in self.technicians if not technician.is_specialised_for(fish_type)
        ]

        # Calculate how much specialized labor can handle
        specialized_labor_available = len(specialized_technicians) * Technician.LABOUR_PER_QUARTER
        equivalent_specialized_time = specialized_labor_available * (3 / 2)  # Convert specialized labor to equivalent time
        max_specialized_quantity = equivalent_specialized_time / (base_maintenance_time / sell_quantity)

        if max_specialized_quantity >= sell_quantity:
            # Specialized technicians can handle the entire sale
            actual_maintenance_time = base_maintenance_time * (2 / 3)
        else:
            # Specialized technicians handle part of the sale
            specialized_maintenance_time = max_specialized_quantity * (base_maintenance_time / sell_quantity) * (2 / 3)
            remaining_quantity = sell_quantity - max_specialized_quantity
            regular_maintenance_time = remaining_quantity * (base_maintenance_time / sell_quantity)
            actual_maintenance_time = specialized_maintenance_time + regular_maintenance_time

        # Check labor constraint
        labor_issue = self.available_labor < actual_maintenance_time

        # Resource check and deduction
        resource_needs = Fish.calculate_resource_needs(fish_type, sell_quantity)
        insufficient_resources = {}
        for resource, amount_needed in resource_needs.items():
            available_amount = self.warehouse.main_stock.get(resource, 0) + self.warehouse.aux_stock.get(resource, 0)
            if available_amount < amount_needed:
                insufficient_resources[resource] = {
                    "needed": amount_needed,
                    "available": available_amount
                }

        # Determine return status based on labor and resources
        if labor_issue and insufficient_resources:
            return {
                "status": "insufficient_labor_and_resources",
                "required_labor": actual_maintenance_time,
                "available_labor": self.available_labor,
                "resources": insufficient_resources
            }
        elif labor_issue:
            return {
                "status": "insufficient_labor",
                "required_labor": actual_maintenance_time,
                "available_labor": self.available_labor
            }
        elif insufficient_resources:
            return {
                "status": "insufficient_resources",
                "resources": insufficient_resources
            }

        # Deduct labor
        self.available_labor -= actual_maintenance_time

        # Deduct resources
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

        total_main_cost = sum(main_costs.values())
        total_aux_cost = sum(aux_costs.values())

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

        if restock_result.get("status") == "bankrupt":
            self.cash_balance = restock_result["available_cash"]
            return {
                "status": "bankrupt",
                "warehouse": restock_result["warehouse"],
                "resource": restock_result["resource"],
                "needed": restock_result["needed"],
                "available_cash": self.cash_balance
            }
        else:
            total_restock_cost = restock_result["total_cost"]
            self.cash_balance -= total_restock_cost
            return {
                "status": "success",
                "total_restock_cost": total_restock_cost,
                "available_cash": self.cash_balance,
                "main_stock": self.warehouse.main_stock,
                "aux_stock": self.warehouse.aux_stock
            }
