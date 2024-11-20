from Hatchery import Hatchery

# Initialize Hatchery instance
hatchery = Hatchery()

# Simulate adding technicians
hatchery.add_technicians(["Alice", "Bob"])
print(f"Technicians hired: {[tech.name for tech in hatchery.technicians]}")

# Simulate a quarter's labor and sales
hatchery.start_new_quarter()
hatchery.sell_fish("Clef Fins", 10)  # Example sale
hatchery.sell_fish("Timpani Snapper", 5)  # Example sale

# Apply depreciation to warehouse stocks
print("\nApplying depreciation to the warehouse...")
hatchery.warehouse.calculate_depreciation()

# Call end_of_quarter_summary and test it
supplier_name = "Slippery Lakes"  # Example supplier
summary = hatchery.end_of_quarter_summary(supplier_name)

# Display the returned summary
print("\n=== End of Quarter Summary ===")
print(f"Fixed Costs: {summary['fixed_costs']}")
print(f"Technician Wages: {summary['technician_wages']}")
print(f"Storage Costs: {summary['storage_costs']}")
print(f"Restocking Costs: {summary['restocking_costs']}")
print(f"Total Expenses: {summary['total_expenses']}")
print(f"Remaining Cash Balance: {summary['remaining_cash_balance']:.2f}")

# Verify the results manually or via assertions
expected_cash_balance = 10000 - (
    summary["fixed_costs"]
    + summary["technician_wages"]
    + summary["storage_costs"]
    + summary["restocking_costs"]
)
assert abs(summary["remaining_cash_balance"] - expected_cash_balance) < 0.01, "Cash balance calculation error"
print("\nTest Passed: End-of-quarter summary calculations are correct.")
