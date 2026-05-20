import sqlite3
import json

def dump_data():
    conn = sqlite3.connect('pablo.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    tables = ['users', 'cars', 'bookings', 'messages', 'reviews']
    data = {}
    
    for table in tables:
        try:
            c.execute(f"SELECT * FROM {table}")
            rows = c.fetchall()
            data[table] = [dict(row) for row in rows]
        except Exception as e:
            data[table] = f"Error: {str(e)}"
            
    conn.close()
    return data

if __name__ == '__main__':
    data = dump_data()
    # Print a summary
    for table, rows in data.items():
        if isinstance(rows, list):
            print(f"Table: {table} ({len(rows)} records)")
            if len(rows) > 0:
                # Print keys
                print("Columns:", list(rows[0].keys()))
                # Print first 3 rows as samples
                for idx, row in enumerate(rows[:5]):
                    # Mask password for security if users table
                    display_row = dict(row)
                    if 'password' in display_row:
                        display_row['password'] = '********'
                    print(f"  Row {idx+1}: {display_row}")
            else:
                print("  No records.")
        else:
            print(f"Table: {table} - {rows}")
        print("-" * 50)
