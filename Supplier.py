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

