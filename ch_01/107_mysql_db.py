import pymysql

db_conf = {
    "host": "127.0.0.1",
    "user": "test",
    "password": "test11",
    "database": "temp",
}

con = pymysql.connect(**db_conf)

# 테이블 생성
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS stocks")
cur.execute(
    """
        CREATE TABLE stocks (
            date VARCHAR(10),
            trans VARCHAR(20),
            symbol VARCHAR(10),
            qty INT,
            price INT,
            primary key (date) )
            """
)
con.commit()
con.close()

# insert table
con = pymysql.connect(**db_conf)
cur = con.cursor()
cur.execute(
    """
        INSERT INTO stocks (date, trans, symbol, qty, price)
        VALUES (%s, %s, %s ,%s, %s)
        """, ("2019-10-12", "sell", "K029093", 6 ,10000)
)
con.commit()
con.close()

# SELECT
con = pymysql.connect(**db_conf)
cur = con.cursor()
cur.execute("SELECT * FROM stocks")
df = cur.fetchall()
con.commit()
con.close()

print(df)


# 2) pandas_mysql
import pandas as pd
import pymysql
from sqlalchemy import create_engine

pymysql.install_as_MySQLdb()
engine = create_engine("mysql://test:test11@localhost/temp")
con = engine.connect()
test1 = pd.DataFrame({"a":[1,2,3,4]})
test1.to_sql('test1', con, if_exists="append", index=False)
con.close()


