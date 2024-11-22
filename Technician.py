class Technician:
    WEEKLY_WAGE = 500  # Fixed wage per week in pounds
    LABOUR_PER_QUARTER = 9  # Number of weeks of labour provided per quarter
    MAX_TECHNICIANS = 5  # Maximum number of technicians allowed per quarter
    MIN_TECHNICIANS = 1  # Minimum number of technicians required per quarter

    def __init__(self, name, specialisation=None):
        """
        Initialize a Technician with a name and an optional specialisation.
        :param name: Name of the technician.
        :param specialisation: The fish type the technician is specialised in.
        """
        self.name = name
        self.specialisation = specialisation  # A single fish type or None
        self.quarterly_wage = Technician.WEEKLY_WAGE * 12

    def get_wage(self):
        """Return the technician's wage for the quarter."""
        return self.quarterly_wage

    @classmethod
    def max_technicians(cls):
        """Return the maximum number of technicians allowed per quarter."""
        return cls.MAX_TECHNICIANS

    @classmethod
    def get_quarterly_labour(cls):
        """Return the total labor each technician provides per quarter in days (9 weeks)."""
        return cls.LABOUR_PER_QUARTER

    @classmethod
    def calculate_total_labour(cls, num_technicians):
        """
        Calculate total labor available per quarter based on the number of technicians.
        :param num_technicians: Number of technicians.
        :return: Total labor in days.
        """
        return num_technicians * cls.get_quarterly_labour()

    @classmethod
    def calculate_total_wages(cls, technicians):
        """
        Calculate the total wages for a list of technicians.
        :param technicians: List of Technician instances.
        :return: Total wages for the quarter.
        """
        return sum(technician.get_wage() for technician in technicians)

    def is_specialised_for(self, fish_type):
        """
        Check if the technician is specialised for a specific fish type.
        :param fish_type: Name of the fish type.
        :return: True if the technician is specialised for the given fish type, False otherwise.
        """
        return self.specialisation == fish_type

    def __str__(self):
        """Return a formatted string for displaying technician details."""
        specialisation = self.specialisation or "None"
        return f"Technician {self.name}, weekly rate={Technician.WEEKLY_WAGE}, specialisation={specialisation}"
