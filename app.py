import json

transactions = []

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
    
def show_transactions():
    for t in transactions:
        print(t["type"], "-", t["amount"], "-", t["category"])
        
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
        
def save_transactions():
    with open("transactions.json", "w") as file:
        json.dump(transactions, file)
        
def load_transactions():
    global transactions
    try:
        with open("transactions.json", "r") as file:
            transactions = json.load(file)
    except FileNotFoundError:
        transactions = []
        
    for i,t in enumerate(transactions):
        if "id" not in t:
            t["id"] = i+1
    save_transactions()
    
def get_transaction(t_id):
    for t in transactions:
        if t["id"] == t_id:
            return t
    return None

def delete_transaction(t_id):
    global transactions
    transactions = [t for t in transactions if t["id"] != t_id]
    
def update_transaction(t_id, amount, t_type, category):
    for t in transactions:
        if t["id"] == t_id:
            t["amount"] = amount
            t["type"] = t_type
            t["category"] = category
            

def get_transactions():
    return transactions
# def main():
#     load_transactions()
#     while True:
#         print("\n1. Add transaction")
#         print("2. Show transactions")
#         print("3. Show balance")
#         print("4. Show category totals")
#         print("5. Quit")
#         choice = input("Choose an option: ")
        
#         if choice == "1":
#             amount = float(input("Amount: "))
#             t_type = input("Type (income/expense): ")
#             category = input("Category: ")
#             add_transaction(amount, t_type, category)
#             save_transactions()
            
#         elif choice == "2":
#             show_transactions()
#         elif choice == "3":
#             print("Balance:", get_balance())
#         elif choice == "4":
#             show_category_totals()
#         elif choice == "5":
#             break
#         else:
#             print("Invalid option, try again.")
            
            
            