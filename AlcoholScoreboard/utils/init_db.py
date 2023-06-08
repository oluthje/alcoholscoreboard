import psycopg2
import os
import csv

from dotenv import load_dotenv
from choices import df

csv_file_path = "C:/Users/juand/OneDrive/Documents/DIS/alcoholscoreboard/AlcoholScoreboard/dataset/drinks.csv"

load_dotenv()

if __name__ == '__main__':
    conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD')
    )
    with conn.cursor() as cur:
        # Run users.sql
        with open('users.sql') as db_file:
            cur.execute(db_file.read())
        # Run produce.sql
        with open('produce.sql') as db_file:
            cur.execute(db_file.read())
        # Run countries.sql
        with open('countries.sql') as db_file:
            cur.execute(db_file.read())

        # Import all produce from the dataset
        all_produce = list(
            map(lambda x: tuple(x),
                df[['category', 'item', 'unit', 'variety', 'price']].to_records(index=False))
        )
        args_str = ','.join(cur.mogrify("(%s, %s, %s, %s, %s)", i).decode('utf-8') for i in all_produce)
        cur.execute("INSERT INTO Produce (category, item, unit, variety, price) VALUES " + args_str)

        # Dummy farmer 1 sells all produce
        dummy_sales = [(1, i) for i in range(1, len(all_produce) + 1)]
        args_str = ','.join(cur.mogrify("(%s, %s)", i).decode('utf-8') for i in dummy_sales)
        cur.execute("INSERT INTO Sell (farmer_pk, produce_pk) VALUES " + args_str)
        
        with open(csv_file_path, "r") as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                if "'" in row[0]:
                    row[0] = row[0].replace("'", "")

                sql = f"INSERT INTO Countries(n_country,continent) VALUES ('{row[0]}', '{row[5]}');"
                cur.execute(sql)

        conn.commit()

    conn.close()
