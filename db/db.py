from peewee import PostgresqlDatabase

db = PostgresqlDatabase(
    "test-db", user="postgres", password="postgres", host="localhost", port=1234
)
