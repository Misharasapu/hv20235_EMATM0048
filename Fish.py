

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




