class Warehouse:
    # Static data for warehouse capacities, depreciation rates, and costs
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

    @classmethod
    def get_total_capacity(cls):
        """Calculate total capacity (main + aux) for each resource."""
        return {
            "fertiliser": cls.CAPACITIES["fertiliser"]["main"] + cls.CAPACITIES["fertiliser"]["aux"],
            "feed": cls.CAPACITIES["feed"]["main"] + cls.CAPACITIES["feed"]["aux"],
            "salt": cls.CAPACITIES["salt"]["main"] + cls.CAPACITIES["salt"]["aux"]
        }

    @classmethod
    def display_warehouse_info(cls):
        """Display information about capacities, depreciation rates, and costs."""
        capacities = cls.get_total_capacity()
        return (f"Capacities - Fertiliser: {capacities['fertiliser']} litres, "
                f"Feed: {capacities['feed']} kg, Salt: {capacities['salt']} kg\n"
                f"Depreciation Rates - Fertiliser: {cls.DEPRECIATION_RATES['fertiliser']} per quarter, "
                f"Feed: {cls.DEPRECIATION_RATES['feed']} per quarter, "
                f"Salt: {cls.DEPRECIATION_RATES['salt']} per quarter\n"
                f"Warehouse Costs - Fertiliser: £{cls.COSTS['fertiliser']} per litre, "
                f"Feed: £{cls.COSTS['feed']} per gram, Salt: £{cls.COSTS['salt']} per gram")

    def __init__(self):
        # Initialize stock to full capacity using get_total_capacity
        self.current_stock = Warehouse.get_total_capacity()
        self.storage_costs = 0  # Optional, to track quarterly storage costs

    def calculate_depreciation(self):
        """Apply depreciation to each resource in stock based on its rate."""
        for resource, amount in self.current_stock.items():
            # Retrieve the depreciation rate for the resource (0 if not defined)
            depreciation_rate = Warehouse.DEPRECIATION_RATES.get(resource, 0)

            # Apply depreciation by reducing the stock amount
            # For example, if 100 kg of feed is in stock and depreciation is 10%, it will become 90 kg
            depreciated_amount = amount * (1 - depreciation_rate)

            # Round up to the nearest integer, as specified in the brief
            self.current_stock[resource] = max(0, round(depreciated_amount))

        return self.current_stock

    def get_storage_costs(self):
        """Calculate and return the total storage cost based on the current stock."""
        total_cost = 0  # Initialize the total cost to zero

        # Loop through each resource type in the current stock
        for resource, amount in self.current_stock.items():
            # Retrieve the cost per unit of storage for the resource (e.g., £0.10 per litre of fertiliser)
            unit_cost = Warehouse.COSTS.get(resource, 0)

            # Calculate the cost for the current stock of this resource and add to total cost
            # For example, if we have 10 litres of fertiliser and the cost is £0.10 per litre, the cost is 10 * 0.10 = £1.00
            total_cost += unit_cost * amount

        # Update the storage costs attribute with the calculated total
        self.storage_costs = total_cost

        return total_cost  # Return the total cost for use elsewhere in the program

    def check_stock(self, resource, required_amount):
        """
        Check if there's sufficient stock of a given resource.
        :param resource: Type of resource to check (e.g., 'fertiliser').
        :param required_amount: Amount needed for the operation.
        :return: True if enough stock is available, False otherwise.
        """
        # Check if the resource exists in current stock and if the stock is sufficient
        return self.current_stock.get(resource, 0) >= required_amount

    def deduct_stock(self, resource, amount):
        """
        Deduct a specific amount of a resource from stock.
        :param resource: Type of resource (e.g., 'fertiliser').
        :param amount: Quantity to deduct.
        :return: Updated stock amount for the resource.
        """
        # Ensure that the resource exists in current stock
        if resource in self.current_stock:
            # Deduct the specified amount and ensure stock doesn't go negative
            self.current_stock[resource] = max(0, self.current_stock[resource] - amount)

        return self.current_stock[resource]  # Return the updated amount for verification

    def restock(self, supplier_name, resource, amount):
        """
        Restocks a specified resource using a supplier's price.
        :param supplier_name: Name of the supplier (e.g., "Slippery Lakes").
        :param resource: Type of resource to restock (e.g., 'fertiliser').
        :param amount: Quantity to add to the stock.
        :return: Total cost of restocking.
        """
        # Call Supplier.get_price directly using the supplier name and resource type
        price_per_unit = Supplier.get_price(supplier_name, resource)

        if price_per_unit is not None:
            # Calculate the total cost of the restock
            total_cost = price_per_unit * amount

            # Determine the maximum capacity for the resource
            max_capacity = Warehouse.get_total_capacity()[resource]

            # Update current stock, ensuring it doesn't exceed maximum capacity
            self.current_stock[resource] = min(max_capacity, self.current_stock[resource] + amount)

            return total_cost  # Return the total restocking cost for use in financial calculations
        else:
            # If there's no valid price, return 0 as the cost
            return 0

