import mysql.connector
from mysql.connector import Error

for i in range(0,5):
    connection = mysql.connector.connect(host='127.0.0.1',database='sakila',user='root',password='')
    try:
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("SELECT inventory_id FROM inventory order by rand() limit 1")
            inventoryID = str(cursor.fetchone()[0])
            print(inventoryID)
            cursor.execute("SELECT customer_id FROM customer order by rand() limit 1")
            customerID = str(cursor.fetchone()[0])
            print(customerID)
            cursor.execute("select from_unixtime(unix_timestamp('2020-1-1') + floor(rand() * (unix_timestamp('2020-6-3') - unix_timestamp('2020-1-1') + 1)))")
            createDate = str(cursor.fetchone()[0])
            print(createDate)
            insert_stmt = ("INSERT into rental(rental_date, inventory_id, customer_id, return_date, staff_id, last_update, created_date, order_confirmed_date, order_rejected_date, return_inspected_date) SELECT NULL, %s,%s,NULL,(SELECT staff_id FROM staff, (SELECT store_id FROM inventory where inventory.inventory_id=%s) as fitStoreId Where fitStoreId.store_id=staff.store_id order by rand()  limit 1),%s,%s,NULL,NULL,NULL;""VALUES(%s,%s,%s,%s,%s)")
            data = ((inventoryID, customerID, inventoryID, createDate, createDate))
            cursor.execute(insert_stmt,data)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")