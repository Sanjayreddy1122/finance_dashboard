import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# --- Step 1: Create sample data ---
data = {
    "date": ["2025-10-01", "2025-10-02", "2025-10-03", "2025-10-04", "2025-10-05"],
    "category": ["Food", "Salary", "Transport", "Shopping", "Food"],
    "description": ["Zomato", "October Salary", "Uber", "Amazon", "Groceries"],
    "amount": [350, 50000, 200, 1200, 500],
    "type": ["Expense", "Income", "Expense", "Expense", "Expense"]
}
df = pd.DataFrame(data)

# --- Step 2: Store data in SQLite ---
conn = sqlite3.connect("finance_db.sqlite")
df.to_sql("transactions", conn, if_exists="replace", index=False)

# --- Step 3: SQL query for expenses ---
query_expense_by_cat = """
SELECT category, SUM(amount) AS total_expense
FROM transactions
WHERE type='Expense'
GROUP BY category
ORDER BY total_expense DESC;
"""
expenses = pd.read_sql_query(query_expense_by_cat, conn)

# --- Step 4: Calculate totals ---
total_income = df[df["type"]=="Income"]["amount"].sum()
total_expense = df[df["type"]=="Expense"]["amount"].sum()
net_saving = total_income - total_expense

print("\n------ Financial Summary ------")
print(f"Total Income: ₹{total_income}")
print(f"Total Expenses: ₹{total_expense}")
print(f"Net Savings: ₹{net_saving}")
print("\nExpense Breakdown by Category:")
print(expenses)

# --- Step 5: Visualization ---
plt.figure(figsize=(8,4))
plt.bar(expenses["category"], expenses["total_expense"], color='orange')
plt.title("Expenses by Category")
plt.xlabel("Category")
plt.ylabel("Amount (₹)")
plt.tight_layout()
plt.show()

conn.close()