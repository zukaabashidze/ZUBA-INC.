from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Post, Transaction, ContactMessage, db
from forms import ContactForm, TransactionForm

main = Blueprint('main', __name__)

@main.route('/')
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', posts=posts)

@main.route('/about')
def about(): return render_template('about.html')

@main.route('/how-it-works')
def how_it_works(): return render_template('how_it_works.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('შეტყობინება წარმატებით გაიგზავნა', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    form = TransactionForm()
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).all()

    from decimal import Decimal
    balance = current_user.balance if hasattr(current_user, 'balance') else Decimal('0.00')
    income = sum((t.amount for t in transactions if t.amount >= 0), Decimal('0.00'))
    expense = sum((t.amount for t in transactions if t.amount < 0), Decimal('0.00'))

    balance_str = f"{balance:.2f}"
    income_str = f"{income:.2f}"
    expense_str = f"{(-expense):.2f}" if expense < 0 else "0.00"

    return render_template('dashboard.html', transactions=transactions, form=form,
                           balance=balance_str, income=income_str, expense=expense_str)

@main.route('/add-transaction', methods=['POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        # keep Decimal precision from form
        amount = form.amount.data
        description = form.description.data or ''
        t = Transaction(user_id=current_user.id, amount=amount, description=description)
        db.session.add(t)
        db.session.commit()
        flash('ტრანზაქცია დამატებულია', 'success')
    else:
        flash('არასწორი მონაცემები ტრანზაქციისთვის', 'danger')
    return redirect(url_for('main.dashboard'))

