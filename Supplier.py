class Supplier:
    # Static pricing information as class-level dictionary
    PRICES = {
        "Slippery Lakes": {
            "fertiliser": 0.30,  # per litre
            "feed": 0.10,  # per gram
            "salt": 0.05  # per gram
        },
        "Scaly Wholesaler": {
            "fertiliser": 0.20,  # per litre
            "feed": 0.40,  # per gram
            "salt": 0.25  # per gram
        }
    }

    @classmethod
    def get_price(cls, supplier_name, supply_type):
        """
        Retrieve the price for a specific supplier and supply type.

        :param supplier_name: Name of the supplier (e.g., "Slippery Lakes").
        :param supply_type: Type of supply (e.g., "fertiliser", "feed", or "salt").
        :return: Price per unit for the specified supply type from the specified supplier.
        """
        return cls.PRICES.get(supplier_name, {}).get(supply_type, None)

    @classmethod
    def list_suppliers(cls):
        """
        List all available suppliers with indices for selection in the console.
        :return: A formatted string listing suppliers by index.
        """
        suppliers = [f"{index + 1}. {supplier}" for index, supplier in enumerate(cls.PRICES.keys())]
        return "\n".join(suppliers)


