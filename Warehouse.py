class Warehouse:
    # Static data for warehouse capacities, depreciation rates, and costs
    CAPACITIES = {
        "fertiliser": {"main": 20, "aux": 10},  # litres
        "feed": {"main": 400, "aux": 200},  # kg
        "salt": {"main": 200, "aux": 100}  # kg
    }

    DEPRECIATION_RATES = {
        "fertiliser": 0.4,  # per quarter
        "feed": 0.1,
        "salt": 0.0
    }

    COSTS = {
        "fertiliser": 0.10,  # cost per litre
        "feed": 0.001,  # cost per gram (1 kg = £1)
        "salt": 0.001  # cost per gram
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
        Deduct resources if available, otherwise log "Insufficient ingredients" message.
        :param resource: Type of resource (e.g., 'fertiliser').
        :param amount_required: Quantity needed.
        :return: True if resources were deducted, False if insufficient resources.
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
            # Log insufficient resources
            needed_amount = amount_required - total_available
            print(f"Insufficient ingredients: {resource} need {needed_amount}, storage {total_available}")
            return False

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
        """
        Restock main and auxiliary warehouses to full capacity if enough cash is available.
        :param supplier_name: Name of the supplier (e.g., "Slippery Lakes").
        :param available_cash: Total cash available for restocking.
        :return: Total cost of restocking, or amount actually spent if cash is insufficient.
        """
        total_cost = 0

        for resource in self.main_stock:
            # Calculate amount needed to reach full capacity
            required_main = Warehouse.CAPACITIES[resource]["main"] - self.main_stock[resource]
            required_aux = Warehouse.CAPACITIES[resource]["aux"] - self.aux_stock[resource]
            total_required = required_main + required_aux

            # Get the price per unit from the supplier
            price_per_unit = Supplier.get_price(supplier_name, resource)
            if price_per_unit is None:
                continue  # Skip if no valid price is available

            # Calculate total cost for restocking
            total_cost_for_resource = total_required * price_per_unit

            # Attempt full restock if funds allow, prioritize Main
            if available_cash >= total_cost + total_cost_for_resource:
                self.main_stock[resource] = Warehouse.CAPACITIES[resource]["main"]
                self.aux_stock[resource] = Warehouse.CAPACITIES[resource]["aux"]
                total_cost += total_cost_for_resource
                available_cash -= total_cost_for_resource
            else:
                # Restock partially based on remaining cash
                affordable_amount = int(available_cash // price_per_unit)
                restock_main = min(affordable_amount, required_main)
                self.main_stock[resource] += restock_main
                affordable_amount -= restock_main

                restock_aux = min(affordable_amount, required_aux)
                self.aux_stock[resource] += restock_aux

                total_cost += (restock_main + restock_aux) * price_per_unit
                break  # Exit restocking once cash is exhausted

        return total_cost
