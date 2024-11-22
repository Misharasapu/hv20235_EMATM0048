"""
Author: [Your Name]
Section: [Your Section/Group]
Description: This file contains the Warehouse class, which manages stock levels,
depreciation, storage costs, and resource restocking for the hatchery. It interacts with
the Supplier class to handle pricing and ensures resource availability for operations.
"""

from Supplier import Supplier

class Warehouse:
    """
    The Warehouse class handles resource management, including maintaining stock levels,
    applying depreciation, calculating storage costs, and restocking resources.

    Attributes:
        CAPACITIES (dict): Static dictionary defining the maximum capacities for resources
        in both main and auxiliary warehouses.
        DEPRECIATION_RATES (dict): Static dictionary defining depreciation rates for each
        resource type.
        COSTS (dict): Static dictionary defining storage costs per unit for each resource.
        main_stock (dict): Current stock levels in the main warehouse.
        aux_stock (dict): Current stock levels in the auxiliary warehouse.
    """
    # Static data for warehouse capacities, depreciation rates, and costs
    CAPACITIES = {
        "fertiliser": {"main": 20000, "aux": 10000},  # Converted from litres to ml
        "feed": {"main": 400, "aux": 200},  # kg
        "salt": {"main": 200, "aux": 100}  # kg
    }

    DEPRECIATION_RATES = {
        "fertiliser": 0.4,  # per quarter
        "feed": 0.1,
        "salt": 0.0
    }

    COSTS = {
        "fertiliser": 0.0001,  # cost per ml
        "feed": 1,  # cost per kg
        "salt": 1  # cost per kg
    }

    def __init__(self):
        """
        Initialize the Warehouse with full stock capacities for both main and auxiliary warehouses.
        """
        # Initialize stock levels to full capacity for both main and auxiliary
        self.main_stock = {
            "fertiliser": Warehouse.CAPACITIES["fertiliser"]["main"],
            "feed": Warehouse.CAPACITIES["feed"]["main"],
            "salt": Warehouse.CAPACITIES["salt"]["main"]
        }
        self.aux_stock = {
            "fertiliser": Warehouse.CAPACITIES["fertiliser"]["aux"],
            "feed": Warehouse.CAPACITIES["feed"]["aux"],
            "salt": Warehouse.CAPACITIES["salt"]["aux"]
        }

    def calculate_depreciation(self):
        """
        Apply depreciation rates to each resource in both main and auxiliary stocks.

        Returns:
            tuple: Updated main and auxiliary stock levels after applying depreciation.
        """
        for resource in self.main_stock:
            # Apply depreciation to main stock
            depreciation_rate = Warehouse.DEPRECIATION_RATES.get(resource, 0)
            depreciated_amount_main = self.main_stock[resource] * (1 - depreciation_rate)
            self.main_stock[resource] = max(0, round(depreciated_amount_main))

            # Apply depreciation to auxiliary stock
            depreciated_amount_aux = self.aux_stock[resource] * (1 - depreciation_rate)
            self.aux_stock[resource] = max(0, round(depreciated_amount_aux))

        return self.main_stock, self.aux_stock

    def check_and_deduct_resources(self, resource, amount_required):
        """
        Check if sufficient resources are available and deduct them if possible.

        Args:
            resource (str): Type of resource (e.g., "fertiliser").
            amount_required (float): Quantity required.

        Returns:
            bool or dict: True if resources are deducted successfully. If insufficient,
            a dictionary with shortage details is returned.
        """
        total_available = self.main_stock.get(resource, 0) + self.aux_stock.get(resource, 0)

        if total_available >= amount_required:
            # Deduct from main stock first
            if self.main_stock[resource] >= amount_required:
                self.main_stock[resource] -= amount_required
            else:
                # Use auxiliary stock if main stock is insufficient
                amount_needed_from_aux = amount_required - self.main_stock[resource]
                self.main_stock[resource] = 0
                self.aux_stock[resource] = max(0, self.aux_stock[resource] - amount_needed_from_aux)
            return True
        else:
            # Return shortage details
            needed_amount = amount_required - total_available
            return {
                "status": "insufficient",
                "resource": resource,
                "needed": needed_amount,
                "available": total_available
            }

    def get_storage_costs(self):
        """
        Calculate storage costs for both main and auxiliary warehouses.

        Returns:
            tuple: Dictionaries containing detailed storage costs for main and auxiliary stocks.
        """
        main_cost = {}
        aux_cost = {}

        # Calculate costs for main stock
        for resource, amount in self.main_stock.items():
            unit_cost = Warehouse.COSTS.get(resource, 0)
            main_cost[resource] = unit_cost * amount

        # Calculate costs for auxiliary stock
        for resource, amount in self.aux_stock.items():
            unit_cost = Warehouse.COSTS.get(resource, 0)
            aux_cost[resource] = unit_cost * amount

        return main_cost, aux_cost

    def restock_to_full(self, supplier_name, available_cash):
        """
        Restock resources to full capacity for both main and auxiliary warehouses.

        Args:
            supplier_name (str): Name of the supplier.
            available_cash (float): Cash available for restocking.

        Returns:
            dict: Details of restocking status, cost, and updated cash balance. Returns
            bankruptcy details if insufficient funds are available.
        """
        total_cost = 0  # Initialize total restocking cost

        for resource in self.main_stock:
            # Retrieve supplier-specific price per unit
            price_per_unit = Supplier.get_price(supplier_name, resource)

            if price_per_unit is None:
                continue  # Skip if the supplier does not provide a price for this resource

            # Calculate amounts needed for restocking
            main_restock_amount = Warehouse.CAPACITIES[resource]["main"] - self.main_stock[resource]
            aux_restock_amount = Warehouse.CAPACITIES[resource]["aux"] - self.aux_stock[resource]

            # Calculate costs for main and auxiliary restocking
            cost_main = price_per_unit * main_restock_amount
            cost_aux = price_per_unit * aux_restock_amount

            # Attempt to restock main warehouse
            if available_cash >= cost_main:
                self.main_stock[resource] = Warehouse.CAPACITIES[resource]["main"]  # Restock to full
                total_cost += cost_main
                available_cash -= cost_main
            else:
                # Insufficient funds for main warehouse restock
                needed_amount = cost_main - available_cash
                return {
                    "status": "bankrupt",
                    "warehouse": "main",
                    "resource": resource,
                    "needed": needed_amount,
                    "available_cash": available_cash
                }

            # Attempt to restock auxiliary warehouse
            if available_cash >= cost_aux:
                self.aux_stock[resource] = Warehouse.CAPACITIES[resource]["aux"]  # Restock to full
                total_cost += cost_aux
                available_cash -= cost_aux
            else:
                # Insufficient funds for auxiliary warehouse restock
                needed_amount = cost_aux - available_cash
                return {
                    "status": "bankrupt",
                    "warehouse": "auxiliary",
                    "resource": resource,
                    "needed": needed_amount,
                    "available_cash": available_cash
                }

        # Successful restocking for all resources
        return {
            "status": "success",
            "total_cost": total_cost,
            "available_cash": available_cash
        }
