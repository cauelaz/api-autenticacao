import os
from dotenv import load_dotenv
from classes.database.generics.postgresql import PGConn

load_dotenv(dotenv_path="./.env")


class NoDataFoundError(Exception):
    pass


class PanelConnection(PGConn):
    def __init__(self):
        super().__init__(
            os.getenv("PANEL_DATABASE"),
            os.getenv("PANEL_HOST"),
            os.getenv("PANEL_PORT"),
            os.getenv("PANEL_USER"),
            os.getenv("PANEL_PASSWORD"),
        )

    def client_connection_data(self, cnpj: str) -> dict:
        try:
            print(f"Obtendo dados de conexão para CNPJ: {cnpj}")

            query = f"""
                SELECT
                    t.codigo,
                    t.banco as database,
                    t.servidor as host,
                    t.porta as port,
                    t.user_server as user,
                    t.cnpj as cnpj,
                    t.senha_server as password
                FROM transportador t
                WHERE t.cnpj = '{cnpj}'
            """
            query_result = self.query_with_field_name(query)

            if not query_result:
                return 1

            for row in query_result:
                result = {
                    0: row["database"] or os.getenv("FDB_DATABASE"),
                    1: row["host"] or os.getenv("FDB_HOST"),
                    2: row["port"] or os.getenv("FDB_PORT"),
                    3: row["user"] or os.getenv("FDB_USER"),
                    4: row["password"] or os.getenv("FDB_PASSWORD"),
                }

                if any(value is None or value == "" for value in result.values()):
                    return 2

                return result

        except Exception as e:
            print(f"Erro ao obter dados de conexão: {e}")
            return False

    def client_connection_data_order_id(self) -> dict:
        try:
            print(f"Obtendo dados de conexão para company_id: {id}")

            query = f"""
                        SELECT
                        t.cnpj as cnpj
                    FROM transportador t
                    JOIN integracoes_transportadoras it on t.codigo = it.transportador
                    WHERE it.integracao = 12
                """

            query_result = self.query_with_field_name(query)
            print(query_result)
            return query_result

        except Exception as e:
            print(f"Erro ao obter dados de conexão: {e}")
            return False
