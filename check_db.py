import sqlite3

def print_database():
    conn = sqlite3.connect('cnic_database.db')
    c = conn.cursor()
    
    # Print all records
    c.execute("SELECT * FROM guests")
    print("\nCurrent Database Contents:")
    print("ID | CNIC | Name | Status | Added At")
    print("-"*60)
    for row in c.fetchall():
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")
    
    # Print count
    c.execute("SELECT COUNT(*) FROM guests")
    print(f"\nTotal records: {c.fetchone()[0]}")
    conn.close()

if __name__ == '__main__':
    print_database()