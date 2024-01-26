import sqlite3

def view_database():
    connection = sqlite3.connect("votes.db")
    cursor = connection.cursor()

    # Execute a SELECT query to retrieve all data from the 'votes' table
    cursor.execute("SELECT * FROM votes")
    rows = cursor.fetchall()

    if not rows:
        print("No data in the 'votes' table.")
    else:
        print("ID\tParty Name")
        print("-" * 20)
        for row in rows:
            print(f"{row[0]}\t{row[1]}")

    connection.close()

if __name__ == "__main__":
    view_database()
