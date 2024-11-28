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
        Retrieve the price of a specific supply type from a given supplier.

        Args:
            supplier_name (str): Name of the supplier (e.g., "Slippery Lakes").
            supply_type (str): Type of supply (e.g., "fertiliser", "feed", or "salt").

        Returns:
            float or None: Price per unit for the specified supply type from the supplier,
            or None if the supplier or supply type is not found.
        """
        return cls.PRICES.get(supplier_name, {}).get(supply_type, None)

    @classmethod
    def list_suppliers(cls):
        """
        Generate a formatted list of all available suppliers with indices for easy selection.

        Returns:
            str: A formatted string listing suppliers by index.
        """
        # Initialize an empty list to store each supplier line
        supplier_list = []

        # Loop through PRICES dictionary using enumerate to get both index and supplier name
        for index, supplier in enumerate(cls.PRICES.keys(), start=1):
            # Format each supplier with its index
            supplier_list.append(f"{index}. {supplier}")

        # Join all supplier lines with a newline character and return the result
        return "\n".join(supplier_list)
