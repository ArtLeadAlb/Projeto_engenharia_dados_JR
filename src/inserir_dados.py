
import sqlite3
from conexao import conectar


def inserir_clientes(cursor):
    """Insere os clientes."""

    clientes = [
        ("Ana Souza", "ana.souza@email.com", "Rio de Janeiro"),
        ("Bruno Lima", "bruno.lima@email.com", "São Paulo"),
        ("Carla Mendes", "carla.mendes@email.com", "Belo Horizonte"),
        ("Daniel Oliveira", "daniel.oliveira@email.com", "Curitiba"),
        ("Eduarda Costa", "eduarda.costa@email.com", "Salvador"),
        ("Felipe Santos", "felipe.santos@email.com", "Brasília"),
        ("Gabriela Rocha", "gabriela.rocha@email.com", "Recife"),
        ("Henrique Alves", "henrique.alves@email.com", "Porto Alegre"),
        ("Isabela Martins", "isabela.martins@email.com", "Campinas"),
        ("João Pereira", "joao.pereira@email.com", "Niterói")
    ]

    cursor.executemany("""
        INSERT INTO clientes (nome, email, cidade)
        VALUES (?, ?, ?)
        ON CONFLICT(email) DO NOTHING;
    """, clientes)

    print("Clientes processados!")


def inserir_produtos(cursor):
    """Insere os produtos."""

    produtos = [
        ("Notebook", "Informática", 3500.00, 20),
        ("Mouse", "Acessórios", 80.00, 100),
        ("Teclado", "Acessórios", 150.00, 60),
        ("Monitor", "Informática", 1200.00, 30),
        ("Headset", "Áudio", 250.00, 45),
        ("Webcam", "Acessórios", 180.00, 35),
        ("Cadeira Gamer", "Móveis", 950.00, 15),
        ("SSD 1TB", "Armazenamento", 450.00, 40),
        ("Impressora", "Periféricos", 700.00, 12),
        ("Tablet", "Informática", 1800.00, 25)
    ]

    cursor.executemany("""
        INSERT INTO produtos (nome, categoria, preco, estoque)
        VALUES (?, ?, ?, ?)
        ON CONFLICT DO NOTHING;
    """, produtos)

    print("Produtos processados!")


def inserir_pedidos(cursor):
    """Insere os pedidos associados aos clientes."""

    pedidos = [
        (1, "2026-10-01 09:15:00", "Concluído"),
        (2, "2026-10-02 10:30:00", "Concluído"),
        (3, "2026-10-03 14:20:00", "Enviado"),
        (4, "2026-10-04 16:45:00", "Pendente"),
        (5, "2026-10-05 11:10:00", "Concluído"),
        (1, "2026-10-06 13:00:00", "Enviado"),
        (6, "2026-10-07 15:30:00", "Concluído"),
        (7, "2026-10-08 09:50:00", "Pendente"),
        (8, "2026-10-09 17:25:00", "Concluído"),
        (9, "2026-10-10 12:40:00", "Enviado"),
        (10, "2026-10-11 08:35:00", "Concluído"),
        (2, "2026-10-12 18:10:00", "Pendente"),
        (3, "2026-10-13 10:00:00", "Concluído"),
        (5, "2026-10-14 14:15:00", "Enviado"),
        (7, "2026-10-15 16:20:00", "Concluído")
    ]

    cursor.executemany("""
        INSERT INTO pedidos (id_cliente, data_pedido, status)
        SELECT ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1
            FROM pedidos
            WHERE id_cliente = ?
              AND data_pedido = ?
        );
    """, [
        (cliente, data, status, cliente, data)
        for cliente, data, status in pedidos
    ])

    print("Pedidos processados!")


def inserir_itens_pedido(cursor):
    """Insere os produtos pertencentes a cada pedido."""

    itens_pedido = [
        (1, 1, 1, 3500.00),
        (1, 2, 2, 80.00),
        (1, 3, 1, 150.00),
        (2, 4, 1, 1200.00),
        (2, 5, 1, 250.00),
        (3, 6, 2, 180.00),
        (3, 2, 1, 80.00),
        (4, 7, 1, 950.00),
        (4, 3, 1, 150.00),
        (5, 10, 1, 1800.00),
        (5, 8, 2, 450.00),
        (6, 9, 1, 700.00),
        (6, 2, 1, 80.00),
        (7, 1, 1, 3500.00),
        (7, 8, 1, 450.00),
        (8, 5, 2, 250.00),
        (8, 6, 1, 180.00),
        (9, 4, 2, 1200.00),
        (9, 3, 2, 150.00),
        (10, 10, 1, 1800.00),
        (10, 2, 3, 80.00),
        (11, 7, 1, 950.00),
        (11, 5, 1, 250.00),
        (12, 1, 1, 3500.00),
        (12, 3, 1, 150.00),
        (13, 8, 2, 450.00),
        (13, 2, 2, 80.00),
        (14, 9, 1, 700.00),
        (14, 6, 2, 180.00),
        (15, 4, 1, 1200.00),
        (15, 5, 1, 250.00)
    ]

    cursor.executemany("""
        INSERT INTO itens_pedido (
            id_pedido,
            id_produto,
            quantidade,
            preco_unitario
        )
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1
            FROM itens_pedido
            WHERE id_pedido = ?
              AND id_produto = ?
        );
    """, [
        (
            pedido, produto, quantidade, preco,
            pedido, produto
        )
        for pedido, produto, quantidade, preco in itens_pedido
    ])

    print("Itens dos pedidos processados!")



def popular_banco():
    """Executa a carga completa em uma única transação."""

    conexao = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        inserir_clientes(cursor)
        inserir_produtos(cursor)
        inserir_pedidos(cursor)
        inserir_itens_pedido(cursor)

        conexao.commit()
        print("\nCarga de dados concluída com sucesso!")
        return True

    except sqlite3.Error as erro:
        if conexao is not None:
            conexao.rollback()

        print(f"\nErro ao inserir dados: {erro}")
        return False

    finally:
        if conexao is not None:
            conexao.close()


if __name__ == "__main__":
    popular_banco()


if __name__ == "__main__":
    popular_banco()
