from Technician import Technician
from Warehouse import Warehouse
from Fish import Fish
from Supplier import Supplier

"""
Author: Mishara Sapukotanage
Section: Data Science
Description: This file contains the Hatchery class, which represents the main operations 
of the fish hatchery. It handles technician management, fish sales, resource management, 
and overall cash flow. The Hatchery class interacts with other classes such as Warehouse, 
Technician, Fish, and Supplier to simulate the hatchery's operations.
"""


class Hatchery:
    """
    The Hatchery class represents the main operations of the fish hatchery, including
    managing technicians, selling fish, and maintaining resources and cash flow.

    Attributes:
        CUSTOMER_DEMAND (dict): Static data about customer demand and prices for fish species.
        FIXED_QUARTERLY_COST (int): Fixed cost incurred by the hatchery each quarter.
        cash_balance (float): Current cash balance of the hatchery.
        technicians (list): List of Technician objects employed by the hatchery.
        warehouse (Warehouse): Instance of the Warehouse class to manage resources.
        available_labor (float): Tracks available labor hours for the quarter.
    """
    # Static data related to customer demand and fixed quarterly costs
    CUSTOMER_DEMAND = {
        "Clef Fins": {"demand": 25, "price": 250},
        "Timpani Snapper": {"demand": 10, "price": 350},
        "Andalusian Brim": {"demand": 15, "price": 250},
        "Plagal Cod": {"demand": 20, "price": 400},
        "Fugue Flounder": {"demand": 30, "price": 550},
        "Modal Bass": {"demand": 50, "price": 500}
    }
    FIXED_QUARTERLY_COST = 1500  # Fixed cost for each quarter

    def __init__(self):
        """
        Initialize the Hatchery class with a starting cash balance, empty list of technicians,
        and a Warehouse instance. Labor availability is set to 0 initially.
        """
        # Initial cash balance for the hatchery
        self.cash_balance = 10000

        # Initialize an empty list to hold Technician objects
        self.technicians = []

        # Create an instance of the Warehouse class for resource management
        self.warehouse = Warehouse()

        # Track available labor hours (updated at the start of each quarter)
        self.available_labor = 0

    def start_new_quarter(self):
        """
        Reset available labor based on the number of technicians at the start of each quarter.
        Calculates labor using the Technician class's static method.
        """
        # Calculate total labor hours based on the number of employed technicians
        self.available_labor = Technician.calculate_total_labour(len(self.technicians))

    @classmethod
    def get_demand_and_price(cls, fish_type):
        """
        Retrieve the demand and price for a specific fish type.

        Args:
            fish_type (str): Name of the fish species.

        Returns:
            dict: Dictionary containing 'demand' and 'price' for the specified fish,
            or None if the fish type is not found.
        """
        # Look up demand and price for the given fish type in CUSTOMER_DEMAND
        return cls.CUSTOMER_DEMAND.get(fish_type, None)

    @classmethod
    def get_fixed_cost(cls):
        """
        Retrieve the fixed quarterly cost for the hatchery.

        Returns:
            int: Fixed cost incurred each quarter.
        """
        # Return the predefined fixed cost
        return cls.FIXED_QUARTERLY_COST

    def get_cash_balance(self):
        """
        Retrieve the current cash balance of the hatchery.

        Returns:
            float: Current cash balance.
        """
        # Return the current cash balance
        return self.cash_balance

    def add_technicians(self, technician_details):
        """
        Add new technicians to the hatchery based on the provided details. Ensures
        the total number of technicians does not exceed the maximum allowed.

        Args:
            technician_details (list of tuples): Each tuple contains the technician's
            name and an optional specialization.

        Returns:
            list: List of successfully added technician names.
        """
        # Initialize a list to track the names of hired technicians
        hired_technicians = []

        # Loop through the provided technician details
        for name, specialization in technician_details:
            # Ensure the total technicians don't exceed the maximum limit
            if len(self.technicians) < Technician.MAX_TECHNICIANS:
                # Create a new Technician object and add it to the list
                new_technician = Technician(name, specialization)
                self.technicians.append(new_technician)
                hired_technicians.append(name)
            else:
                break  # Stop adding technicians if the limit is reached

        # Return the list of hired technician names
        return hired_technicians

    def remove_technicians(self, num_to_remove):
        """
        Remove technicians from the hatchery. Ensures the total number of technicians
        does not fall below the minimum allowed.

        Args:
            num_to_remove (int): Number of technicians to remove.

        Returns:
            list: List of removed technician names.
        """
        # Initialize a list to track the names of removed technicians
        removed_technicians = []

        # Loop through the number of technicians to remove
        for _ in range(num_to_remove):
            # Ensure the total technicians don't fall below the minimum limit
            if len(self.technicians) > Technician.MIN_TECHNICIANS:
                # Remove the last technician in the list and store their name
                removed_technician = self.technicians.pop()
                removed_technicians.append(removed_technician.name)
            else:
                break  # Stop removing technicians if the minimum limit is reached

        # Return the list of removed technician names
        return removed_technicians

    def sell_fish(self, fish_type, requested_quantity):
        """
        Attempt to sell a specified quantity of a fish type, considering labor and resource
        constraints.

        Args:
            fish_type (str): Type of fish to sell.
            requested_quantity (int): Quantity of fish to sell.

        Returns:
            dict: Dictionary containing the result of the sale, including status, quantity sold,
            revenue, and errors if any.
        """
        # Retrieve demand and price details for the specified fish type
        demand_data = self.CUSTOMER_DEMAND.get(fish_type)
        if not demand_data:
            # Return an error if the fish type is not available for sale
            return {"status": "error", "message": f"{fish_type} is not available for sale."}

        demand = demand_data["demand"]  # Maximum demand for the fish type
        price = demand_data["price"]  # Price per unit of the fish type

        # Exit early if no quantity is requested
        if requested_quantity == 0:
            return {"status": "skipped", "fish_type": fish_type}

        # Determine the quantity to sell based on requested quantity and demand
        sell_quantity = min(requested_quantity, demand)

        # Calculate the total maintenance time required for selling the specified quantity
        base_maintenance_time = Fish.calculate_total_maintenance_time(fish_type, sell_quantity)

        # Split technicians into two groups: specialized and regular
        specialized_technicians = [
            technician for technician in self.technicians if technician.is_specialised_for(fish_type)
        ]
        regular_technicians = [
            technician for technician in self.technicians if not technician.is_specialised_for(fish_type)
        ]

        # Calculate total labor available for specialized technicians
        specialized_labor_available = len(specialized_technicians) * Technician.LABOUR_PER_QUARTER
        # Convert specialized labor into equivalent time using a 3:2 ratio for efficiency
        equivalent_specialized_time = specialized_labor_available * (3 / 2)
        # Determine the maximum quantity of fish that can be handled by specialized technicians
        max_specialized_quantity = equivalent_specialized_time / (base_maintenance_time / sell_quantity)

        # Calculate the actual maintenance time based on labor availability
        if max_specialized_quantity >= sell_quantity:
            # If specialized technicians can handle all the fish, apply the efficiency factor
            actual_maintenance_time = base_maintenance_time * (2 / 3)
        else:
            # Split the work between specialized and regular technicians
            specialized_maintenance_time = max_specialized_quantity * (base_maintenance_time / sell_quantity) * (2 / 3)
            remaining_quantity = sell_quantity - max_specialized_quantity
            regular_maintenance_time = remaining_quantity * (base_maintenance_time / sell_quantity)
            actual_maintenance_time = specialized_maintenance_time + regular_maintenance_time

        # Check if there is sufficient labor available
        labor_issue = self.available_labor < actual_maintenance_time

        # Check if there are sufficient resources available
        resource_needs = Fish.calculate_resource_needs(fish_type, sell_quantity)
        insufficient_resources = {}
        for resource, amount_needed in resource_needs.items():
            # Calculate the total available stock for the resource
            available_amount = self.warehouse.main_stock.get(resource, 0) + self.warehouse.aux_stock.get(resource, 0)
            if available_amount < amount_needed:
                # Record the shortage details if resources are insufficient
                insufficient_resources[resource] = {
                    "needed": amount_needed,
                    "available": available_amount
                }

        # Return an appropriate status if there are labor or resource shortages
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

        # Deduct the required labor and resources
        self.available_labor -= actual_maintenance_time
        for resource, amount_needed in resource_needs.items():
            self.warehouse.check_and_deduct_resources(resource, amount_needed)

        # Calculate revenue and update the cash balance
        revenue = sell_quantity * price
        self.cash_balance += revenue

        # Return success details
        return {
            "status": "success",
            "fish_type": fish_type,
            "sell_quantity": sell_quantity,
            "revenue": revenue
        }

    def pay_technicians(self):
        """
        Pay all technicians their quarterly wages and update the cash balance.

        Returns:
            dict: Contains total payment and payment details for each technician.
        """
        # Calculate the total wages for all technicians
        total_payment = Technician.calculate_total_wages(self.technicians)

        # Generate payment details for each technician
        payments = []
        for technician in self.technicians:
            payments.append({"name": technician.name, "amount": technician.get_wage()})

        # Deduct the total payment from the cash balance
        self.cash_balance -= total_payment

        # Return payment details
        return {"total_payment": total_payment, "individual_payments": payments}

    def calculate_storage_costs(self):
        """
        Calculate storage costs for both main and auxiliary warehouses.

        Returns:
            dict: Detailed costs per resource and total storage cost.
        """
        # Retrieve storage costs for main and auxiliary warehouses
        main_costs, aux_costs = self.warehouse.get_storage_costs()

        # Calculate total costs for main and auxiliary warehouses
        total_main_cost = sum(main_costs.values())
        total_aux_cost = sum(aux_costs.values())
        total_storage_cost = total_main_cost + total_aux_cost

        # Return detailed storage costs
        return {
            "total_storage_cost": total_storage_cost,
            "main_costs": main_costs,
            "aux_costs": aux_costs
        }

    def restock_resources(self, vendor_name):
        """
        Restock resources using the selected vendor and deduct the cost from the cash balance.

        Args:
            vendor_name (str): Name of the vendor to purchase resources from.

        Returns:
            dict: Contains the restock status, total cost, and updated stock levels.
        """
        # Attempt to restock resources using the specified vendor
        restock_result = self.warehouse.restock_to_full(vendor_name, self.cash_balance)

        if restock_result.get("status") == "bankrupt":
            # If funds are insufficient, update the cash balance and return bankruptcy details
            self.cash_balance = restock_result["available_cash"]
            return {
                "status": "bankrupt",
                "warehouse": restock_result["warehouse"],
                "resource": restock_result["resource"],
                "needed": restock_result["needed"],
                "available_cash": self.cash_balance
            }
        else:
            # Deduct the total restocking cost from the cash balance
            total_restock_cost = restock_result["total_cost"]
            self.cash_balance -= total_restock_cost

            # Return success details including updated stock levels
            return {
                "status": "success",
                "total_restock_cost": total_restock_cost,
                "available_cash": self.cash_balance,
                "main_stock": self.warehouse.main_stock,
                "aux_stock": self.warehouse.aux_stock
            }

