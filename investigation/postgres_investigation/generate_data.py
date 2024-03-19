import uuid
import psycopg2
from random import randint
from time import time


def generate_reviews(amount):
    user_ids = [uuid.uuid4() for _ in range(1000)]
    film_ids = [uuid.uuid4() for _ in range(1000)]
    text = 'Lorem ipsum dolores sir amet'

    reviews = []

    for _ in range(amount):
        reviews.append((
            str(user_ids[randint(0, 999)]),
            str(film_ids[randint(0, 999)]),
            text,
        ))

    return reviews


def test_generate_data(db_conn, amount: int = 100000):
    reviews = generate_reviews(amount)
    records_list_template = ','.join(['%s'] * len(reviews))
    query = 'INSERT INTO reviews (user_id, film_id, text) values {}'.format(records_list_template)

    print(f"Inserting {amount} rows...")

    with db_conn.cursor() as cursor:
        cursor.execute('DELETE FROM reviews')

        start_time = time()
        cursor.execute(query, reviews)
        end_time = time()
        print(f"Data generated in {round(end_time - start_time, 2)} s")


def test_read_data(db_conn):
    query = f"SELECT user_id, film_id, text " \
            f"FROM reviews"

    print(f"Retrieving rows...")
    start_time = time()

    with db_conn.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
        print(f"{len(data)} rows retrieved")

    end_time = time()
    print(f"Data retrieved in {round(end_time - start_time, 2)} s")


if __name__ == "__main__":
    dsl = {
        'dbname': 'activities',
        'user': 'test',
        'password': 'test',
        'host': '0.0.0.0',
        'port': '5431'
    }

    with psycopg2.connect(**dsl) as conn:
        test_generate_data(conn, 1000000)
        test_read_data(conn)
