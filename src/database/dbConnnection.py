from psycopg2 import connect

def get_Connection():
    try:    
        conn = connect(host='localhost',port='5432',dbname='ECommerceUsersDB',user='postgres',password='abc123')
        return conn
    except Exception as error:
        print("Error : ",error)