
from Supplier import Supplier

class Warehouse:
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
        """Apply depreciation to each resource in both main and auxiliary stocks."""
        for resource in self.main_stock:
            # Calculate depreciation for main stock
            depreciation_rate = Warehouse.DEPRECIATION_RATES.get(resource, 0)
            depreciated_amount_main = self.main_stock[resource] * (1 - depreciation_rate)
            self.main_stock[resource] = max(0, round(depreciated_amount_main))

            # Calculate depreciation for auxiliary stock
            depreciated_amount_aux = self.aux_stock[resource] * (1 - depreciation_rate)
            self.aux_stock[resource] = max(0, round(depreciated_amount_aux))

        return self.main_stock, self.aux_stock

    def check_and_deduct_resources(self, resource, amount_required):
        """
        Check if there are sufficient resources in both main and auxiliary stocks for a given resource.
        Deduct resources if available, otherwise return details about the shortage.

        :param resource: Type of resource (e.g., 'fertiliser').
        :param amount_required: Quantity needed.
        :return: True if resources were deducted, or a dictionary with 'status': 'insufficient' and shortage details if not.
        """
        total_available = self.main_stock.get(resource, 0) + self.aux_stock.get(resource, 0)

        if total_available >= amount_required:
            # Deduct from main stock first
            if self.main_stock[resource] >= amount_required:
                self.main_stock[resource] -= amount_required
            else:
                # Use auxiliary stock if main is insufficient
                amount_needed_from_aux = amount_required - self.main_stock[resource]
                self.main_stock[resource] = 0
                self.aux_stock[resource] = max(0, self.aux_stock[resource] - amount_needed_from_aux)
            return True
        else:
            # Return shortage information instead of printing it
            needed_amount = amount_required - total_available
            return {
                "status": "insufficient",
                "resource": resource,
                "needed": needed_amount,
                "available": total_available
            }

    def get_storage_costs(self):
        """Calculate and return detailed storage costs for both main and auxiliary warehouses."""
        main_cost = {}
        aux_cost = {}

        for resource, amount in self.main_stock.items():
            unit_cost = Warehouse.COSTS.get(resource, 0)
            main_cost[resource] = unit_cost * amount

        for resource, amount in self.aux_stock.items():
            unit_cost = Warehouse.COSTS.get(resource, 0)
            aux_cost[resource] = unit_cost * amount

        return main_cost, aux_cost

    def restock_to_full(self, supplier_name, available_cash):
        total_cost = 0  # Initialize total cost of restocking

        for resource in self.main_stock:
            # Retrieve the supplier-specific price per unit of the resource
            price_per_unit = Supplier.get_price(supplier_name, resource)

            if price_per_unit is None:
                continue  # Skip if the supplier does not provide a price for this resource

            # Calculate the amounts needed to restock
            main_restock_amount = Warehouse.CAPACITIES[resource]["main"] - self.main_stock[resource]
            aux_restock_amount = Warehouse.CAPACITIES[resource]["aux"] - self.aux_stock[resource]

            # Calculate the cost to fully restock main and auxiliary warehouses for this resource
            cost_main = price_per_unit * main_restock_amount
            cost_aux = price_per_unit * aux_restock_amount

            # Attempt to restock the main warehouse first
            if available_cash >= cost_main:
                self.main_stock[resource] = Warehouse.CAPACITIES[resource]["main"]  # Restock to full capacity
                total_cost += cost_main
                available_cash -= cost_main
            else:
                # Bankruptcy occurs in the main warehouse; insufficient funds for full restock
                needed_amount = cost_main - available_cash
                return {
                    "status": "bankrupt",
                    "warehouse": "main",
                    "resource": resource,
                    "needed": cost_main,
                    "available_cash": available_cash
                }

            # Attempt to restock the auxiliary warehouse
            if available_cash >= cost_aux:
                self.aux_stock[resource] = Warehouse.CAPACITIES[resource]["aux"]  # Restock to full capacity
                total_cost += cost_aux
                available_cash -= cost_aux
            else:
                # Bankruptcy occurs in the auxiliary warehouse; insufficient funds for full restock
                needed_amount = cost_aux - available_cash
                return {
                    "status": "bankrupt",
                    "warehouse": "auxiliary",
                    "resource": resource,
                    "needed": cost_aux,
                    "available_cash": available_cash
                }

        # If restocking was successful for all resources, return success
        return {
            "status": "success",
            "total_cost": total_cost,
            "available_cash": available_cash
        }






