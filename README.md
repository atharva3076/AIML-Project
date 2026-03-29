# AIML-Project

# AI-Powered Expense Distributor

Split group expenses fairly and settle debts in the fewest transactions possible — with automatic expense categorization and spending pattern analysis built in.

Built for trips, shared flats, team outings — anywhere money gets messy.

------------------------------------------------------------------------------------------------------------------------------

## What It Does

- Enter expenses: who paid, how much, and who was involved
- Automatically tags each expense into a category (Food, Transport, Accommodation, etc.) using NLP keyword matching
- Calculates who owes whom and figures out the minimum number of transactions to settle everything
- Groups members into spending profiles (Light / Moderate / Heavy) using K-Means clustering
- Exports a full JSON report at the end

------------------------------------------------------------------------------------------------------------------------------

## How to Run

**Quick demo — no input needed**
```bash
python demo.py
```
Runs a pre-loaded Goa trip scenario with 4 people and 7 expenses.

**Interactive mode**
```bash
python expense_distributor.py
```
Enter your group members, then use the menu to add expenses and view results.

------------------------------------------------------------------------------------------------------------------------------

## Menu

```
1. Add Expense          → description, amount, who paid, who participated
2. View Summary         → spending breakdown by category
3. Settlement Plan      → who pays whom and how much
4. Spending Clusters    → K-Means analysis of member spending behaviour
5. Save Report          → exports to expense_report.json
6. Exit
```

------------------------------------------------------------------------------------------------------------------------------

## Example Output

```
Added: 'Hotel stay' (₹4500.00) — Category: Accommodation
Added: 'Uber to beach' (₹350.00) — Category: Transport
Added: 'Dinner at restaurant' (₹2400.00) — Category: Food

EXPENSE SUMMARY BY CATEGORY

Accommodation    ₹ 4500.00  ████████████
Food             ₹ 2880.00  ████████
Transport        ₹ 1150.00  ███

SETTLEMENT PLAN

Settle in 3 transaction(s):

Priya  →  Arjun    ₹1603.33
Sneha  →  Arjun    ₹618.33
Sneha  →  Rahul    ₹535.00

Spending Clusters (K-Means):
Arjun     ₹5100.00   Heavy Spender
Priya     ₹1150.00   Moderate Spender
Rahul     ₹2880.00   Light Spender
Sneha     ₹1600.00   Moderate Spender
```

------------------------------------------------------------------------------------------------------------------------------

## Project Structure

```
ai-expense-distributor/
├── expense_distributor.py   # main app
├── demo.py                  # non-interactive demo
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------------------------------------------------------------

## Dependencies

- `numpy`
- `scikit-learn`
