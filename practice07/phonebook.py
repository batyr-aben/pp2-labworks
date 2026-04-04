import csv
from connect import get_connection


def insert_from_csv(file_path):
    
    conn, cur = get_connection()  
    with open(file_path, "r") as file:  
        reader = csv.DictReader(file)  
        for row in reader:  
            
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row["name"], row["phone"])
            )
    conn.commit()  
    cur.close()
    conn.close()



def insert_from_console():
    
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn, cur = get_connection()
    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()



def update_contact():
    
    conn, cur = get_connection()
    name = input("Enter contact name for update: ")
    choice = input("What to update 1) Name 2) Phone: ")
    if choice == "1":
        new_name = input("New name: ")
        cur.execute(
            "UPDATE phonebook SET name=%s WHERE name=%s",
            (new_name, name)
        )
    elif choice == "2":
        new_phone = input("New name: ")
        cur.execute(
            "UPDATE phonebook SET phone=%s WHERE name=%s",
            (new_phone, name)
        )
    conn.commit()
    cur.close()
    conn.close()



def search_contacts():
    
    conn, cur = get_connection()
    choice = input("Search by: 1) Name 2) Phone prefix: ")
    if choice == "1":
        name = input("Enter name: ")
        cur.execute("SELECT * FROM phonebook WHERE name=%s", (name,))
    elif choice == "2":
        prefix = input("Enter phone prefix: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (prefix+"%",))
    rows = cur.fetchall()  
    for row in rows:
        print(row)
    cur.close()
    conn.close()



def delete_contact():
   
    
    conn, cur = get_connection()
    choice = input("Delete by: 1) Name 2) Phone: ")
    if choice == "1":
        name = input("Enter name: ")
        cur.execute("DELETE FROM phonebook WHERE name=%s", (name,))
    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    conn.commit()
    cur.close()
    conn.close()



def main():
    while True:
        print("\nМеню:")
        print("1. Add contact from CSV")
        print("2. Add contact by hand")
        print("3. Update")
        print("4. Search")
        print("5. Delete")
        print("6. Quit")
        choice = input("Choice: ")
        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            break
        else:
            print("Incorrect choice, try again")
