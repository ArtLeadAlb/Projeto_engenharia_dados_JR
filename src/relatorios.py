from conexao import consultar


def listar_clientes():
    sql = """
        SELECT id_cliente, nome, email, cidade
        FROM clientes
        ORDER BY nome;
    """
    return consultar(sql)


def listar_produtos():
    sql = """
        SELECT id_produto, nome AS produto, categoria, preco, estoque
        FROM produtos
        ORDER BY preco DESC;
    """
    return consultar(sql)


def pedidos_por_cliente():
    sql = """
        SELECT
            p.id_pedido,
            c.nome AS cliente,
            p.data_pedido,
            p.status
        FROM pedidos AS p
        INNER JOIN clientes AS c
            ON p.id_cliente = c.id_cliente
        ORDER BY p.data_pedido;
    """
    return consultar(sql)


def detalhar_pedidos():
    sql = """
        SELECT
            p.id_pedido,
            c.nome AS cliente,
            pr.nome AS produto,
            ip.quantidade,
            ip.preco_unitario,
            ROUND(ip.quantidade * ip.preco_unitario, 2) AS valor_item
        FROM pedidos AS p
        INNER JOIN clientes AS c
            ON p.id_cliente = c.id_cliente
        INNER JOIN itens_pedido AS ip
            ON p.id_pedido = ip.id_pedido
        INNER JOIN produtos AS pr
            ON ip.id_produto = pr.id_produto
        ORDER BY p.id_pedido, pr.nome;
    """
    return consultar(sql)


def total_por_pedido():
    sql = """
        SELECT
            p.id_pedido,
            c.nome AS cliente,
            ROUND(SUM(ip.quantidade * ip.preco_unitario), 2)
                AS valor_total
        FROM pedidos AS p
        INNER JOIN clientes AS c
            ON p.id_cliente = c.id_cliente
        INNER JOIN itens_pedido AS ip
            ON p.id_pedido = ip.id_pedido
        GROUP BY p.id_pedido, c.nome
        ORDER BY valor_total DESC;
    """
    return consultar(sql)


def faturamento_por_cliente():
    sql = """
        SELECT
            c.id_cliente,
            c.nome AS cliente,
            COUNT(DISTINCT p.id_pedido) AS total_pedidos,
            ROUND(
                COALESCE(SUM(ip.quantidade * ip.preco_unitario), 0),
                2
            ) AS valor_total
        FROM clientes AS c
        LEFT JOIN pedidos AS p
            ON c.id_cliente = p.id_cliente
        LEFT JOIN itens_pedido AS ip
            ON p.id_pedido = ip.id_pedido
        GROUP BY c.id_cliente, c.nome
        ORDER BY valor_total DESC;
    """
    return consultar(sql)


def produtos_mais_vendidos():
    sql = """
        SELECT
            pr.id_produto,
            pr.nome AS produto,
            SUM(ip.quantidade) AS unidades_vendidas,
            ROUND(
                SUM(ip.quantidade * ip.preco_unitario), 2
            ) AS valor_vendido
        FROM produtos AS pr
        INNER JOIN itens_pedido AS ip
            ON pr.id_produto = ip.id_produto
        GROUP BY pr.id_produto, pr.nome
        ORDER BY unidades_vendidas DESC, valor_vendido DESC;
    """
    return consultar(sql)


def pedidos_por_status():
    sql = """
        SELECT status, COUNT(*) AS quantidade_pedidos
        FROM pedidos
        GROUP BY status
        ORDER BY quantidade_pedidos DESC;
    """
    return consultar(sql)


def faturamento_por_cidade():
    sql = """
        SELECT
            c.cidade,
            COUNT(DISTINCT p.id_pedido) AS total_pedidos,
            ROUND(
                SUM(ip.quantidade * ip.preco_unitario), 2
            ) AS faturamento
        FROM clientes AS c
        INNER JOIN pedidos AS p
            ON c.id_cliente = p.id_cliente
        INNER JOIN itens_pedido AS ip
            ON p.id_pedido = ip.id_pedido
        GROUP BY c.cidade
        ORDER BY faturamento DESC;
    """
    return consultar(sql)


def pedidos_pendentes():
    sql = """
        SELECT
            p.id_pedido,
            c.nome AS cliente,
            p.data_pedido,
            p.status
        FROM pedidos AS p
        INNER JOIN clientes AS c
            ON p.id_cliente = c.id_cliente
        WHERE p.status = ?
        ORDER BY p.data_pedido;
    """
    return consultar(sql, ("Pendente",))


def vendas_por_periodo():
    sql = """
        SELECT
            DATE(p.data_pedido) AS data,
            COUNT(DISTINCT p.id_pedido) AS total_pedidos,
            ROUND(
                SUM(ip.quantidade * ip.preco_unitario), 2
            ) AS valor_vendido
        FROM pedidos AS p
        INNER JOIN itens_pedido AS ip
            ON p.id_pedido = ip.id_pedido
        WHERE DATE(p.data_pedido) BETWEEN ? AND ?
        GROUP BY DATE(p.data_pedido)
        ORDER BY data;
    """
    return consultar(sql, ("2026-10-01", "2026-10-15"))


def resumo_geral():
    sql = """
        SELECT
            COUNT(DISTINCT p.id_pedido) AS total_pedidos,
            COUNT(DISTINCT p.id_cliente) AS clientes_com_pedidos,
            COALESCE(SUM(ip.quantidade), 0) AS unidades_vendidas,
            ROUND(
                COALESCE(
                    SUM(ip.quantidade * ip.preco_unitario), 0
                ), 2
            ) AS valor_total
        FROM pedidos AS p
        LEFT JOIN itens_pedido AS ip
            ON p.id_pedido = ip.id_pedido;
    """
    return consultar(sql)
