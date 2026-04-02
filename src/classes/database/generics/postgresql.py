import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


class PGConn:
    def __init__(
        self, database: str, host: str, port: int, user: str, password: str
    ) -> psycopg2.connect:
        self.connection = psycopg2.connect(
            database=f"{database}",
            user=f"{user}",
            password=f"{password}",
            host=f"{host}",
            port=port,
        )

    def query_with_field_name(self, query: str):
        try:
            cur = self.connection.cursor()
            cur.execute(query)
            res = []

            try:
                for row in cur.fetchall():
                    temp_array = {}
                    for item in range(0, len(row)):
                        temp_array[cur.description[item].name] = row[item]

                    self.__commit_transaction()
                    res.append(temp_array)

                return res
            except Exception as e:
                return True
        except Exception as e:
            print(e)
            return False

    def query(self, query: str):
        try:
            cur = self.connection.cursor()
            cur.execute(query)
            res = []

            try:
                for row in cur.fetchall():
                    res.append(row)
                self.__commit_transaction()
                return res
            except Exception as e:
                return True
        except Exception as e:

            print(e)
            return False

    def close_connection(self):
        self.connection.close()

    def __commit_transaction(self):
        self.connection.commit()
