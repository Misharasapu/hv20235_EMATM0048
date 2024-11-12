class Technician:
    WEEKLY_WAGE = 500  # Fixed wage per week in pounds
    LABOUR_PER_QUARTER = 9  # Number of weeks of labour provided per quarter
    MAX_TECHNICIANS = 5  # Maximum number of technicians allowed per quarter
    MIN_TECHNICIANS = 1  # Minimum number of technicians required per quarter (for reference)

    def __init__(self, name):
        self.name = name
        self.quarterly_wage = Technician.WEEKLY_WAGE * 12  # Calculate wage per quarter

    def get_wage(self):
        """Return the technician's wage for the quarter."""
        return self.quarterly_wage

    @classmethod
    def max_technicians(cls):
        """Return the maximum number of technicians allowed per quarter."""
        return cls.MAX_TECHNICIANS

    def get_quarterly_labour(self):
        """Return the total number of weeks the technician is available per quarter (9 weeks)."""
        return Technician.LABOUR_PER_QUARTER


