import json
import os
from datetime import datetime


ARQUIVO = "dados_financeiros.json"

def carregar_dados():
    if os.path.exists(ARQUIVO):
       try:
           with open(ARQUIVO, "r", encoding="utf-8") as f:
               return json.load(f)
       except json.JSONDecodeError:
           return[]
    return[]

def salvar_dados(movimentacoes):
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(movimentacoes, f, ensure_ascii=False, indent=4)

def ler_texto_obrigatorio(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Esse campo não pode ficar vazio.")

def ler_data():
    while True:
        data = input("Digite a data (dd/mm/aaaa): ").strip()
        try:
            datetime.strptime(data, "%d/%m/%Y")
            return data
        except ValueError:
            print("Data inválida. Use o formato dd/mm/aaaa.")

def ler_data_edicao(data_atual):
    while True:
        nova_data = input(f"Nova data ({data_atual}): ").strip()
        if not nova_data:
            return data_atual
        try:
            datetime.strptime(nova_data, "%d/%m/%Y")
            return nova_data
        except ValueError:
            print("Data inálida. Use o formato dd/mm/aaaa.")

def ler_valor():
    while True:
        try:
            valor_texto = input("Digite o valor: R$ ").strip().replace(",", ".")
            valor = float(valor_texto)
            if valor > 0:
                return valor
            print("O valor deve ser maior que zero.")
        except ValueError:
            print("Digite um valor númerico válido.")

def ler_valor_edicao(valor_atual):
    while True:
        try:
            novo_valor = input(f"Novo valor ({valor_atual:.2f}): ").strip()
            if not novo_valor:
                return valor_atual
            novo_valor = float(novo_valor.replace(",", "."))
            if novo_valor > 0:
                return novo_valor
            print("O valor deve ser maior que zero.")
        except ValueError:
            print("Digite um valor númerico válido.")

def adicionar_movimentacao(movimentacoes, tipo):
    descricao = input("Digite a descrição: ").strip()
    categoria = input("Digite a categoria: ").strip()
    data = input("Digite a data (dd/mm/aaaa): ").strip()

    try:
        valor = float(input("Digite o valor: R$ ").replace(",", "."))
    except ValueError:
        print("Valor inválido. Tente novamente.")
        return

    if valor <= 0:
        print("O valor deve ser maior que zero.")
        return

    movimentacao = {
        "tipo": tipo.strip().lower(),
        "descricao": descricao,
        "categoria": categoria,
        "data": data,
        "valor": valor,
    }

    movimentacoes.append(movimentacao)
    salvar_dados(movimentacoes)
    print(f"{tipo.capitalize()} cadastrada com sucesso!")

def listar_movimentacoes(movimentacoes):
    if not movimentacoes:
        print("Nenhuma movimentação cadastrada.")
        return

    print("\n ===== MOVIMENTAÇÕES =====")
    for i, mov in enumerate(movimentacoes, start=1):
        print(f"[{i}] {mov['tipo'].upper()} | {mov['data']} | " f"{mov['descricao']} | {mov['categoria']} | R${mov['valor']:.2f}")

def exibir_lista(movimentacoes, titulo):
    if not movimentacoes:
        print("Nenhuma movimentacão cadastrada.")
        return
    print(f"\n ===== {titulo} =====")
    for i, mov in enumerate(movimentacoes, start=1):
        print(f"[{i}] {mov['tipo']} | {mov['data']} | {mov['descricao']} | {mov['categoria']} | R${mov['valor']:.2f}")

def filtrar_por_tipo(movimentacoes):
    if not movimentacoes:
        print("Nenhuma movimentação cadastrada.")
        return

    tipo = input("Digite o tipo para filtrar (entrada/saida): ").strip().lower()
    if tipo not in ["entrada", "saida"]:
        print("Tipo inválido. Digite 'entrada' ou 'saida'.")
        return

    encontrados = [mov for mov in movimentacoes if mov["tipo"] == tipo]
    exibir_lista(encontrados, f"FILTRO POR TIPO: {tipo.upper()}")

def filtrar_por_categoria(movimentacoes):
    if not movimentacoes:
        print("Nenhuma movimentação cadastrada.")
        return
    categoria = input("Digite a categoria para filtrar: ").strip().lower()
    encontrados = [mov for mov in movimentacoes if mov["categoria"].lower() == categoria]
    exibir_lista(encontrados, f"FILTRO POR CATEGORIA: {categoria.upper()}")

def buscar_por_descricao(movimentacoes):
    if not movimentacoes:
        print("Nenhuma movimentação cadastrada.")
        return

    termo = input("Digite um termo de descrição para buscar: ").strip().lower()

    encontrados = [mov for mov in movimentacoes if termo in mov["descrição"].lower()]
    exibir_lista(encontrados, f"BUSCAR POR DESCRIÇÃO: {termo.upper()}")

def filtrar_por_data(movimentacoes):
    if not movimentacoes:
        print("Nenhuma movimentação cadastrada.")
        return
    data = input("Digite a data para filtrar (dd/mm/aaaa): ").strip()

    encontrados = [mov for mov in movimentacoes if mov ["data"] == data]
    exibir_lista(encontrados, f"FILTRO POR DATA: {data}")

def filtrar_por_mes(movimentacoes):
        if not movimentacoes:
            print("Nenhuma movimentação cadastrada.")
            return
        mes_ano = input("Digite o mês e ano (mm/aaaa): ").strip()

        encontrados = [mov for mov in movimentacoes if mov ["data"][3:] == mes_ano]

def total_por_categoria(movimentacoes):
    if not movimentacoes:
        print("Nenhuma movimentação cadastrada.")
        return

    totais = {}

    for mov in movimentacoes:
        categoria = mov["categoria"]
        if categoria not in totais:
            totais[categoria] = 0
        totais[categoria] += mov["valor"]

    print("\n ====== TOTAL POR CATEGORIA ======")
    for categoria, total in totais.items():
        print(f"{categoria}: R${total:.2f}")

def calcular_saldo(movimentacoes):
    entradas = sum(mov["valor"] for mov in movimentacoes if mov["tipo"] == "entrada")
    saidas = sum(mov["valor"] for mov in movimentacoes if mov["tipo"] == "saida")
    saldo = entradas - saidas

    print("\n ===== RESUMO FINANCEIRO =====")
    print(f"Total de entradas: R$ {entradas:.2f}")
    print(f"Total de saídas: R$ {saidas:.2f}")
    print(f"Saldo atual: R$ {saldo:.2f}")

def editar_movimentacao(movimentacoes):
    if not movimentacoes:
        print("Nenhuma movimentação cadastrada.")
        return

    listar_movimentacoes(movimentacoes)

    try:
        indice = int(input("Digite o número da movimentação que deseja editar: ")) - 1
        if indice < 0 or indice >= len(movimentacoes):
            print("Movimentação inválida.")
            return
    except ValueError:
        print("Digite um número válido.")
        return

    mov = movimentacoes[indice]

    nova_descricao = input(f"Nova descrição ({mov['descricao']}): ").strip()
    nova_categoria = input(f"Nova categoria ({mov['categoria']}): ").strip()
    nova_data = ler_data_edicao(mov["data"])
    novo_valor = ler_valor_edicao(mov["valor"])

    if nova_descricao:
        mov["descricao"] = nova_descricao

    if nova_categoria:
        mov["categoria"] = nova_categoria

    mov["data"] = nova_data
    mov["valor"] = novo_valor

    salvar_dados(movimentacoes)
    print("Movimentação editada com sucesso!")

def excluir_movimentacao(movimentacoes):
    if not movimentacoes:
        print("Nenhuma movimentação cadastrada.")
        return

    listar_movimentacoes(movimentacoes)

    try:
        indice = int(input("Digite o número da movimentação que deseja excluir: ")) - 1
        if indice < 0 or indice >= len(movimentacoes):
            print("Movimentalção inválida.")
            return
    except ValueError:
        print("Digite um número válido.")
        return

    mov = movimentacoes[indice]
    confirmacao = input(f"Tem certeza que deseja excluir '{mov['descricao']}'? (s/n): ").strip().lower()

    if confirmacao == "s":
        movimentacoes.pop(indice)
        salvar_dados(movimentacoes)
        print("Movientação excluida com sucesso!")
    else:
        print("Exclusão cancelada.")

def relatorio_financeiro(movimentacoes):
    if not movimentacoes:
        print("Nenhuma movimentacao cadastrada.")
        return

    entradas = sum(mov["valor"] for mov in movimentacoes if mov["tipo"] == "entrada")
    saidas = sum(mov["valor"] for mov in movimentacoes if mov["tipo"] == "saida")
    saldo = entradas - saidas

    print("\n ===== RELATÓRIO FINANCEIRO =====")
    print(f"Quantidade de movimentações: {len(movimentacoes)}")
    print(f"Total de entradas: R$ {entradas:.2f}")
    print(f"Toral de saidas: R$ {saidas:.2f}")
    print(f"Saldo atual: R$ {saldo:.2f}")

    print("\n ----- Entradas cadastradas -----")
    encontrou_entrada = False
    for mov in movimentacoes:
        if mov["tipo"] == "entrada":
            print(f"{mov['data']} | {mov['descricao']} | {mov['categoria']} | R${mov['valor']:.2f}")
            encontrou_entrada = True
        if not encontrou_entrada:
            print("Nenhuma entrada cadastrada.")

            print("\n ----- Saídas cadastradas -----")
            encontrou_saida = False
            for mov in movimentacoes:
                if mov["tipo"] == "saida":
                    print(f"{mov['data']} | {mov['descricao']} | {mov['categoria']} | R${mov['valor']:.2f}")
                    encontou_saida = True
            if not encontrou_saida:
                print("Nenhuma saida cadastrada.")

def menu():
    movimentacoes = carregar_dados()

    while True:
        print("\n ===== CONTROLE FINANCEIRO =====")
        print("1 - Adicionar entrada")
        print("2 - Adicionar saída")
        print("3 - Listar movimentações")
        print("4 - Ver saldo")
        print("5 - Editar movimentação")
        print("6 - Excluir movimentação")
        print("7 - Relatório financeiro")
        print("8 - Filtrar por tipo")
        print("9 - Filtrar por categoria")
        print("10 - Buscar por descrição")
        print("11 - Filtrar pot data")
        print("12 - Filtrar por mês")
        print("13 -Total por categoria")
        print("14 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            adicionar_movimentacao(movimentacoes, "entrada")

        elif opcao == "2":
            adicionar_movimentacao(movimentacoes, "saida")

        elif opcao == "3":
            listar_movimentacoes(movimentacoes)

        elif opcao == "4":
            calcular_saldo(movimentacoes)

        elif opcao == "5":
            editar_movimentacao(movimentacoes)

        elif opcao == "6":
            excluir_movimentacao(movimentacoes)

        elif opcao == "7":
            relatorio_financeiro(movimentacoes)

        elif opcao == "8":
            filtrar_por_tipo(movimentacoes)

        elif opcao == "9":
            filtrar_por_tipo(movimentacoes)

        elif opcao == "10":
            buscar_por_descricao(movimentacoes)

        elif opcao == "11":
            filtrar_por_data(movimentacoes)

        elif opcao == "12":
            filtrar_por_mes(movimentacoes)

        elif opcao == "13":
            total_por_categoria(movimentacoes)
            
        elif opcao == "14":
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")


menu()
