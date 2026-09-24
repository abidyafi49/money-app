from flask import Flask, render_template, request, redirect
from app import add_transaction, get_balance, load_transactions, get_transactions, get_transaction, save_transactions, spending_by_category, delete_transaction, update_transaction

app = Flask(__name__)

@app.route("/")
def home():
    load_transactions()
    balance = get_balance()
    totals = spending_by_category()
    return render_template("index.html", balance=balance, transactions= get_transactions(), totals = totals)

@app.route("/add", methods=["POST"])
def add():
    amount = float(request.form["amount"])
    t_type = request.form["t_type"]
    category = request.form["category"]
    add_transaction(amount, t_type, category)
    save_transactions()
    return redirect("/")

@app.route("/delete/<int:t_id>")
def delete(t_id):
    load_transactions()
    delete_transaction(t_id)
    save_transactions()
    return redirect("/")

@app.route("/edit/<int:t_id>")
def edit_form(t_id):
    load_transactions()
    transaction = get_transaction(t_id)
    return render_template("edit.html", transaction=transaction)

@app.route("/update/<int:t_id>", methods=["POST"])
def update(t_id):
    load_transactions()
    amount = float(request.form["amount"])
    t_type = request.form["t_type"]
    category = request.form["category"]
    update_transaction(t_id, amount, t_type, category)
    save_transactions()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)