from flask import Flask, render_template, request, jsonify
import json
import os
import csv
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "tracker_data.json"
CSV_FILE = "tracker_data.csv"

def load_existing_data():
    """Load existing data from the file if it exists."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"records": []}
    return {"records": []}

def save_data_to_file(earning_items, total_earning, expense_items, total_expenses):
    """Save the items and totals to a JSON file."""
    data = load_existing_data()
    
    record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "earnings": earning_items,
        "total_earning": total_earning,
        "expenses": expense_items,
        "total_expenses": total_expenses,
        "net": total_earning - total_expenses
    }
    
    data.setdefault("records", []).append(record)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def export_to_csv():
    """Export all saved data from JSON to CSV file."""
    data = load_existing_data()
    
    if not data.get("records"):
        return False
    
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(["Date", "Earnings", "Total Earning", "Expenses", "Total Expenses", "Net"])
        
        # Write each record
        for record in data.get("records", []):
            earnings_str = ", ".join([f"{e['name']}: {e['amount']}" for e in record.get("earnings", [])])
            expenses_str = ", ".join([f"{e['name']}: {e['amount']}" for e in record.get("expenses", [])])
            
            writer.writerow([
                record.get("date", ""),
                earnings_str,
                record.get("total_earning", 0),
                expenses_str,
                record.get("total_expenses", 0),
                record.get("net", 0)
            ])
    
    return True

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
        
        # Save data to files
        save_data_to_file(earning_items, total_earning, expense_items, total_expenses)
        export_to_csv()
        
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
    """Display all saved records."""
    data = load_existing_data()
    records = data.get("records", [])
    return render_template('history.html', records=records)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
