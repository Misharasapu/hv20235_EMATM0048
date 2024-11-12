class Warehouse:
    # Static data for main and auxiliary warehouse capacities, depreciation rates, and costs
    CAPACITIES = {
        "fertiliser": {"main": 20, "aux": 10},  # litres
        "feed": {"main": 400, "aux": 200},      # kg
        "salt": {"main": 200, "aux": 100}       # kg
    }

    DEPRECIATION_RATES = {
        "fertiliser": 0.4,  # per quarter
        "feed": 0.1,
        "salt": 0.0
    }

    COSTS = {
        "fertiliser": 0.10,  # cost per litre
        "feed": 0.001,       # cost per gram (1 kg = £1)
        "salt": 0.001        # cost per gram
    }

    def __init__(self):
        # Initialize main and auxiliary stock to full capacity
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
            # Calculate depreciation for main warehouse stock
            depreciation_rate = Warehouse.DEPRECIATION_RATES.get(resource, 0)
            depreciated_amount_main = self.main_stock[resource] * (1 - depreciation_rate)
            self.main_stock[resource] = max(0, round(depreciated_amount_main))

            # Calculate depreciation for auxiliary warehouse stock
            depreciated_amount_aux = self.aux_stock[resource] * (1 - depreciation_rate)
            self.aux_stock[resource] = max(0, round(depreciated_amount_aux))

        return self.main_stock, self.aux_stock

    def get_storage_costs(self):
        """Calculate and return the storage costs for both main and auxiliary warehouses."""
        main_cost = 0
        aux_cost = 0

        # Calculate costs for the main warehouse
        for resource, amount in self.main_stock.items():
            unit_cost = Warehouse.COSTS.get(resource, 0)
            main_cost += unit_cost * amount

        # Calculate costs for the auxiliary warehouse
        for resource, amount in self.aux_stock.items():
            unit_cost = Warehouse.COSTS.get(resource, 0)
            aux_cost += unit_cost * amount

        # Store the costs in attributes
        self.storage_costs_main = main_cost
        self.storage_costs_aux = aux_cost

        return main_cost, aux_cost

    def check_stock(self, resource, required_amount):
        """
        Check if there's sufficient stock of a given resource across both warehouses.
        :param resource: Type of resource to check (e.g., 'fertiliser').
        :param required_amount: Amount needed for the operation.
        :return: True if enough stock is available, False otherwise.
        """
        total_stock = self.main_stock.get(resource, 0) + self.aux_stock.get(resource, 0)
        return total_stock >= required_amount

    def deduct_stock(self, resource, amount):
        """
        Deduct a specific amount of a resource from stock, prioritizing the main warehouse.
        :param resource: Type of resource (e.g., 'fertiliser').
        :param amount: Quantity to deduct.
        :return: Remaining amount after deduction for verification.
        """
        if resource in self.main_stock:
            # Deduct from main stock first
            main_available = self.main_stock[resource]
            if main_available >= amount:
                self.main_stock[resource] -= amount
                amount = 0
            else:
                # Deduct whatever is left from auxiliary if main doesn't have enough
                self.main_stock[resource] = 0
                amount -= main_available
                self.aux_stock[resource] = max(0, self.aux_stock[resource] - amount)

        return self.main_stock[resource] + self.aux_stock[resource]  # Total remaining for verification

    def restock(self, supplier_name, resource, amount):
        """
        Restock a specified resource using a supplier's price, prioritizing the main warehouse.
        :param supplier_name: Name of the supplier (e.g., "Slippery Lakes").
        :param resource: Type of resource to restock (e.g., 'fertiliser').
        :param amount: Quantity to add to the stock.
        :return: Total cost of restocking.
        """
        price_per_unit = Supplier.get_price(supplier_name, resource)

        if price_per_unit is not None:
            total_cost = price_per_unit * amount

            # Determine maximum capacities for main and auxiliary
            max_main = Warehouse.CAPACITIES[resource]["main"]
            max_aux = Warehouse.CAPACITIES[resource]["aux"]

            # Restock main stock first
            available_space_main = max_main - self.main_stock[resource]
            if amount <= available_space_main:
                self.main_stock[resource] += amount
            else:
                # Fill main stock to capacity and put the remainder in aux stock
                self.main_stock[resource] = max_main
                remaining_amount = amount - available_space_main
                self.aux_stock[resource] = min(max_aux, self.aux_stock[resource] + remaining_amount)

            return total_cost
        else:
            # Return 0 if no valid price is available
            return 0
