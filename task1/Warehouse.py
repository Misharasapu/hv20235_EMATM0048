"""
Author: Mishara Sapukotanage
Section: Data Science
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
        "fertiliser": {"main": 20000, "aux": 10000},  # Capacities in ml
        "feed": {"main": 400, "aux": 200},  # Capacities in kg
        "salt": {"main": 200, "aux": 100}  # Capacities in kg
    }

    DEPRECIATION_RATES = {
        "fertiliser": 0.4,  # 40% per quarter
        "feed": 0.1,  # 10% per quarter
        "salt": 0.0  # No depreciation
    }

    COSTS = {
        "fertiliser": 0.0001,  # Storage cost per ml
        "feed": 1,  # Storage cost per kg
        "salt": 1  # Storage cost per kg
    }

    def __init__(self):
        """
        Initialize the Warehouse with full stock capacities for both main and auxiliary warehouses.
        """
        # Set initial stock levels to the full capacity for the main warehouse
        self.main_stock = {
            "fertiliser": Warehouse.CAPACITIES["fertiliser"]["main"],
            "feed": Warehouse.CAPACITIES["feed"]["main"],
            "salt": Warehouse.CAPACITIES["salt"]["main"]
        }
        # Set initial stock levels to the full capacity for the auxiliary warehouse
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
            # Get the depreciation rate for the resource
            depreciation_rate = Warehouse.DEPRECIATION_RATES.get(resource, 0)

            # Apply depreciation to main stock
            depreciated_amount_main = self.main_stock[resource] * (1 - depreciation_rate)
            # Ensure stock does not go below zero
            self.main_stock[resource] = max(0, round(depreciated_amount_main))

            # Apply depreciation to auxiliary stock
            depreciated_amount_aux = self.aux_stock[resource] * (1 - depreciation_rate)
            # Ensure stock does not go below zero
            self.aux_stock[resource] = max(0, round(depreciated_amount_aux))

        # Return the updated stock levels
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
        # Calculate the total available stock (main + auxiliary)
        total_available = self.main_stock.get(resource, 0) + self.aux_stock.get(resource, 0)

        # Check if the total available stock is sufficient
        if total_available >= amount_required:
            # Deduct from the main stock first
            if self.main_stock[resource] >= amount_required:
                self.main_stock[resource] -= amount_required
            else:
                # Deduct the remainder from auxiliary stock if main stock is insufficient
                amount_needed_from_aux = amount_required - self.main_stock[resource]
                self.main_stock[resource] = 0  # Deplete main stock
                self.aux_stock[resource] = max(0, self.aux_stock[resource] - amount_needed_from_aux)
            return True
        else:
            # Return details of the shortage if resources are insufficient
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

        # Calculate storage cost for each resource in the main warehouse
        for resource, amount in self.main_stock.items():
            unit_cost = Warehouse.COSTS.get(resource, 0)
            main_cost[resource] = unit_cost * amount

        # Calculate storage cost for each resource in the auxiliary warehouse
        for resource, amount in self.aux_stock.items():
            unit_cost = Warehouse.COSTS.get(resource, 0)
            aux_cost[resource] = unit_cost * amount

        # Return the calculated costs for both warehouses
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
        total_cost = 0  # Track the total cost of restocking

        for resource in self.main_stock:
            # Retrieve the price per unit from the supplier
            price_per_unit = Supplier.get_price(supplier_name, resource)

            if price_per_unit is None:
                continue  # Skip resources not offered by the supplier

            # Calculate the amounts needed to restock both warehouses to full capacity
            main_restock_amount = Warehouse.CAPACITIES[resource]["main"] - self.main_stock[resource]
            aux_restock_amount = Warehouse.CAPACITIES[resource]["aux"] - self.aux_stock[resource]

            # Calculate the costs for restocking the main and auxiliary warehouses
            cost_main = price_per_unit * main_restock_amount
            cost_aux = price_per_unit * aux_restock_amount

            # Restock the main warehouse if funds are sufficient
            if available_cash >= cost_main:
                self.main_stock[resource] = Warehouse.CAPACITIES[resource]["main"]
                total_cost += cost_main
                available_cash -= cost_main
            else:
                # If funds are insufficient, return bankruptcy details
                needed_amount = cost_main - available_cash
                return {
                    "status": "bankrupt",
                    "warehouse": "main",
                    "resource": resource,
                    "needed": needed_amount,
                    "available_cash": available_cash
                }

            # Restock the auxiliary warehouse if funds are sufficient
            if available_cash >= cost_aux:
                self.aux_stock[resource] = Warehouse.CAPACITIES[resource]["aux"]
                total_cost += cost_aux
                available_cash -= cost_aux
            else:
                # If funds are insufficient, return bankruptcy details
                needed_amount = cost_aux - available_cash
                return {
                    "status": "bankrupt",
                    "warehouse": "auxiliary",
                    "resource": resource,
                    "needed": needed_amount,
                    "available_cash": available_cash
                }

        # Return success details if restocking was completed for all resources
        return {
            "status": "success",
            "total_cost": total_cost,
            "available_cash": available_cash
        }
