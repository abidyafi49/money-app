from flask import Blueprint, render_template, request, redirect, url_for
from app.models import (
    load_transactions, save_transactions, get_transactions,
    get_transaction, add_transaction, update_transaction,
    delete_transaction, get_balance, spending_by_category
)

main = Blueprint("main", __name__)

@main.route("/")
def home():
    load_transactions()
    balance = get_balance()
    totals = spending_by_category()
    return render_template("index.html", balance=balance,
                           transactions=get_transactions(), totals=totals)

@main.route("/add", methods=["POST"])
def add():
    amount = float(request.form["amount"])
    t_type = request.form["t_type"]
    category = request.form["category"]
    add_transaction(amount, t_type, category)
    save_transactions()
    return redirect(url_for("main.home"))

@main.route("/edit/<int:t_id>")
def edit_form(t_id):
    load_transactions()
    transaction = get_transaction(t_id)
    return render_template("edit.html", transaction=transaction)

@main.route("/update/<int:t_id>", methods=["POST"])
def update(t_id):
    load_transactions()
    amount = float(request.form["amount"])
    t_type = request.form["t_type"]
    category = request.form["category"]
    update_transaction(t_id, amount, t_type, category)
    save_transactions()
    return redirect(url_for("main.home"))

@main.route("/delete/<int:t_id>")
def delete(t_id):
    load_transactions()
    delete_transaction(t_id)
    save_transactions()
    return redirect(url_for("main.home"))