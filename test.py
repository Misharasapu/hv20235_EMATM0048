from Hatchery import Hatchery
from Technician import Technician
from Fish import Fish

def test_specialised_technician_impact():
    # Set up the Hatchery
    hatchery = Hatchery()
    hatchery.available_labor = 18  # Set available labour for the quarter

    # Add technicians (1 specialised in Clef Fins, 1 regular)
    hatchery.technicians = [
        Technician(name="Specialist", specialisation="Modal Bass"),  # Specialised technician
        Technician(name="Regular", specialisation=None),           # Regular technician
    ]

    # Define test parameters
    fish_type = "Modal Bass"
    requested_quantity = 30  # Request to sell 10 units of Clef Fins

    # Calculate expected values
    base_maintenance_time = Fish.calculate_total_maintenance_time(fish_type, requested_quantity)
    adjusted_maintenance_time = base_maintenance_time * (2 / 3)  # Due to the specialised technician
    expected_remaining_labour = hatchery.available_labor - adjusted_maintenance_time

    # Call the sell_fish method
    result = hatchery.sell_fish(fish_type, requested_quantity)

    # Print test results
    print("\n=== Test Results ===")
    print(f"Fish Type: {fish_type}")
    print(f"Requested Quantity: {requested_quantity}")
    print(f"Base Maintenance Time: {base_maintenance_time}")
    print(f"Adjusted Maintenance Time (Specialised Technician): {adjusted_maintenance_time}")
    print(f"Initial Labour: 18")
    print(f"Remaining Labour After Deduction: {hatchery.available_labor}")
    print(f"Sell Fish Result: {result}")

    # Assertions
    assert result["status"] == "success", "Failed: Sale should be successful."
    assert round(hatchery.available_labor, 2) == round(expected_remaining_labour, 2), \
        "Failed: Labour deduction with specialised technicians is incorrect."

# Run the test
if __name__ == "__main__":
    test_specialised_technician_impact()
