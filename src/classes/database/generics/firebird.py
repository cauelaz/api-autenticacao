import firebirdsql
from typing import Any, List, Tuple, Optional
import logging

# Configuração básica de logging, caso não esteja configurado globalmente
# Se já estiver configurado no seu arquivo principal, esta parte pode ser removida.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class FBConn:
    def __init__(
        self, database: str, host: str, port: int, user: str, password: str
    ):  # Removido o tipo de retorno '-> firebirdsql.connect' pois __init__ não retorna nada
        try:
            self.connection = firebirdsql.connect(
                database=database,  # Removidas as f-strings, não são necessárias aqui
                user=user,
                password=password,
                host=host,
                port=port,
            )
            logger.info(f"Conexão Firebird estabelecida para {host}:{port}/{database}")
        except Exception as e:
            logger.exception(f"Falha ao conectar ao banco de dados Firebird: {e}")
            raise ConnectionError(f"Não foi possível conectar ao Firebird: {e}") from e

    def query(
        self, query: str, params: Optional[Tuple[Any, ...]] = None
    ) -> List[Tuple[Any, ...]]:
        """
        Executa uma consulta SELECT no banco de dados Firebird.

        Args:
            query: A string da consulta SQL.
            params: Uma tupla de parâmetros para a consulta, usada para prevenir injeção SQL.
                    Se não for fornecido, a consulta é executada sem parâmetros.

        Returns:
            Uma lista de tuplas, onde cada tupla representa uma linha do resultado.
        """
        if params is None:
            params = ()  # Garante que params seja uma tupla vazia se nenhum for fornecido

        cur = None  # Inicializa cur como None para garantir que seja fechado no finally
        try:
            cur = self.connection.cursor()
            cur.execute(query, params)  # <--- AGORA PASSAMOS OS PARÂMETROS AQUI
            res = cur.fetchall()
            return res
        except Exception as e:
            logger.exception(
                f"Erro ao executar consulta SQL: {query} com parâmetros: {params}"
            )
            raise  # Re-levanta a exceção para que o chamador possa tratá-la
        finally:
            if cur:
                cur.close()  # Garante que o cursor seja fechado

    def upDate(
        self, query: str, params: Optional[Tuple[Any, ...]] = None
    ) -> List[Tuple[Any, ...]]:
        """
        Executa uma operação DML (INSERT, UPDATE, DELETE) no banco de dados Firebird.
        Considerar renomear este método para 'execute_dml' ou 'update_data' para maior clareza.

        Args:
            query: A string da consulta SQL.
            params: Uma tupla de parâmetros para a consulta.

        Returns:
            Uma lista de tuplas, representando os resultados (se houver).
            Para operações DML, fetchall() geralmente retorna uma lista vazia.
        """
        if params is None:
            params = ()

        cur = None  # Inicializa cur como None
        try:
            cur = self.connection.cursor()
            cur.execute(query, params)  # <--- AGORA PASSAMOS OS PARÂMETROS AQUI
            res = cur.fetchall()  # fetchall() pode retornar uma lista vazia para DML
            self.__commit_transaction()
            return res
        except Exception as e:
            self.connection.rollback()  # Desfaz as alterações em caso de erro
            logger.exception(
                f"Erro ao executar DML SQL: {query} com parâmetros: {params}"
            )
            raise  # Re-levanta a exceção
        finally:
            if cur:
                cur.close()  # Garante que o cursor seja fechado

    def __commit_transaction(self):
        """Commits a transação atual."""
        try:
            self.connection.commit()
            logger.debug("Transação commitada.")
        except Exception as e:
            logger.exception(f"Erro ao commitar transação: {e}")
            raise  # Re-levanta se o commit falhar

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.connection:
            try:
                self.connection.close()
                logger.info("Conexão Firebird fechada.")
            except Exception as e:
                logger.exception(f"Erro ao fechar conexão Firebird: {e}")
