import json
import os
from datetime import datetime, timedelta, date

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'transactions.json')
BUDGET_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'budgets.json')

transactions = []
budgets = {}


# Transaction Models
def load_transactions():
    global transactions
    try:
        with open(DATA_FILE, "r") as file:
            transactions = json.load(file)
    except FileNotFoundError:
        transactions = []

    for i, t in enumerate(transactions):
        if "id" not in t:
            t["id"] = i + 1
    save_transactions()

def save_transactions():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as file:
        json.dump(transactions, file)

def get_transactions():
    return transactions

def get_transaction(t_id):
    for t in transactions:
        if t["id"] == t_id:
            return t
    return None

def add_transaction(amount, t_type, category):
    if transactions:
        new_id = max(t["id"] for t in transactions) + 1
    else:
        new_id = 1
    transaction = {
        "id": new_id,
        "amount": amount,
        "type": t_type,
        "category": category,
        "date": date.today().isoformat()
    }
    transactions.append(transaction)

def update_transaction(t_id, amount, t_type, category):
    for t in transactions:
        if t["id"] == t_id:
            t["amount"] = amount
            t["type"] = t_type
            t["category"] = category

def delete_transaction(t_id):
    global transactions
    transactions = [t for t in transactions if t["id"] != t_id]

def get_balance():
    balance = 0
    for t in transactions:
        if t["type"] == "income":
            balance += t["amount"]
        else:
            balance -= t["amount"]
    return balance

def spending_by_category():
    totals = {
        "income": {},
        "expense": {}
    }
    for t in transactions:
        transaction_type = t["type"]
        category = t["category"]
        amount = t["amount"]

        if category in totals[transaction_type]:
            totals[transaction_type][category] += amount
        else:
            totals[transaction_type][category] = amount
            
    return totals

def show_category_totals():
    totals = spending_by_category()
    for category, amount in totals.items():
        print(category, ":", amount)
        
# Budget Models

def load_budgets():
    global budgets
    try:
        with open(BUDGET_FILE, "r") as file:
            budgets = json.load(file)
    except FileNotFoundError:
        budgets = {}
        
def save_budgets():
    os.makedirs(os.path.dirname(BUDGET_FILE), exist_ok=True)
    with open(BUDGET_FILE, "w") as file:
        json.dump(budgets, file)

def get_budgets():
    return budgets

def set_budget(category, amount):
    budgets[category] = amount
    
# Home Page
def get_recent_transactions(n=5):
    return sorted(transactions, key=lambda t: t.get("date", ""), reverse=True)[:n]

def get_transactions_by_date(date_str):
    return [t for t in transactions if t.get("date") == date_str]

def get_weekly_totals():
    today = datetime.now().date()
    result = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        day_transactions = [t for t in transactions if t.get("date") == day_str]
        income = sum(t["amount"] for t in day_transactions if t["type"] == "income")
        expense = sum(t["amount"] for t in day_transactions if t["type"] == "expense")
        result.append({
            "day": day.strftime("%a"),
            "date": day_str,
            "income": income,
            "expense": expense
        })
    return result

def get_today_stats():
    today = date.today()
    today_t = [t for t in transactions if date.fromisoformat(t.get("date")) == today]
    income = sum(t["amount"] for t in today_t if t["type"] == "income")
    expense = sum(t["amount"] for t in today_t if t["type"] == "expense")
    return {"income": income, "expense": expense}

#end of homepage