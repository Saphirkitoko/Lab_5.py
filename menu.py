import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('record_holders.db')
cursor = conn.cursor()

# Create a table to store record holders
cursor.execute('''
CREATE TABLE IF NOT EXISTS record_holders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    catches INTEGER NOT NULL
)
''')

# Commit the changes
conn.commit()

def display_all_records():
    cursor.execute('SELECT * FROM record_holders')
    records = cursor.fetchall()
    if records:
        for record in records:
            print(f"ID: {record[0]}, Name: {record[1]}, Catches: {record[2]}")
    else:
        print("No records found.")

def search_by_name():
    name = input("Enter the name of the record holder: ")
    cursor.execute('SELECT * FROM record_holders WHERE name = ?', (name,))
    record = cursor.fetchone()
    if record:
        print(f"ID: {record[0]}, Name: {record[1]}, Catches: {record[2]}")
    else:
        print(f"No record found for '{name}'.")

def add_new_record():
    name = input("Enter the name of the new record holder: ")
    catches = int(input("Enter the number of catches: "))
    try:
        cursor.execute('INSERT INTO record_holders (name, catches) VALUES (?, ?)', (name, catches))
        conn.commit()
        print(f"Record for {name} added successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: A record for '{name}' already exists.")

def update_catches():
    name = input("Enter the name of the record holder to update: ")
    cursor.execute('SELECT * FROM record_holders WHERE name = ?', (name,))
    record = cursor.fetchone()
    if record:
        new_catches = int(input(f"Enter the new number of catches for {name}: "))
        cursor.execute('UPDATE record_holders SET catches = ? WHERE name = ?', (new_catches, name))
        conn.commit()
        print(f"Updated {name}'s number of catches to {new_catches}.")
    else:
        print(f"No record found for '{name}'.")

def delete_record():
    name = input("Enter the name of the record holder to delete: ")
    cursor.execute('SELECT * FROM record_holders WHERE name = ?', (name,))
    record = cursor.fetchone()
    if record:
        cursor.execute('DELETE FROM record_holders WHERE name = ?', (name,))
        conn.commit()
        print(f"Record for {name} deleted.")
    else:
        print(f"No record found for '{name}'.")

def main():
    menu_text = """
    1. Display all records
    2. Search for a record holder by name
    3. Add a new record holder
    4. Update the number of catches for a record holder
    5. Delete a record holder
    6. Quit
    """

    while True:
        print(menu_text)
        choice = input("Enter your choice: ")

        if choice == '1':
            display_all_records()
        elif choice == '2':
            search_by_name()
        elif choice == '3':
            add_new_record()
        elif choice == '4':
            update_catches()
        elif choice == '5':
            delete_record()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()

# Close the connection when done
conn.close()