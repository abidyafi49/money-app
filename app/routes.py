from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from app.models import (
    load_transactions, save_transactions, get_transactions,
    get_transaction, add_transaction, update_transaction,
    delete_transaction, get_balance, spending_by_category,
    load_budgets, save_budgets, get_budgets, set_budget,
    get_recent_transactions, get_weekly_totals, get_today_stats,
    get_filtered_transactions, group_transactions_by_date
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
    date_str = request.args.get("date", None)
    date_from = request.args.get("date_from", None)
    date_to = request.args.get("date_to", None)
    
    if date_from or date_to:
        filter_type = "custom"
    
    filtered = get_filtered_transactions(filter_type, date_str, date_from, date_to)
    grouped = group_transactions_by_date(filtered)
    
    total_income = sum(t["amount"] for t in filtered if t["type"] == "income")
    total_expense = sum(t["amount"] for t in filtered if t["type"] == "expense")
    
    return render_template("history.html",
                           grouped=grouped,
                           filter_type=filter_type,
                           date_str=date_str,
                           date_from=date_from,
                           date_to=date_to,
                           total_income=total_income,
                           total_expense=total_expense)

@main.route("/add-page")
def add_page():
    today = datetime.now().isoformat()
    return render_template("add.html")

@main.route("/add", methods=["POST"])
def add():
    amount = float(request.form["amount"])
    t_type = request.form["t_type"]
    category = request.form["category"]
    date = request.form.get("date") or None
    load_transactions()
    add_transaction(amount, t_type, category, date)
    save_transactions()
    return redirect(url_for("main.home"))

@main.route("/edit/<int:t_id>")
def edit_form(t_id):
    load_transactions()
    transaction = get_transaction(t_id)
    today = datetime.now().isoformat()
    return render_template("edit.html", transaction=transaction)

@main.route("/update/<int:t_id>", methods=["POST"])
def update(t_id):
    load_transactions()
    amount = float(request.form["amount"])
    t_type = request.form["t_type"]
    category = request.form["category"]
    date = request.form.get("date") or None
    update_transaction(t_id, amount, t_type, category, date)
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