#!/usr/bin/env python3
"""
Migration script: Import existing JSON data into SQLite database.
Run this once to transfer all historical data from tracker_data.json to tracker_data.db
"""

import json
import sqlite3
import os

DB_FILE = "tracker_data.db"
JSON_FILE = "tracker_data.json"

def migrate():
    """Migrate data from JSON to SQLite."""
    
    # Check if JSON file exists
    if not os.path.exists(JSON_FILE):
        print(f"✓ No {JSON_FILE} file found. Nothing to migrate.")
        return
    
    # Load JSON data
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"✗ Error reading {JSON_FILE}: {e}")
        return
    
    records = data.get("records", [])
    if not records:
        print("✓ No records found in JSON. Nothing to migrate.")
        return
    
    # Connect to database
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Check if records already exist
        cursor.execute('SELECT COUNT(*) FROM records')
        existing_count = cursor.fetchone()[0]
        
        if existing_count > 0:
            print(f"✗ Database already has {existing_count} records. Migration aborted to avoid duplicates.")
            print("   If you want to start fresh, delete tracker_data.db and run this script again.")
            conn.close()
            return
        
        # Migrate records
        migrated = 0
        for record in records:
            try:
                # Insert record
                cursor.execute('''
                    INSERT INTO records (date, total_earning, total_expenses, net)
                    VALUES (?, ?, ?, ?)
                ''', (
                    record.get('date'),
                    record.get('total_earning', 0),
                    record.get('total_expenses', 0),
                    record.get('net', 0)
                ))
                
                record_id = cursor.lastrowid
                
                # Insert earnings
                for earning in record.get('earnings', []):
                    cursor.execute('''
                        INSERT INTO earnings (record_id, name, amount)
                        VALUES (?, ?, ?)
                    ''', (record_id, earning.get('name'), earning.get('amount', 0)))
                
                # Insert expenses
                for expense in record.get('expenses', []):
                    cursor.execute('''
                        INSERT INTO expenses (record_id, name, amount)
                        VALUES (?, ?, ?)
                    ''', (record_id, expense.get('name'), expense.get('amount', 0)))
                
                migrated += 1
            except Exception as e:
                print(f"⚠ Error migrating record {record.get('date')}: {e}")
                conn.rollback()
                continue
        
        conn.commit()
        conn.close()
        
        print(f"✓ Migration completed! {migrated} records imported to {DB_FILE}")
        
    except Exception as e:
        print(f"✗ Error during migration: {e}")
        return

if __name__ == '__main__':
    print("=" * 50)
    print("JSON to SQLite Migration")
    print("=" * 50)
    migrate()
    print("=" * 50)
