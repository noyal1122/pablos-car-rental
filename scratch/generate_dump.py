import sqlite3

def generate_markdown():
    conn = sqlite3.connect('pablo.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    tables = ['users', 'cars', 'bookings', 'messages', 'reviews']
    md_content = "# Pablo's Car Rental - Database Dump\n\n"
    md_content += "This document contains a complete dump of all data present in the SQLite database (`pablo.db`).\n\n"
    
    for table in tables:
        c.execute(f"SELECT * FROM {table}")
        rows = c.fetchall()
        
        md_content += f"## Table: `{table}` ({len(rows)} records)\n\n"
        if not rows:
            md_content += "*No records found.*\n\n"
            continue
            
        # Get column names
        columns = list(rows[0].keys())
        
        # Create table header
        md_content += "| " + " | ".join(columns) + " |\n"
        md_content += "| " + " | ".join(["---"] * len(columns)) + " |\n"
        
        # Add table rows
        for row in rows:
            row_dict = dict(row)
            # Mask password in users
            if 'password' in row_dict:
                row_dict['password'] = '********'
                
            row_values = []
            for col in columns:
                val = row_dict[col]
                if val is None:
                    row_values.append("`NULL`")
                else:
                    # Escape vertical pipes in values to prevent broken markdown tables
                    str_val = str(val).replace("|", "\\|").replace("\n", " ")
                    row_values.append(str_val)
            md_content += "| " + " | ".join(row_values) + " |\n"
            
        md_content += "\n"
        
    conn.close()
    
    # Save the markdown dump to artifacts directory
    artifact_path = r"C:\Users\noelp\.gemini\antigravity\brain\fc013206-3e1e-4217-830f-6b06f19d30aa\all_database_data.md"
    with open(artifact_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Database dump saved successfully to {artifact_path}")

if __name__ == '__main__':
    generate_markdown()
