# run a query that counts the rows in teachers, and print the result. It should print 0, which proves the whole chain works.

import psycopg

# connect to an existing database
with psycopg.connect("dbname=sped_hub") as conn:  # noqa: SIM117

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

       cur.execute("SELECT COUNT(*) FROM teachers")
       result = cur.fetchone()
       print(f'Total rows: {result[0]}')