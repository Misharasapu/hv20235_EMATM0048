

class Fish:
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
        """Retrieve information for a specific fish type."""
        if fish_type in cls.FISH_DATA:
            return cls.FISH_DATA[fish_type]
        else:
            return f"{fish_type} not found in FISH_DATA."

    @classmethod
    def display_all_fish(cls):
        """Display all fish types and their details."""
        for fish, data in cls.FISH_DATA.items():
            print(f"Fish Type: {fish}, Details: {data}")

    @classmethod
    def calculate_resource_needs(cls, fish_type, quantity):
        """
        Calculate total resources needed based on the quantity of fish.

        :param fish_type: Type of fish (e.g., 'Clef Fins')
        :param quantity: Number of fish being managed or sold.
        :return: Dictionary with required amounts for fertiliser, feed, and salt.
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
        Retrieve the maintenance time in weeks for this fish type.

        :param fish_type: Type of fish (e.g., 'Clef Fins')
        :return: Maintenance time in weeks for the given fish type.
        """
        maintenance_time_days = cls.FISH_DATA.get(fish_type, {}).get("maintenance_time", 0)
        # Convert days to weeks (assuming a 5-day work week)
        maintenance_time_weeks = maintenance_time_days / 5
        return maintenance_time_weeks

    @classmethod
    def calculate_total_maintenance_time(cls, fish_type, quantity):
        """
        Calculate the total maintenance time in weeks required based on the quantity of fish.

        :param fish_type: Type of fish (e.g., 'Clef Fins')
        :param quantity: Number of fish being managed or sold.
        :return: Total maintenance time in weeks required for the given quantity of fish.
        """
        maintenance_time_per_fish = cls.get_maintenance_time(fish_type)
        return maintenance_time_per_fish * quantity



