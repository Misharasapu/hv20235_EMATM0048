"""
Author: Mishara Sapukotanage
Section: Data Science
Description: This file contains the Fish class, which manages static data and
provides methods for fish-related operations, including calculating resource needs,
determining maintenance time, and listing fish species.
"""

class Fish:
    """
    The Fish class handles information and operations related to fish species in the hatchery.
    It provides static data and utility methods for resource calculations, maintenance time estimation,
    and fish type management.

    Attributes:
        FISH_DATA (dict): Static dictionary containing data for each fish type,
        including resource requirements and maintenance time.
    """

    # Static dictionary holding data for each fish species
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
            dict: Resource requirements and maintenance time for the fish type,
                  if found in FISH_DATA.
            str: Error message if the fish type is not found.
        """
        # Check if the fish type exists in the FISH_DATA dictionary
        if fish_type in cls.FISH_DATA:
            # If it exists, return the corresponding data
            return cls.FISH_DATA[fish_type]
        # If the fish type is not found, return an error message
        return f"{fish_type} not found in FISH_DATA."

    @classmethod
    def display_all_fish(cls):
        """
        Print details of all available fish species and their resource requirements.
        """
        # Iterate through each fish type in the FISH_DATA dictionary
        for fish, data in cls.FISH_DATA.items():
            # Print the fish type along with its resource requirements
            print(f"Fish Type: {fish}, Details: {data}")

    @classmethod
    def calculate_resource_needs(cls, fish_type, quantity):
        """
        Calculate the total resources required for a specific quantity of a fish type.

        Args:
            fish_type (str): Name of the fish species (e.g., "Clef Fins").
            quantity (int): Number of fish.

        Returns:
            dict: Total amounts of fertiliser, feed, and salt needed, or an empty
                  dictionary if the fish type is not found.
        """
        # Check if the fish type exists in the FISH_DATA dictionary
        if fish_type in cls.FISH_DATA:
            # Retrieve the resource requirements for the specified fish type
            requirements = cls.FISH_DATA[fish_type]
            # Calculate the total requirements by multiplying by the quantity
            return {
                "fertiliser": requirements["fertilizer_req"] * quantity,
                "feed": requirements["feed_req"] * quantity,
                "salt": requirements["salt_req"] * quantity
            }
        # Return an empty dictionary if the fish type is not found
        return {}

    @classmethod
    def get_maintenance_time(cls, fish_type):
        """
        Retrieve the maintenance time (in weeks) for a specific fish type.

        Args:
            fish_type (str): Name of the fish species (e.g., "Clef Fins").

        Returns:
            float: Maintenance time in weeks, or 0 if the fish type is not found.
        """
        # Get the maintenance time (in days) for the fish type, defaulting to 0 if not found
        maintenance_time_days = cls.FISH_DATA.get(fish_type, {}).get("maintenance_time", 0)
        # Convert maintenance time from days to weeks
        # Assuming a 5-day work week
        return maintenance_time_days / 5

    @classmethod
    def calculate_total_maintenance_time(cls, fish_type, quantity):
        """
        Calculate the total maintenance time (in weeks) required for a given quantity of a fish type.

        Args:
            fish_type (str): Name of the fish species (e.g., "Clef Fins").
            quantity (int): Number of fish.

        Returns:
            float: Total maintenance time in weeks.
        """
        # Get the maintenance time for a single fish of the specified type
        maintenance_time_per_fish = cls.get_maintenance_time(fish_type)
        # Multiply the per-fish maintenance time by the quantity to get the total time
        return maintenance_time_per_fish * quantity

    @classmethod
    def list_fish_types(cls):
        """
        Generate a formatted list of all available fish species with indices for display.

        Returns:
            str: A formatted string listing fish species with their indices.
        """
        # Initialise an empty list to store formatted fish types
        fish_list = []
        # Enumerate through the fish types in FISH_DATA, starting index at 1
        for index, fish_type in enumerate(cls.FISH_DATA.keys(), start=1):
            # Append each fish type with its index to the list
            fish_list.append(f"{index}. {fish_type}")
        # Join the list into a single string with line breaks and return it
        return "\n".join(fish_list)
