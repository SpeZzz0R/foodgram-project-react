import psycopg2
import csv


conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="postgres",
    host="db",
    port="5432"
)
cur = conn.cursor()


with open('ingredients.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cur.execute(
            "INSERT INTO recipes_ingredient ("
            "name, measurement_unit) VALUES (%s, %s)", row
        )

conn.commit()
cur.close()
conn.close()
