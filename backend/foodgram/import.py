# import csv
# import sqlite3
#
# # con = sqlite3.connect(r'D:\Dev\foodgram-project-react\backend\foodgram\db.sqlite3')
# con = sqlite3.connect(r'D:/Dev/foodgram-project-react/backend/foodgram/db.sqlite3')
# cur = con.cursor()
# cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cur.fetchall())
#
# con.commit()
# con.close()



import psycopg2
import csv


# установите соединение с базой данных PostgreSQL
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()


# откройте файл .csv и прочитайте его с помощью библиотеки csv
with open('ingredients.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # пропустите заголовок столбца
    for row in reader:
        # выполните вставку строки в таблицу
        cur.execute("INSERT INTO recipes_ingredient (name, measurement_unit) VALUES (%s, %s)", row)


# сохраните изменения в базе данных и закройте соединение
conn.commit()
cur.close()
conn.close()
