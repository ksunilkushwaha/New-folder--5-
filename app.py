from flask import Flask, render_template, request, jsonify
import json
import os
import csv
import sqlite3
from datetime import datetime
from contextlib import contextmanager

app = Flask(__name__)

DB_FILE = "tracker_data.db"
DATA_FILE = "tracker_data.json"  # Keep for backward compatibility
CSV_FILE = "tracker_data.csv"

@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Initialize the SQLite database with required tables."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Create records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total_earning INTEGER NOT NULL,
                total_expenses INTEGER NOT NULL,
                net INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create earnings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS earnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                amount INTEGER NOT NULL,
                FOREIGN KEY (record_id) REFERENCES records (id) ON DELETE CASCADE
            )
        ''')
        
        # Create expenses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                amount INTEGER NOT NULL,
                FOREIGN KEY (record_id) REFERENCES records (id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()

def save_record_to_db(earning_items, total_earning, expense_items, total_expenses):
    """Save record to SQLite database."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Insert into records table
        cursor.execute('''
            INSERT INTO records (date, total_earning, total_expenses, net)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total_earning, total_expenses, total_earning - total_expenses))
        
        record_id = cursor.lastrowid
        
        # Insert earnings
        for item in earning_items:
            cursor.execute('''
                INSERT INTO earnings (record_id, name, amount)
                VALUES (?, ?, ?)
            ''', (record_id, item['name'], item['amount']))
        
        # Insert expenses
        for item in expense_items:
            cursor.execute('''
                INSERT INTO expenses (record_id, name, amount)
                VALUES (?, ?, ?)
            ''', (record_id, item['name'], item['amount']))
        
        conn.commit()

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
                    cursor.execute('SELECT name, amount FROM earnings WHERE record_id = ?', (record_id,))
                    earnings = cursor.fetchall()
                    earnings_str = ", ".join([f"{e['name']}: {e['amount']}" for e in earnings])
                    
                    cursor.execute('SELECT name, amount FROM expenses WHERE record_id = ?', (record_id,))
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
def home():
    """Display the main form page."""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
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
        
        # Save data to database
        save_record_to_db(earning_items, total_earning, expense_items, total_expenses)
        export_to_csv()  # Also export to CSV for backup
        
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
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM records ORDER BY date DESC')
            db_records = cursor.fetchall()
            
            # Reconstruct records with earnings and expenses
            records = []
            for record in db_records:
                record_id = record['id']
                
                # Fetch earnings
                cursor.execute('SELECT name, amount FROM earnings WHERE record_id = ? ORDER BY id', (record_id,))
                earnings = [dict(row) for row in cursor.fetchall()]
                
                # Fetch expenses
                cursor.execute('SELECT name, amount FROM expenses WHERE record_id = ? ORDER BY id', (record_id,))
                expenses = [dict(row) for row in cursor.fetchall()]
                
                records.append({
                    'date': record['date'],
                    'earnings': earnings,
                    'expenses': expenses,
                    'total_earning': record['total_earning'],
                    'total_expenses': record['total_expenses'],
                    'net': record['net']
                })
            
            return render_template('history.html', records=records)
    except Exception as e:
        print(f"Error loading history: {e}")
        return render_template('history.html', records=[])

if __name__ == '__main__':
    init_db()  # Initialize database on startup
    app.run(debug=True, port=5000)
