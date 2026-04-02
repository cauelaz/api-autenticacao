import hashlib
import base64
from datetime import datetime, timedelta


def encode_base64(text: str) -> str:
    return base64.b64encode(text.encode()).decode()


def gerar_senha_crip(senha: str, nome_usuario: str) -> str:
    # 1. MD5
    senha_md5 = hashlib.md5(senha.encode("utf-8")).hexdigest()

    # 2. Data +50 anos (~18600 dias)
    data_futura = datetime.now() + timedelta(days=18600)
    data_formatada = data_futura.strftime("%d%m%Y")

    # 3. Concatena tudo
    senha_final = senha_md5 + data_formatada

    # 4. Adiciona nome (TrimRight)
    senha_final += nome_usuario.rstrip()

    # 5. Base64
    senha_crip = encode_base64(senha_final)

    return senha_crip
