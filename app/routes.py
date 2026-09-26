from flask import Blueprint, render_template, request, redirect, url_for
from app.models import (
    load_transactions, save_transactions, get_transactions,
    get_transaction, add_transaction, update_transaction,
    delete_transaction, get_balance, spending_by_category,
    load_budgets, save_budgets, get_budgets, set_budget,
    get_recent_transactions, get_weekly_totals, get_today_stats
)

main = Blueprint("main", __name__)

@main.route("/")
def home():
    load_transactions()
    balance = get_balance()
    income = sum(t["amount"] for t in get_transactions() if t["type"] == "income")
    outcome = sum(t["amount"] for t in get_transactions() if t["type"] == "expense")
    recent = get_recent_transactions(5)
    weekly = get_weekly_totals()
    today_stats = get_today_stats()
    return render_template("index.html", balance=balance,
                           transactions=get_transactions(), income=income, outcome=outcome, recent=recent, weekly=weekly, today_stats=today_stats)

@main.route("/history")
def history():
    load_transactions()
    filter_type = request.args.get("filter", "all")
    all_transactions = get_transactions()
    if filter_type == "income":
        filtered = [t for t in all_transactions if t["type"] == "income"]
    elif filter_type == "outcome":
        filtered = [t for t in all_transactions if t["type"] == "expense"]
    else:
        filtered = all_transactions
    return render_template("history.html", transactions=filtered, filter_type=filter_type)

@main.route("/add-page")
def add_page():
    return render_template("add.html")

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

@main.route("/analytics")
def analytics():
    load_transactions()
    load_budgets()
    totals = spending_by_category()
    budgets = get_budgets()
    return render_template("analytics.html", totals=totals, budgets=budgets)

@main.route("/settings", methods=["GET", "POST"])
def settings():
    load_transactions()
    load_budgets()
    if request.method == "POST":
        category = request.form["category"]
        amount = float(request.form["amount"])
        set_budget(category, amount)
        save_budgets()
        return redirect(url_for("main.settings"))
    categories = list(spending_by_category().keys())
    return render_template("settings.html", budgets=get_budgets(), categories=categories)