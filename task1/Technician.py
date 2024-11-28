"""
Author: Mishara Sapukotanage
Section: Data Science
Description: This file contains the Technician class, which represents employees working
at the hatchery. It includes attributes and methods for managing wages, labour,
and specialisations of technicians.
"""

class Technician:
    """
    The Technician class represents employees working at the hatchery. It includes methods
    for calculating wages, available labour, and determining specialisations.

    Attributes:
        WEEKLY_WAGE (int): Fixed weekly wage for each technician.
        LABOUR_PER_QUARTER (int): Number of weeks of labour provided per technician each quarter.
        MAX_TECHNICIANS (int): Maximum number of technicians allowed per quarter.
        MIN_TECHNICIANS (int): Minimum number of technicians required per quarter.
    """
    WEEKLY_WAGE = 500  # Fixed wage per week in pounds
    LABOUR_PER_QUARTER = 9  # Number of weeks of labour provided per quarter
    MAX_TECHNICIANS = 5  # Maximum number of technicians allowed per quarter
    MIN_TECHNICIANS = 1  # Minimum number of technicians required per quarter

    def __init__(self, name, specialisation=None):
        """
        Initialize a Technician instance with a name and an optional specialisation.

        Args:
            name (str): Name of the technician.
            specialisation (str or None): Fish type the technician is specialised in, or None if no specialisation.

        Attributes:
            name (str): Name of the technician.
            specialisation (str or None): Fish type the technician specialises in.
            quarterly_wage (int): Wage for the technician for an entire quarter (12 weeks).
        """
        # Store the technician's name
        self.name = name

        # Store the technician's specialisation, defaulting to None if not provided
        self.specialisation = specialisation  # A single fish type or None

        # Calculate and store the total wage for the quarter (12 weeks)
        self.quarterly_wage = Technician.WEEKLY_WAGE * 12  # Total quarterly wage

    def get_wage(self):
        """
        Retrieve the technician's wage for the quarter.

        Returns:
            int: Quarterly wage of the technician.
        """
        # Return the pre-calculated quarterly wage
        return self.quarterly_wage

    @classmethod
    def max_technicians(cls):
        """
        Retrieve the maximum number of technicians allowed per quarter.

        Returns:
            int: Maximum number of technicians.
        """
        # Return the class-level constant for maximum technicians
        return cls.MAX_TECHNICIANS

    @classmethod
    def get_quarterly_labour(cls):
        """
        Retrieve the total labour provided by a single technician in a quarter.

        Returns:
            int: Total labour in weeks (9 weeks per technician per quarter).
        """
        # Return the labour weeks per quarter per technician
        return cls.LABOUR_PER_QUARTER

    @classmethod
    def calculate_total_labour(cls, num_technicians):
        """
        Calculate the total labour available for a given number of technicians.

        Args:
            num_technicians (int): Number of technicians employed.

        Returns:
            int: Total labour in weeks for all technicians in the quarter.
        """
        # Multiply the labour weeks per technician by the number of technicians
        return num_technicians * cls.get_quarterly_labour()

    @classmethod
    def calculate_total_wages(cls, technicians):
        """
        Calculate the total wages for a list of technicians for a quarter.

        Args:
            technicians (list of Technician): List of Technician instances.

        Returns:
            int: Total wages for all technicians in the list.
        """
        # Use a generator to sum up the quarterly wages for all technicians in the list
        return sum(technician.get_wage() for technician in technicians)

    def is_specialised_for(self, fish_type):
        """
        Check if the technician is specialised in maintaining or selling a specific fish type.

        Args:
            fish_type (str): Name of the fish type to check.

        Returns:
            bool: True if the technician is specialised for the given fish type, False otherwise.
        """
        # Compare the technician's specialisation with the provided fish type
        # Return True if they match, otherwise False
        return self.specialisation == fish_type

    def __str__(self):
        """
        Provide a formatted string representation of the technician's details.

        Returns:
            str: A string containing the technician's name, weekly rate, and specialisation.
        """
        # Use "None" as a default string if the specialisation is not set
        specialisation = self.specialisation or "None"

        # Return a formatted string with the technician's details
        return f"Technician {self.name}, weekly rate={Technician.WEEKLY_WAGE}, specialisation={specialisation}"
