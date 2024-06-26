from database.dbConnnection import get_Connection
from psycopg2 import extras
def pushQuery(query:str,queryTuple:tuple)->dict:
    conn = get_Connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute(query,queryTuple)
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return result
