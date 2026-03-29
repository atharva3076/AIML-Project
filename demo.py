from expense_distributor import (
    add_expense, calculate_balances, minimize_transactions,
    print_summary, print_settlement, cluster_spending_patterns,
    save_report, members
)

print("\n Demo: Goa Trip Expense Split\n")

add_expense("Hotel stay",4500,"Arjun",["Arjun", "Priya", "Rahul", "Sneha"])
add_expense("Taxi from airport",800,"Priya",["Arjun", "Priya", "Rahul","Sneha"])
add_expense("Dinner at restaurant",2400, "Rahul", ["Arjun", "Priya", "Rahul", "Sneha"])
add_expense("Snorkeling tickets",  1600, "Sneha", ["Arjun", "Priya", "Sneha"])
add_expense("Groceries", 600, "Arjun", ["Arjun", "Rahul"])
add_expense("Uber to beach", 350, "Priya", ["Priya", "Sneha"])
add_expense("Coffee and snacks", 480, "Rahul", ["Arjun", "Priya", "Rahul", "Sneha"])

print_summary()
print_settlement()
cluster_spending_patterns()
save_report("demo_report.json")
