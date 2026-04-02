from classes.database.generics.firebird import FBConn
from typing import Any, List, Tuple, Optional  # Importações adicionadas para tipagem


class ClientConnection(FBConn):
    def __init__(self, database: str, host: str, port: int, user: str, password: str):
        super().__init__(database, host, port, user, password)

    def get_companies_ciot(self, codigo_empresa: int) -> Optional[dict]:
        try:

            query_sql = f"SELECT chave, valor FROM empresas_configs WHERE entrada LIKE '%_CIOT_FF' AND empresa = {codigo_empresa} ORDER BY entrada;"
            result_rows = self.query(
                query_sql
            )  # Assumindo que self.query retorna uma lista de tuplas/listas

            if not result_rows or len(result_rows) < 2:
                # Logar um aviso ou levantar uma exceção mais específica aqui
                return None  # Retorna None em vez de False para ser mais consistente com a tipagem

            result = {
                "login": result_rows[0][1],
                "password": result_rows[1][1],
            }
            return result
        except Exception as e:
            # Logar a exceção completa para depuração
            # logger.exception("Erro ao obter dados de CIOT da empresa.")
            return None  # Retorna None em vez de False

    def get_companies_vpo(self, codigo_empresa: int) -> Optional[dict]:
        try:

            query_sql = f"SELECT entrada, valor FROM empresas_configs WHERE entrada LIKE '%_VPO_FF' AND empresa = {codigo_empresa} ORDER BY entrada;"
            result_rows = self.query(
                query_sql
            )  # Assumindo que self.query retorna uma lista de tuplas/listas
            if not result_rows or len(result_rows) < 2:
                # Logar um aviso ou levantar uma exceção mais específica aqui
                return None  # Retorna None em vez de False para ser mais consistente com a tipagem

            result = {
                "login": result_rows[0][1],
                "password": result_rows[1][1],
            }
            return result
        except Exception as e:
            # Logar a exceção completa para depuração
            # logger.exception("Erro ao obter dados de VPO da empresa.")
            return None  # Retorna None em vez de False

    # ESTE É O MÉTODO QUE PRECISA SER ALTERADO PARA ACEITAR PARÂMETROS
    def searches(
        self, sql: str, params: Optional[Tuple[Any, ...]] = None
    ) -> List[Tuple[Any, ...]]:
        """
        Executa uma consulta SELECT no banco de dados, aceitando parâmetros.

        Args:
            sql: A string da consulta SQL.
            params: Uma tupla de parâmetros para a consulta, usada para prevenir injeção SQL.
                    Se não for fornecido, a consulta é executada sem parâmetros.

        Returns:
            Uma lista de tuplas, onde cada tupla representa uma linha do resultado.
        """
        # Assumindo que self.query (da classe FBConn) é o método que realmente executa a SQL
        # e que ele pode aceitar um segundo argumento para os parâmetros.
        return self.query(sql, params)  # AGORA PASSAMOS OS PARÂMETROS PARA self.query

    # Este método também deve ser atualizado para aceitar parâmetros se for usado para DML com valores dinâmicos
    def update(self, sql: str, params: Optional[Tuple[Any, ...]] = None) -> List[Any]:
        """
        Executa uma operação de atualização (DML) no banco de dados, aceitando parâmetros.

        Args:
            sql: A string da consulta SQL.
            params: Uma tupla de parâmetros para a consulta.

        Returns:
            Uma lista de resultados (se houver).
        """
        # Assumindo que self.upDate (da classe FBConn) é o método que realmente executa a SQL
        # e que ele pode aceitar um segundo argumento para os parâmetros.
        query_result = self.upDate(
            sql, params
        )  # Passamos os parâmetros para self.upDate
        result = []
        for row in query_result:
            result.append(row[0])
        return result
