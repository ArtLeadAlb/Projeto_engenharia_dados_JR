
import sqlite3
from pathlib import Path


# Localização fixa baseada no próprio arquivo conexao.py
# Estrutura: Projeto_engenharia_dados_JR/src/conexao.py
PASTA_SRC = Path(__file__).resolve().parent
PASTA_PROJETO = PASTA_SRC.parent
PASTA_DATA = PASTA_PROJETO / "data"
CAMINHO_BANCO = PASTA_DATA / "vendas.db"


def obter_caminho_banco():
    """Retorna o caminho absoluto do banco de dados."""

    return CAMINHO_BANCO


def conectar():
    """Cria a pasta data na raiz e abre a conexão SQLite."""

    PASTA_DATA.mkdir(parents=True, exist_ok=True)

    conexao = sqlite3.connect(str(CAMINHO_BANCO))
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao


def consultar(sql, parametros=()):
    """Executa consultas SQL e retorna colunas e registros."""

    conexao = conectar()

    try:
        cursor = conexao.cursor()
        cursor.execute(sql, parametros)

        if cursor.description is None:
            raise ValueError("A consulta não retornou resultados.")

        colunas = [coluna[0] for coluna in cursor.description]
        registros = cursor.fetchall()

        return colunas, registros

    finally:
        conexao.close()


def testar_conexao():
    """Testa a conexão e mostra o caminho utilizado."""

    conexao = None

    try:
        conexao = conectar()
        conexao.execute("SELECT sqlite_version()")

        print("Conexão realizada com sucesso!")
        print(f"Arquivo do banco: {CAMINHO_BANCO}")
        print(f"Pasta data: {PASTA_DATA}")

    except sqlite3.Error as erro:
        print(f"Erro de conexão: {erro}")

    finally:
        if conexao is not None:
            conexao.close()


if __name__ == "__main__":
    testar_conexao()
