from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
import os
import csv
import csv
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'REPLACE_WITH_A_SECURE_RANDOM_KEY'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
from werkzeug.security import generate_password_hash, check_password_hash
# User model for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            user = cursor.fetchone()
            if user:
                return User(user['id'], user['username'], user['password_hash'])
        return None

    @staticmethod
    def get_by_username(username):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()
            if user:
                return User(user['id'], user['username'], user['password_hash'])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Username and password required.')
            return redirect(url_for('register'))
        if User.get_by_username(username):
            flash('Username already exists.')
            return redirect(url_for('register'))
        password_hash = generate_password_hash(password)
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', (username, password_hash))
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('login'))

DB_FILE = "tracker_data.db"
DATA_FILE = "tracker_data.json"  # Keep for backward compatibility
CSV_FILE = "tracker_data.csv"

@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), cursor_factory=RealDictCursor)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Initialize the PostgreSQL database with required tables."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        # Create transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount INTEGER NOT NULL,
                type TEXT CHECK(type IN ('earning','expense')) NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()

def save_record_to_db(earning_items, total_earning, expense_items, total_expenses):
    """Save record to SQLite database."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Insert into records table
    # This function will be replaced with transaction-based logic and user_id support.
    pass

def load_existing_data():
    """Load existing data from JSON file (for backward compatibility)."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"records": []}
    return {"records": []}

def export_to_csv():
    """Export all records from database to CSV file."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM records ORDER BY date')
            records = cursor.fetchall()
            
            if not records:
                return False
            
            with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Earnings", "Total Earning", "Expenses", "Total Expenses", "Net"])
                
                for record in records:
                    record_id = record['id']
                    
                    # Fetch earnings and expenses for this record
                    cursor.execute('SELECT name, amount FROM earnings WHERE record_id = %s', (record_id,))
                    earnings = cursor.fetchall()
                    earnings_str = ", ".join([f"{e['name']}: {e['amount']}" for e in earnings])
                    
                    cursor.execute('SELECT name, amount FROM expenses WHERE record_id = %s', (record_id,))
                    expenses = cursor.fetchall()
                    expenses_str = ", ".join([f"{e['name']}: {e['amount']}" for e in expenses])
                    
                    writer.writerow([
                        record['date'],
                        earnings_str,
                        record['total_earning'],
                        expenses_str,
                        record['total_expenses'],
                        record['net']
                    ])
            
            return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False

@app.route('/')
@login_required
def home():
    """Display the main form page."""
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html', user=current_user)

@app.route('/calculate', methods=['POST'])
@login_required
def calculate():
    """Process the form data and calculate the summary."""
    try:
        # Get all form data
        form_data = request.form.to_dict()
        
        # Parse earnings
        earning_items = []
        for key, value in form_data.items():
            if key.startswith('earning_name_'):
                item_id = key.replace('earning_name_', '')
                amount_key = f'earning_amount_{item_id}'
                
                if amount_key in form_data:
                    name = value.strip()
                    amount = int(form_data[amount_key] or 0)
                    
                    if name and amount > 0:
                        earning_items.append({"name": name, "amount": amount})
        
        # Parse expenses
        expense_items = []
        for key, value in form_data.items():
            if key.startswith('expense_name_'):
                item_id = key.replace('expense_name_', '')
                amount_key = f'expense_amount_{item_id}'
                
                if amount_key in form_data:
                    name = value.strip()
                    amount = int(form_data[amount_key] or 0)
                    
                    if name and amount > 0:
                        expense_items.append({"name": name, "amount": amount})
        
        # Calculate totals
        total_earning = sum(item['amount'] for item in earning_items)
        total_expenses = sum(item['amount'] for item in expense_items)
        net = total_earning - total_expenses
        
        # Determine status
        if total_earning > total_expenses:
            status = "✅ Your earning is greater than your expenses. So financially good day!"
            status_color = "green"
        elif total_earning < total_expenses:
            status = "🚨 Your expenses are greater than your earnings. Be careful!"
            status_color = "red"
        else:
            status = "⚖️ Your earnings and expenses are equal."
            status_color = "blue"
        
        # Save transactions for the logged-in user
        with get_db() as conn:
            cursor = conn.cursor()
            user_id = current_user.id
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for item in earning_items:
                cursor.execute('''
                    INSERT INTO transactions (date, description, amount, type, user_id)
                    VALUES (%s, %s, %s, 'earning', %s)
                ''', (now, item['name'], item['amount'], user_id))
            for item in expense_items:
                cursor.execute('''
                    INSERT INTO transactions (date, description, amount, type, user_id)
                    VALUES (%s, %s, %s, 'expense', %s)
                ''', (now, item['name'], item['amount'], user_id))
        
        # Prepare data to send to results page
        result_data = {
            "earning_items": earning_items,
            "total_earning": total_earning,
            "expense_items": expense_items,
            "total_expenses": total_expenses,
            "net": net,
            "status": status,
            "status_color": status_color
        }
        
        return render_template('results.html', data=result_data)
    
    except Exception as e:
        return render_template('error.html', error_message=str(e))

@app.route('/history')
def history():
    """Display all saved records from database."""
    try:
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        with get_db() as conn:
            cursor = conn.cursor()
            user_id = current_user.id
            cursor.execute('''
                SELECT id, date, description, amount, type
                FROM transactions
                WHERE user_id = %s
                ORDER BY date DESC
            ''', (user_id,))
            all_transactions = cursor.fetchall()
            # Aggregate by date, keeping transaction objects with IDs
            history = {}
            for txn in all_transactions:
                date = txn['date']
                if date not in history:
                    history[date] = {'earnings': [], 'expenses': [], 'total_earning': 0, 'total_expenses': 0}
                txn_obj = dict(txn)  # Convert sqlite3.Row to dict
                if txn['type'] == 'earning':
                    history[date]['earnings'].append(txn_obj)
                    history[date]['total_earning'] += txn['amount']
                else:
                    history[date]['expenses'].append(txn_obj)
                    history[date]['total_expenses'] += txn['amount']
            # Prepare records for template
            records = []
            for date, data in history.items():
                net = data['total_earning'] - data['total_expenses']
                records.append({
                    'date': date,
                    'earnings': data['earnings'],
                    'expenses': data['expenses'],
                    'total_earning': data['total_earning'],
                    'total_expenses': data['total_expenses'],
                    'net': net
                })
            return render_template('history.html', records=records)
    except Exception as e:
        return render_template('error.html', error_message=str(e))

# Edit transaction route
@app.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions WHERE id = %s AND user_id = %s', (transaction_id, current_user.id))
        transaction = cursor.fetchone()
        if not transaction:
            flash('Transaction not found.')
            return redirect(url_for('history'))
        if request.method == 'POST':
            description = request.form['description']
            amount = request.form['amount']
            cursor.execute('UPDATE transactions SET description = %s, amount = %s WHERE id = %s', (description, amount, transaction_id))
            flash('Transaction updated.')
            return redirect(url_for('history'))
        return render_template('edit_transaction.html', transaction=transaction)

# Delete transaction route
@app.route('/delete/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM transactions WHERE id = %s AND user_id = %s', (transaction_id, current_user.id))
        flash('Transaction deleted.')
    return redirect(url_for('history'))

if __name__ == '__main__':
    init_db()  # Initialize database on startup
    app.run(debug=True, port=5000)
