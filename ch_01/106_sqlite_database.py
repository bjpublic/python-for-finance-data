# 1) DB 연결하고, SQL실행하기
import sqlite3
conn = sqlite3.connect("test.db")

c = conn.cursor()
c.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')

conn.commit()
conn.close()


# 2) 판다스 데이터 프레임 만들고 DB에 테이블로 저장하기
import sqlite3
con = sqlite3.connect("test.db")


import pandas as pd

df = pd.DataFrame({"a":[1,2,3],
                   "b":[4,5,6],
                   "id":["a", "b","c"]})

df.to_sql("df", con)


# 3) UNIQUE 인덱스 생성하기
con = sqlite3.connect("test.db")
df = pd.DataFrame({"a":[1,2,3],
                   "b":[4,5,6],
                   "id":["a", "b","c"]})

df.to_sql("df", con, index=False, if_exists="replace")
c = con.cursor()
c.execute("CREATE UNIQUE INDEX id ON df (id)")
con.commit()
con.close()


# 4) 인덱스 확인하기
con = sqlite3.connect("test.db")
c = con.cursor()
c.execute("PRAGMA index_list(df)").fetchall()
c.execute("PRAGMA index_info('id')").fetchall()
con.close()

# 5) 추가 데이터 저장하기 -> 에러가 발생합니다.
df_2 = pd.DataFrame({"a":[4], "b":[4], "id":["c"]})

df_2 = df_2.set_index("id")
con = sqlite3.connect("test.db")
df_2.to_sql("df", con, if_exists="append")


# 6) REPLACE INTO로 넣기
con = sqlite3.connect("test.db")
c =con.cursor()
c.execute("REPLACE INTO df (a, b, id) VALUES (?, ?, ?)", (4, 4, "c"))
con.commit()
con.close()

# 7) read_sql함수 이용하기
con = sqlite3.connect("test.db")
temp = pd.read_sql("SELECT * FROM df", con)
print(temp)
con.close()
