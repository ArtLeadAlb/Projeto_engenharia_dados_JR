
import sqlite3
from conexao import conectar


def criar_tabela_clientes(cursor):
    """Cria a tabela de clientes."""

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            cidade TEXT NOT NULL
        );
    """)


def criar_tabela_produtos(cursor):
    """Cria a tabela de produtos."""

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL CHECK (preco >= 0),
            estoque INTEGER NOT NULL CHECK (estoque >= 0)
        );
    """)


def criar_tabela_pedidos(cursor):
    """Cria a tabela de pedidos."""

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            data_pedido TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (id_cliente)
                REFERENCES clientes(id_cliente),
            UNIQUE (id_cliente, data_pedido)
        );
    """)


def criar_tabela_itens_pedido(cursor):
    """Cria a tabela de itens dos pedidos."""

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id_item INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pedido INTEGER NOT NULL,
            id_produto INTEGER NOT NULL,
            quantidade INTEGER NOT NULL CHECK (quantidade > 0),
            preco_unitario REAL NOT NULL CHECK (preco_unitario >= 0),
            FOREIGN KEY (id_pedido)
                REFERENCES pedidos(id_pedido),
            FOREIGN KEY (id_produto)
                REFERENCES produtos(id_produto),
            UNIQUE (id_pedido, id_produto)
        );
    """)


def gerar_banco_dados():
    """Cria as quatro tabelas dentro do banco configurado."""

    conexao = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        criar_tabela_clientes(cursor)
        criar_tabela_produtos(cursor)
        criar_tabela_pedidos(cursor)
        criar_tabela_itens_pedido(cursor)

        conexao.commit()

        print("\nBanco de dados e tabelas criados com sucesso!")

    except sqlite3.Error as erro:
        if conexao is not None:
            conexao.rollback()

        print(f"\nErro ao criar as tabelas: {erro}")

    finally:
        if conexao is not None:
            conexao.close()


if __name__ == "__main__":
    gerar_banco_dados()
