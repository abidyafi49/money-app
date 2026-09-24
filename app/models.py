import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'transactions.json')

transactions = []

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
        "category": category
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
    totals = {}
    for t in transactions:
        if t["type"] == "expense":
            category = t["category"]
            if category in totals:
                totals[category] += t["amount"]
            else:
                totals[category] = t["amount"]
    return totals

def show_category_totals():
    totals = spending_by_category()
    for category, amount in totals.items():
        print(category, ":", amount)