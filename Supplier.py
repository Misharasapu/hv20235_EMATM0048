class Supplier:
    # Static pricing information as class-level dictionary
    PRICES = {
        "Slippery Lakes": {
            "fertiliser": 0.0003,  # price per ml (converted from 0.30 per litre)
            "feed": 0.1,  # price per kg
            "salt": 0.05  # price per kg
        },
        "Scaly Wholesaler": {
            "fertiliser": 0.0002,  # price per ml (converted from 0.20 per litre)
            "feed": 0.4,  # price per kg
            "salt": 0.25  # price per kg
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
        # Initialize an empty list to store each supplier line
        supplier_list = []

        # Loop through PRICES dictionary using enumerate to get both index and supplier name
        for index, supplier in enumerate(cls.PRICES.keys(), start=1):
            # Format each supplier with its index
            supplier_list.append(f"{index}. {supplier}")

        # Join all supplier lines with a newline character and return the result
        return "\n".join(supplier_list)



