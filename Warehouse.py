class Warehouse:
    # Static data for warehouse capacities, depreciation rates, and costs
    CAPACITIES = {
        "fertiliser": {"main": 20, "aux": 10},  # litres
        "feed": {"main": 400, "aux": 200},      # kg
        "salt": {"main": 200, "aux": 100}       # kg
    }

    DEPRECIATION_RATES = {
        "fertiliser": 0.4,  # per quarter
        "feed": 0.1,
        "salt": 0.0
    }

    COSTS = {
        "fertiliser": 0.10,  # cost per litre
        "feed": 0.001,       # cost per gram (1 kg = £1)
        "salt": 0.001        # cost per gram
    }

    @classmethod
    def get_total_capacity(cls):
        """Calculate total capacity (main + aux) for each resource."""
        return {
            "fertiliser": cls.CAPACITIES["fertiliser"]["main"] + cls.CAPACITIES["fertiliser"]["aux"],
            "feed": cls.CAPACITIES["feed"]["main"] + cls.CAPACITIES["feed"]["aux"],
            "salt": cls.CAPACITIES["salt"]["main"] + cls.CAPACITIES["salt"]["aux"]
        }

    @classmethod
    def display_warehouse_info(cls):
        """Display information about capacities, depreciation rates, and costs."""
        capacities = cls.get_total_capacity()
        return (f"Capacities - Fertiliser: {capacities['fertiliser']} litres, "
                f"Feed: {capacities['feed']} kg, Salt: {capacities['salt']} kg\n"
                f"Depreciation Rates - Fertiliser: {cls.DEPRECIATION_RATES['fertiliser']} per quarter, "
                f"Feed: {cls.DEPRECIATION_RATES['feed']} per quarter, "
                f"Salt: {cls.DEPRECIATION_RATES['salt']} per quarter\n"
                f"Warehouse Costs - Fertiliser: £{cls.COSTS['fertiliser']} per litre, "
                f"Feed: £{cls.COSTS['feed']} per gram, Salt: £{cls.COSTS['salt']} per gram")


print(Warehouse.display_warehouse_info())
