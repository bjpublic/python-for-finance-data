import FinanceDataReader as fdr
import pymysql
from tqdm import tqdm
from datetime import datetime

db_conf = {
    "host": "127.0.0.1",
    "user": "test",
    "password": "test11",
    "database": "finance",
}

def create_table(db_conf):

    con = pymysql.connect(**db_conf)
    cur = con.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS STOCK_CODE (
        symbol VARCHAR(6),
        name VARCHAR(30),
        sector VARCHAR(40),
        industry VARCHAR(200),
        collected_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        primary key (symbol))
        """)

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS STOCK_DATA (
        date VARCHAR(10),
        open int,
        high int,
        low int,
        close int,
        volume int,
        change_rate float,
        symbol VARCHAR(6),
        collected_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        primary key (date, symbol))
        """
    )

    con.commit()
    con.close()

    return 0

def insert_code(df):

    con = pymysql.connect(**db_conf)
    cur = con.cursor()

    for symbol, name, sector, industry in zip(df["Symbol"], df["Name"], df["Sector"], df["Industry"]):
        cur.execute(
            """
            REPLACE INTO STOCK_CODE (symbol, name, sector, industry) VALUES (%s, %s, %s, %s)
            """, (symbol, name, sector, industry))

    con.commit()
    con.close()

    return 0

def insert_stock_data(db_conf, symbol, df):

    df = df.reset_index(drop=False)
    df["Date"] = df["Date"].astype(str)
    df["Change"] = df["Change"].fillna(0)

    con = pymysql.connect(**db_conf)
    cur = con.cursor()

    for date, open, high, low, close, volume, change in zip(df["Date"], df["Open"], df["High"], df["Low"], df["Close"], df["Volume"], df["Change"]):
        cur.execute(
            """
            REPLACE INTO STOCK_DATA (date, open, high, low, close, volume, change_rate, symbol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (date, open, high, low, close, volume, change, symbol))

    con.commit()
    con.close()

    return 0

def stock_data_collect(year):
    create_table(db_conf)
    df_krx = fdr.StockListing('KRX')
    df_krx = df_krx.fillna("")
    insert_code(df_krx)

    # 주가 데이터
    # symbol='005930'
    # year="2017"

    symbol_list = df_krx["Symbol"]

    for symbol in tqdm(symbol_list):
        try:
            df_sto = fdr.DataReader(symbol, year)
            insert_stock_data(db_conf, symbol, df_sto)
        except Exception as e:
            print(symbol, end=",")
            print(e)

    return 0


if __name__ == '__main__':

    year = str(datetime.now().year)
    stock_data_collect(year)
