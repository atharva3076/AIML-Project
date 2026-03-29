"""
Expense Distributor — AI/ML Enhanced Group Expense Splitter
Course: Fundamentals of AI and ML (CSA2001)
"""

import json
import os
from collections import defaultdict
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import numpy as np

# 1. NLP-BASED AUTO CATEGORY CLASSIFIER

CATEGORY_KEYWORDS = {
    "Accommodation": ["hotel", "hostel", "airbnb", "rent", "room", "stay", "lodge"],
    "Food": ["pizza", "burger", "restaurant", "food", "lunch", "dinner", "breakfast",
             "cafe", "coffee", "snack", "meal", "biryani", "dosa", "swiggy", "zomato"],
    "Transport": ["uber", "ola", "cab", "taxi", "bus", "train", "metro", "petrol",
                  "fuel", "auto", "rickshaw", "flight", "rapido"],
    "Entertainment": ["movie", "cinema", "netflix", "game", "concert", "event",
                      "show", "party", "club", "bar", "pub", "snorkeling", "trek",
                      "adventure", "activity", "ticket", "tickets"],
    "Groceries": ["grocery", "vegetables", "fruits", "supermarket", "market",
                  "milk", "eggs", "bread", "rice", "dal", "oil"],
    "Utilities": ["electricity", "water", "wifi", "internet", "gas", "bill", "recharge"],
    "Shopping": ["clothes", "shoes", "amazon", "flipkart", "mall", "shirt", "bag"],
    "Medical": ["medicine", "doctor", "pharmacy", "hospital", "health", "clinic"],
    "Miscellaneous": []
}

def classify_expense(description: str) -> str:
    """Classify expense description into a category using keyword matching (NLP)."""
    desc_lower = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in desc_lower:
                return category
    return "Miscellaneous"


# 2. EXPENSE DATA STRUCTURES

expenses = []   # list of {description, amount, paid_by, participants, category}
members = set()

def add_expense(description: str, amount: float, paid_by: str, participants: list):
    """Add an expense and auto-classify it."""
    paid_by = paid_by.strip().title()
    participants = [p.strip().title() for p in participants]
    members.add(paid_by)
    members.update(participants)

    category = classify_expense(description)

    expenses.append({
        "description": description,
        "amount": amount,
        "paid_by": paid_by,
        "participants": participants,
        "category": category
    })
    print(f"Added: '{description}' (₹{amount:.2f}) — Category: {category}")



# 3. CORE DEBT MINIMIZATION ALGORITHM

def calculate_balances() -> dict:
    """Calculate net balance for each person (positive = owed money, negative = owes money)."""
    balance = defaultdict(float)

    for exp in expenses:
        share = exp["amount"] / len(exp["participants"])
        balance[exp["paid_by"]] += exp["amount"]
        for person in exp["participants"]:
            balance[person] -= share

    return dict(balance)


def minimize_transactions(balances: dict) -> list:
    """
    Greedy debt minimization: reduces number of transactions needed to settle all debts.
    Returns list of (debtor, creditor, amount) tuples.
    """
    creditors = sorted([(p, b) for p, b in balances.items() if b > 0.01], key=lambda x: -x[1])
    debtors   = sorted([(p, -b) for p, b in balances.items() if b < -0.01], key=lambda x: -x[1])

    transactions = []
    i, j = 0, 0

    while i < len(debtors) and j < len(creditors):
        debtor, debt     = debtors[i]
        creditor, credit = creditors[j]

        amount = min(debt, credit)
        transactions.append((debtor, creditor, round(amount, 2)))

        debtors[i]   = (debtor,   round(debt - amount, 2))
        creditors[j] = (creditor, round(credit - amount, 2))

        if debtors[i][1] < 0.01:   i += 1
        if creditors[j][1] < 0.01: j += 1

    return transactions


# 4. ML: K-MEANS CLUSTERING ON SPENDING PATTERNS

def cluster_spending_patterns():
    """
    Use K-Means clustering to group members by their spending behaviour.
    Features: total_spent, total_paid, num_categories
    """
    if len(members) < 2:
        print("\n  (Not enough members to cluster.)")
        return

    member_list = sorted(members)
    feature_matrix = []

    all_categories = list(CATEGORY_KEYWORDS.keys())
    le = LabelEncoder()
    le.fit(all_categories)

    for person in member_list:
        total_paid  = sum(e["amount"] for e in expenses if e["paid_by"] == person)
        total_share = sum(e["amount"] / len(e["participants"])
                         for e in expenses if person in e["participants"])
        categories_used = set(e["category"] for e in expenses
                               if person in e["participants"] or e["paid_by"] == person)
        num_categories = len(categories_used)
        feature_matrix.append([total_paid, total_share, num_categories])

    X = np.array(feature_matrix, dtype=float)

    # Determine number of clusters (max 3, min 2)
    n_clusters = min(3, len(member_list))
    if n_clusters < 2:
        return

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    cluster_names = ["Light Spender", "Moderate Spender", "Heavy Spender"]
    # Sort clusters by centroid total_share (feature index 1)
    centroid_order = np.argsort(kmeans.cluster_centers_[:, 1])
    label_map = {old: cluster_names[new] for new, old in enumerate(centroid_order)}

    print("\n Spending Pattern Clusters (K-Means):")
    print(f"  {'Member':<15} {'Paid':>10} {'Owed Share':>12} {'Categories':>12} {'Cluster':<20}")
    print("  " + "─" * 72)
    for idx, person in enumerate(member_list):
        f = feature_matrix[idx]
        cluster_label = label_map[labels[idx]]
        print(f"  {person:<15} ₹{f[0]:>8.2f}   ₹{f[1]:>8.2f}   {int(f[2]):>10}   {cluster_label}")



# 5. SUMMARY & REPORT

def print_summary():
    print("\n EXPENSE SUMMARY BY CATEGORY")
    
    category_totals = defaultdict(float)
    for e in expenses:
        category_totals[e["category"]] += e["amount"]

    total = sum(category_totals.values())
    for cat, amt in sorted(category_totals.items(), key=lambda x: -x[1]):
        bar = "█" * int((amt / total) * 30)
        print(f"  {cat:<16} ₹{amt:>8.2f}  {bar}")
    print(f"\n  {'TOTAL':<16} ₹{total:>8.2f}")


def print_settlement():
    print("\nSETTLEMENT PLAN")
   
    balances = calculate_balances()
    transactions = minimize_transactions(balances)

    if not transactions:
        print("Everyone is already settled up!")
        return

    print(f"Settle in {len(transactions)} transaction(s):\n")
    for debtor, creditor, amount in transactions:
        print(f" {debtor:<15} → {creditor:<15}  ₹{amount:.2f}")

    print("\n Net Balances:")
    for person, bal in sorted(balances.items()):
        status = "gets back" if bal > 0 else "owes"
        print(f" {person:<15} {status} ₹{abs(bal):.2f}")


def save_report(filename="expense_report.json"):
    balances = calculate_balances()
    transactions = minimize_transactions(balances)
    report = {
        "expenses": expenses,
        "balances": balances,
        "settlement": [{"from": d, "to": c, "amount": a} for d, c, a in transactions]
    }
    with open(filename, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n Report saved to {filename}")


# 6. CLI INTERFACE

def get_members_input():
    print("\n Enter group members (comma-separated):")
    raw = input("  > ").strip()
    return [m.strip().title() for m in raw.split(",") if m.strip()]


def add_expense_interactive(group_members):
    print("\n  ─── Add New Expense ───")
    description = input("  Description (e.g. pizza, uber): ").strip()
    while True:
        try:
            amount = float(input("  Amount (₹): ").strip())
            break
        except ValueError:
            print("  Please enter a valid number.")

    print(f" Members: {', '.join(group_members)}")
    paid_by = input("  Paid by: ").strip().title()
    if paid_by not in group_members:
        group_members.append(paid_by)

    print(" Who participated? (comma-separated, or press Enter for all)")
    raw = input("  > ").strip()
    if not raw:
        participants = group_members[:]
    else:
        participants = [p.strip().title() for p in raw.split(",")]

    add_expense(description, amount, paid_by, participants)
    return group_members


def main():
    
    print("AI-Powered Expense Distributor ")
    print("Group Expense Splitter & Analyzer")

    group_members = get_members_input()
    members.update(group_members)

    while True:
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Settlement Plan")
        print("4. Spending Clusters (ML)")
        print("5. Save Report")
        print("6. Exit")
        
        choice = input("  Choose: ").strip()

        if choice == "1":
            group_members = add_expense_interactive(group_members)
        elif choice == "2":
            if not expenses:
                print("  No expenses added yet.")
            else:
                print_summary()
        elif choice == "3":
            if not expenses:
                print("  No expenses added yet.")
            else:
                print_settlement()
        elif choice == "4":
            if len(expenses) < 2:
                print("  Add at least 2 expenses to see clustering.")
            else:
                cluster_spending_patterns()
        elif choice == "5":
            if expenses:
                save_report()
            else:
                print("  No expenses to save.")
        elif choice == "6":
            print("\n  Goodbye! ")
            break
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()
