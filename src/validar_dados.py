
import sqlite3
from conexao import conectar


def validar_quantidade_registros(cursor):
    """Exibe a quantidade de registros de cada tabela."""

    tabelas = [
        "clientes",
        "produtos",
        "pedidos",
        "itens_pedido"
    ]

    print("\nQUANTIDADE DE REGISTROS POR TABELA")
    print("-" * 40)

    for tabela in tabelas:
        cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
        quantidade = cursor.fetchone()[0]

        print(f"{tabela}: {quantidade} registros")


def validar_chaves_estrangeiras(cursor):
    """Verifica violações de integridade referencial."""

    cursor.execute("PRAGMA foreign_key_check")
    erros = cursor.fetchall()

    print("\nVALIDAÇÃO DAS CHAVES ESTRANGEIRAS")
    print("-" * 40)

    if erros:
        print("Foram encontrados problemas:")

        for erro in erros:
            print(erro)

    else:
        print("Integridade referencial validada!")


def validar_tabelas(cursor):
    """Confirma se as quatro tabelas esperadas existem."""

    tabelas_esperadas = {
        "clientes",
        "produtos",
        "pedidos",
        "itens_pedido"
    }

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
    """)

    tabelas_existentes = {
        registro[0] for registro in cursor.fetchall()
    }

    faltantes = tabelas_esperadas - tabelas_existentes

    print("\nVALIDAÇÃO DA ESTRUTURA")
    print("-" * 40)

    if faltantes:
        print("Tabelas ausentes:", ", ".join(sorted(faltantes)))
        return False

    print("Todas as tabelas esperadas existem!")
    return True


def executar_validacao():
    """Executa todas as validações do banco de dados."""

    conexao = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        print("VALIDAÇÃO DO BANCO DE DADOS")

        tabelas_validas = validar_tabelas(cursor)

        if not tabelas_validas:
            print("\nVerifique a criação das tabelas antes de continuar.")
            return

        validar_quantidade_registros(cursor)
        validar_chaves_estrangeiras(cursor)

        print("\nValidação concluída!")

    except sqlite3.Error as erro:
        print(f"\nErro ao validar o banco de dados: {erro}")

    finally:
        if conexao is not None:
            conexao.close()


if __name__ == "__main__":
    executar_validacao()
