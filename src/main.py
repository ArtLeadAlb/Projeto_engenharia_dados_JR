import sqlite3
import relatorios

from criar_tabelas import gerar_banco_dados
from inserir_dados import popular_banco



def exibir_menu():
    """Mostra as opções disponíveis para o usuário."""

    print("\n" + "=" * 55)
    print("   PROJETO DE ENGENHARIA DE DADOS - JR")
    print("=" * 55)
    print("Escolha uma opção:\n")

    print("1  - Gerar banco de dados")
    print("2  - Popular banco de dados")
    print("-" * 55)
    print("3  - Listar clientes")
    print("4  - Listar produtos")
    print("5  - Pedidos por cliente")
    print("6  - Detalhamento dos pedidos")
    print("7  - Valor total por pedido")
    print("8  - Faturamento por cliente")
    print("9  - Produtos mais vendidos")
    print("10 - Pedidos por status")
    print("11 - Faturamento por cidade")
    print("12 - Pedidos pendentes")
    print("13 - Vendas por período")
    print("14 - Resumo geral das vendas")
    print("0  - Sair")

    print("=" * 55)


def exibir_resultados(colunas, registros):
    """Exibe os resultados em formato tabular."""

    if not registros:
        print("\nNenhum registro encontrado.")
        return

    larguras = []

    for indice, coluna in enumerate(colunas):
        maior_valor = max(
            len(str(registro[indice]))
            if registro[indice] is not None else 4
            for registro in registros
        )

        larguras.append(max(len(coluna), maior_valor))

    cabecalho = " | ".join(
        coluna.ljust(larguras[indice])
        for indice, coluna in enumerate(colunas)
    )

    print("\n" + cabecalho)
    print("-" * len(cabecalho))

    for registro in registros:
        linha = " | ".join(
            (
                str(valor)
                if valor is not None
                else "NULL"
            ).ljust(larguras[indice])
            for indice, valor in enumerate(registro)
        )

        print(linha)

    print(f"\nTotal de registros: {len(registros)}")


def executar_relatorio(titulo, funcao_relatorio):
    """Executa o relatório selecionado e trata erros."""

    print(f"\n### {titulo} ###")

    try:
        colunas, registros = funcao_relatorio()
        exibir_resultados(colunas, registros)

    except sqlite3.Error as erro:
        print(f"\nErro no banco de dados: {erro}")

    except (ValueError, TypeError) as erro:
        print(f"\nErro ao processar o relatório: {erro}")


def obter_opcao():
    """Solicita e retorna a opção escolhida pelo usuário."""

    return input("\nDigite a opção desejada: ").strip()



def main():
    """Controla o fluxo principal do sistema."""

    relatorios_menu = {
        "3": ("LISTA DE CLIENTES", relatorios.listar_clientes),
        "4": ("LISTA DE PRODUTOS", relatorios.listar_produtos),
        "5": ("PEDIDOS POR CLIENTE", relatorios.pedidos_por_cliente),
        "6": ("DETALHAMENTO DOS PEDIDOS", relatorios.detalhar_pedidos),
        "7": ("VALOR TOTAL POR PEDIDO", relatorios.total_por_pedido),
        "8": ("FATURAMENTO POR CLIENTE", relatorios.faturamento_por_cliente),
        "9": ("PRODUTOS MAIS VENDIDOS", relatorios.produtos_mais_vendidos),
        "10": ("PEDIDOS POR STATUS", relatorios.pedidos_por_status),
        "11": ("FATURAMENTO POR CIDADE", relatorios.faturamento_por_cidade),
        "12": ("PEDIDOS PENDENTES", relatorios.pedidos_pendentes),
        "13": ("VENDAS POR PERÍODO", relatorios.vendas_por_periodo),
        "14": ("RESUMO GERAL DAS VENDAS", relatorios.resumo_geral),
    }

    while True:
        try:
            exibir_menu()
            opcao = obter_opcao()

            if opcao == "0":
                print("\nEncerrando o sistema. Até logo!")
                break

            elif opcao == "1":
                gerar_banco_dados()
                input("\nPressione ENTER para voltar ao menu...")

            elif opcao == "2":
                gerar_banco_dados()
                popular_banco()
                input("\nPressione ENTER para voltar ao menu...")

            elif opcao in relatorios_menu:
                titulo, funcao_relatorio = relatorios_menu[opcao]
                executar_relatorio(titulo, funcao_relatorio)
                input("\nPressione ENTER para voltar ao menu...")

            else:
                print("\nOpção inválida. Escolha uma opção de 0 a 14.")

        except (KeyboardInterrupt, EOFError):
            print("\n\nSistema encerrado.")
            break


if __name__ == "__main__":
    main()
