"""
Author: [Your Name]
Section: [Your Section/Group]
Description: This file contains the Fish class, which provides static data and
methods to manage fish-related operations, including resource calculation,
maintenance time determination, and listing fish types.
"""

class Fish:
    """
    The Fish class manages all information related to the fish species available
    in the hatchery. It provides methods to calculate resource requirements,
    maintenance times, and display fish details.

    Attributes:
        FISH_DATA (dict): Static dictionary containing data for each fish type,
        including resource requirements and maintenance time.
    """
    # Dictionary holding data for each fish type
    FISH_DATA = {
        "Clef Fins": {
            "fertilizer_req": 100.0,
            "feed_req": 12,
            "salt_req": 2,
            "maintenance_time": 2.0
        },
        "Timpani Snapper": {
            "fertilizer_req": 50.0,
            "feed_req": 9,
            "salt_req": 2,
            "maintenance_time": 1.0
        },
        "Andalusian Brim": {
            "fertilizer_req": 90.0,
            "feed_req": 6,
            "salt_req": 2,
            "maintenance_time": 0.5
        },
        "Plagal Cod": {
            "fertilizer_req": 100.0,
            "feed_req": 10,
            "salt_req": 2,
            "maintenance_time": 2.0
        },
        "Fugue Flounder": {
            "fertilizer_req": 200.0,
            "feed_req": 12,
            "salt_req": 2,
            "maintenance_time": 2.5
        },
        "Modal Bass": {
            "fertilizer_req": 300.0,
            "feed_req": 12,
            "salt_req": 6,
            "maintenance_time": 3.0
        }
    }

    @classmethod
    def get_fish_info(cls, fish_type):
        """
        Retrieve detailed information for a specific fish type.

        Args:
            fish_type (str): Name of the fish species (e.g., "Clef Fins").

        Returns:
            dict or str: A dictionary containing resource requirements and
            maintenance time if the fish type exists, or an error message if not found.
        """
        if fish_type in cls.FISH_DATA:
            return cls.FISH_DATA[fish_type]
        else:
            return f"{fish_type} not found in FISH_DATA."

    @classmethod
    def display_all_fish(cls):
        """
        Print details of all available fish types and their resource requirements.
        """
        for fish, data in cls.FISH_DATA.items():
            print(f"Fish Type: {fish}, Details: {data}")

    @classmethod
    def calculate_resource_needs(cls, fish_type, quantity):
        """
        Calculate the total amount of resources needed for a specified quantity of fish.

        Args:
            fish_type (str): Type of fish (e.g., "Clef Fins").
            quantity (int): Number of fish to calculate resources for.

        Returns:
            dict: A dictionary with total amounts of fertilizer, feed, and salt required.
        """
        if fish_type in cls.FISH_DATA:
            requirements = cls.FISH_DATA[fish_type]
            return {
                "fertiliser": requirements["fertilizer_req"] * quantity,
                "feed": requirements["feed_req"] * quantity,
                "salt": requirements["salt_req"] * quantity
            }
        return {}

    @classmethod
    def get_maintenance_time(cls, fish_type):
        """
        Retrieve the maintenance time in weeks for a specific fish type.

        Args:
            fish_type (str): Type of fish (e.g., "Clef Fins").

        Returns:
            float: Maintenance time in weeks for the given fish type. Returns 0
            if the fish type is not found.
        """
        maintenance_time_days = cls.FISH_DATA.get(fish_type, {}).get("maintenance_time", 0)
        # Convert days to weeks (assuming a 5-day work week)
        maintenance_time_weeks = maintenance_time_days / 5
        return maintenance_time_weeks

    @classmethod
    def calculate_total_maintenance_time(cls, fish_type, quantity):
        """
        Calculate the total maintenance time in weeks required for a given quantity of fish.

        Args:
            fish_type (str): Type of fish (e.g., "Clef Fins").
            quantity (int): Number of fish to calculate maintenance time for.

        Returns:
            float: Total maintenance time in weeks required.
        """
        maintenance_time_per_fish = cls.get_maintenance_time(fish_type)
        return maintenance_time_per_fish * quantity

    @classmethod
    def list_fish_types(cls):
        """
        Generate a formatted list of all available fish types with indices for console selection.

        Returns:
            str: A formatted string listing fish types with their indices.
        """
        fish_list = []
        for index, fish_type in enumerate(cls.FISH_DATA.keys(), start=1):
            fish_list.append(f"{index}. {fish_type}")
        return "\n".join(fish_list)
