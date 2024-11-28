"""
Author: Mishara Sapukotanage
Section: Data Science
Description: This file contains the Supplier class, which manages information about
the suppliers available for restocking resources. It includes methods for retrieving
pricing information and listing suppliers.
"""

class Supplier:
    """
    The Supplier class provides static data and methods to manage suppliers and their
    pricing information. It allows the retrieval of prices for specific supply types
    and listing of all suppliers.

    Attributes:
        PRICES (dict): Static dictionary containing prices for different supply types
        (fertiliser, feed, salt) offered by each supplier.
    """
    # Static pricing information as a class-level dictionary
    PRICES = {
        "Slippery Lakes": {
            "fertiliser": 0.0003,  # Price per ml (converted from 0.30 per litre)
            "feed": 0.1,  # Price per kg
            "salt": 0.05  # Price per kg
        },
        "Scaly Wholesaler": {
            "fertiliser": 0.0002,  # Price per ml (converted from 0.20 per litre)
            "feed": 0.4,  # Price per kg
            "salt": 0.25  # Price per kg
        }
    }

    @classmethod
    def get_price(cls, supplier_name, supply_type):
        """
        Retrieve the price of a specific supply type from a given supplier.

        Args:
            supplier_name (str): Name of the supplier (e.g., "Slippery Lakes").
            supply_type (str): Type of supply (e.g., "fertiliser", "feed", or "salt").

        Returns:
            float or None: Price per unit for the specified supply type from the supplier,
            or None if the supplier or supply type is not found.
        """
        # Attempt to retrieve the supplier's details from the PRICES dictionary.
        # If the supplier is not found, return an empty dictionary.
        supplier_data = cls.PRICES.get(supplier_name, {})

        # Attempt to retrieve the price for the given supply type from the supplier's data.
        # If the supply type is not found, return None.
        price = supplier_data.get(supply_type, None)

        # Return the price (or None if either the supplier or supply type doesn't exist).
        return price

    @classmethod
    def list_suppliers(cls):
        """
        Generate a formatted list of all available suppliers with indices for easy selection.

        Returns:
            str: A formatted string listing suppliers by index.
        """
        # Initialize an empty list to store each supplier entry as a formatted string.
        supplier_list = []

        # Loop through the PRICES dictionary, enumerating supplier names with an index.
        # The `start=1` ensures the indices start from 1 for user-friendly display.
        for index, supplier in enumerate(cls.PRICES.keys(), start=1):
            # Append the formatted supplier name and index to the list.
            supplier_list.append(f"{index}. {supplier}")

        # Join the list of supplier entries with newline characters to form a multi-line string.
        # Return the final formatted string.
        return "\n".join(supplier_list)
