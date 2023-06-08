import psycopg2
import os

from dotenv import load_dotenv
from choices import df

load_dotenv()



import numpy
from psycopg2.extensions import register_adapter, AsIs
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)



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
        # Run alcohol.sql
        with open('alcohol.sql') as db_file:
            cur.execute(db_file.read())

        # Import all countries from the dataset
        all_countries = list(
            map(lambda x: tuple(x),
                df[['country', 'beer_servings', 'spirit_servings', 'wine_servings', 'total_litres_of_pure_alcohol', 'continent']].to_records(index=False))
        )

        args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s)", i).decode('utf-8') for i in all_countries)
        cur.execute("INSERT INTO Countries (country, beer_servings, spirit_servings, wine_servings, total_litres_of_pure_alcohol, continent) VALUES " + args_str)

        conn.commit()

    conn.close()
