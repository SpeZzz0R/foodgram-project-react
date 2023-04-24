import csv
import sqlite3


con = sqlite3.connect(r'D:/Dev/foodgram-project-react/backend/foodgram/db.sqlite3')
# con = sqlite3.connect(r'D:\Dev\foodgram-project-react\backend\foodgram\db.sqlite3')
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall())

con.commit()
con.close()
