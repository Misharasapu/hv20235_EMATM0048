class Hatchery:
    # Static data related to customer demand and fixed quarterly cost
    CUSTOMER_DEMAND = {
        "Clef Fins": {"demand": 25, "price": 250},
        "Timpani Snapper": {"demand": 10, "price": 350},
        "Andalusian Brim": {"demand": 15, "price": 250},
        "Plagal Cod": {"demand": 20, "price": 400},
        "Fugue Flounder": {"demand": 30, "price": 550},
        "Modal Bass": {"demand": 50, "price": 500}
    }
    FIXED_QUARTERLY_COST = 1500  # Fixed cost incurred each quarter

    def __init__(self):
        # Instance attribute for tracking the cash balance
        self.cash_balance = 10000  # Starting cash balance

    @classmethod
    def get_demand_and_price(cls, fish_type):
        """
        Retrieve the demand and price for a specific fish type.

        :param fish_type: Name of the fish species.
        :return: Dictionary containing 'demand' and 'price' for the specified fish, or None if not found.
        """
        return cls.CUSTOMER_DEMAND.get(fish_type, None)

    @classmethod
    def get_fixed_cost(cls):
        """
        Return the fixed quarterly cost for the hatchery.

        :return: Fixed cost for the quarter.
        """
        return cls.FIXED_QUARTERLY_COST

    def get_cash_balance(self):
        """
        Return the current cash balance of the hatchery.

        :return: Current cash balance.
        """
        return self.cash_balance
