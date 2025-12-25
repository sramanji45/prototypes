import mysql.connector
import time

# ProxySQL connection details
config = {
    'user': 'root',
    'password': 'root123',       # Must match what you put in mysql_users in proxysql.cnf
    'host': '127.0.0.1',         # Your local machine (mapping to proxysql:6033)
    'port': 6033,                # PROXYSQL TRAFFIC PORT
    'database': 'master_replicas_db'
}

def run_test():
    try:
        # 1. Connect to ProxySQL
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        print("--- Connected to ProxySQL ---")

        # 2. PERFORM A WRITE
        """
        print("\n[Write] Writing new character...")
        insert_query = "INSERT INTO Bahubali (fname, lname, role, salary) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, ("Sathya", "Raj", "Kattappa", 95000.00))
        conn.commit()
        print("Write successful!")
        """
        print("\n[Write] Writing new character...")
        insert_query = "INSERT INTO Bahubali (fname, lname, role, salary) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, ("Ramya", "Krishna", "Shivagami", 95000.00))
        conn.commit()
        print("Write successful!")

        # Wait for replication
        time.sleep(1)

        # 3. PERFORM A READ
        print("\n[Read] Fetching data...")
        cursor.execute("SELECT @@server_id, fname, lname FROM Bahubali ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()

        if result:
            print(f"Data received from Server ID: {result['@@server_id']}")
            print(f"Name: {result['fname']} {result['lname']}")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    run_test()