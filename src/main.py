import hashlib
from fastapi import FastAPI, Query
import base64
from classes.database.panel_connection import PanelConnection
from classes.database.client_connection import ClientConnection
import os
from dotenv import load_dotenv
from utils import gerar_senha_crip

load_dotenv()
app = FastAPI()


def encode_base64(text: str) -> str:
    return base64.b64encode(text.encode()).decode()


@app.get("/autenticacao")
def check_password(
    cnpj: str = Query(...),
    user: str = Query(...),
    password: str = Query(..., alias="pass"),
):
    # Aqui você validaria no banco (mock por enquanto)

    connection_pg = PanelConnection()
    connection_data = connection_pg.client_connection_data(cnpj)
    senha_crip = gerar_senha_crip(password, user)
    client_conn = ClientConnection(
        database=connection_data[0],
        host=connection_data[1],
        port=connection_data[2],
        user=connection_data[3],
        password=connection_data[4],
    )
    sql = f"""select us.usuario,us.senha
            from usuarios_servidor us
            left join usuarios u on u.usuario_servidor = us.codigo
            where u.nome = 'teste_caue' and u.senha_crip = 'MjAyY2I5NjJhYzU5MDc1Yjk2NGIwNzE1MmQyMzRiNzAwNTAzMjA3N3Rlc3RlX2NhdWU='
            """
    result = client_conn.query(sql)
    print(result)
    return {
        "success": True,
        "user": result[0][0] if result else "",
        "password": result[0][1] if result else "",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}
