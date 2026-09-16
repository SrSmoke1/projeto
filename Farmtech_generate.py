#!/usr/bin/env python3
"""
FarmTech Solutions - Aplicação básica em Python para Agricultura Digital
Suporta 2 culturas: Café (retângulo) e Milho (círculo).
Guarda dados em vetores (listas), permite entrada, visualização, atualização,
deleção e exportação para CSV (para uso no R).
"""

import csv
import os

# Vetores (listas) para armazenar dados
ids = []                # id do registro
culturas = []           # 'Cafe' ou 'Milho'
geometrias = []         # 'retangulo' ou 'circulo'
params_area = []        # dicts com parametros de area (e.g. {'length':..., 'width':...} ou {'radius':...})
areas_m2 = []           # area calculada em m2
num_ruas = []           # numero de ruas
comp_rua_m = []         # comprimento de cada rua em metros (assumimos todas ruas com mesmo comprimento por registro)
insumos = []            # lista de dicts por registro: {'produto':..., 'taxa_mL_por_m':...}
litros_necessarios = [] # total de litros calculados

next_id = 1  # identificador incremental para registros

# Funções utilitárias
def calc_area(geo, params):
    if geo == 'retangulo':
        return params['length'] * params['width']
    elif geo == 'circulo':
        import math
        return math.pi * (params['radius'] ** 2)
    else:
        return 0

def calc_litros(taxa_mL_por_m, n_ruas, comp_rua_m):
    # taxa em mL por metro. total mL = taxa * n_ruas * comp_rua_m
    total_mL = taxa_mL_por_m * n_ruas * comp_rua_m
    total_L = total_mL / 1000.0
    return total_L

def input_float(prompt, min_val=None):
    while True:
        try:
            v = float(input(prompt).replace(',', '.'))
            if (min_val is not None) and (v < min_val):
                print(f"Valor deve ser >= {min_val}.")
                continue
            return v
        except ValueError:
            print("Entrada inválida. Digite um número (ex: 12.5).")

def input_int(prompt, min_val=None):
    while True:
        try:
            v = int(input(prompt))
            if (min_val is not None) and (v < min_val):
                print(f"Valor deve ser >= {min_val}.")
                continue
            return v
        except ValueError:
            print("Entrada inválida. Digite um inteiro.")

def mostrar_registro(index):
    print("-" * 40)
    print(f"Registro #{ids[index]} - Cultura: {culturas[index]}")
    print(f"Geometria: {geometrias[index]}")
    print(f"Parâmetros de área: {params_area[index]}")
    print(f"Área (m²): {areas_m2[index]:.2f}")
    print(f"Ruas: {num_ruas[index]}, comprimento rua (m): {comp_rua_m[index]:.2f}")
    print(f"Insumo: {insumos[index]['produto']}, taxa (mL/m): {insumos[index]['taxa_mL_por_m']}")
    print(f"Litros necessários: {litros_necessarios[index]:.3f} L")
    print("-" * 40)

def entrada_dados():
    global next_id
    print("\n--- Entrada de dados ---")
    print("Escolha a cultura:")
    print("1 - Café (área retangular)")
    print("2 - Milho (área circular)")
    escolha = input_int("Opção (1/2): ", 1)
    if escolha == 1:
        cultura = "Cafe"
        geo = "retangulo"
        length = input_float("Comprimento do retângulo (m): ", 0)
        width = input_float("Largura do retângulo (m): ", 0)
        params = {'length': length, 'width': width}
    else:
        cultura = "Milho"
        geo = "circulo"
        radius = input_float("Raio do círculo (m): ", 0)
        params = {'radius': radius}

    area = calc_area(geo, params)

    n_ruas = input_int("Número de ruas na lavoura (inteiro): ", 0)
    if n_ruas > 0:
        comp = input_float("Comprimento de cada rua (m) (assuma mesmo comprimento para todas ruas): ", 0)
    else:
        comp = 0.0

    print("\n--- Dados de manejo de insumos ---")
    produto = input("Nome do produto (ex: Fosfato, Herbicida X): ").strip()
    taxa = input_float("Taxa de aplicação (mL por metro linear) (ex: 500 para 500 mL/m): ", 0)

    litros = calc_litros(taxa, n_ruas, comp)

    # salvar nas listas (vetores)
    ids.append(next_id)
    culturas.append(cultura)
    geometrias.append(geo)
    params_area.append(params)
    areas_m2.append(area)
    num_ruas.append(n_ruas)
    comp_rua_m.append(comp)
    insumos.append({'produto': produto, 'taxa_mL_por_m': taxa})
    litros_necessarios.append(litros)

    print(f"\nRegistro salvo com ID {next_id}. Área = {area:.2f} m². Litros necessários = {litros:.3f} L.")
    next_id += 1

def visualizar_dados():
    print("\n--- Visualização de dados ---")
    if not ids:
        print("Nenhum registro cadastrado.")
        return
    for i in range(len(ids)):
        mostrar_registro(i)

def atualizar_dado():
    print("\n--- Atualizar dados ---")
    if not ids:
        print("Nenhum registro para atualizar.")
        return
    print("IDs disponíveis:", ids)
    target = input_int("Informe o ID do registro que deseja atualizar: ")
    if target not in ids:
        print("ID não encontrado.")
        return
    i = ids.index(target)
    print("Que campo deseja atualizar?")
    print("1 - Cultura / Geometria / Parâmetros de área")
    print("2 - Número de ruas / Comprimento rua")
    print("3 - Insumo (produto / taxa)")
    escolha = input_int("Opção: ", 1)
    if escolha == 1:
        if culturas[i] == "Cafe":
            print("Atualizando parâmetros do retângulo (Café).")
            length = input_float("Novo comprimento (m): ", 0)
            width = input_float("Nova largura (m): ", 0)
            params_area[i] = {'length': length, 'width': width}
            areas_m2[i] = calc_area('retangulo', params_area[i])
        else:
            print("Atualizando parâmetros do círculo (Milho).")
            radius = input_float("Novo raio (m): ", 0)
            params_area[i] = {'radius': radius}
            areas_m2[i] = calc_area('circulo', params_area[i])
    elif escolha == 2:
        n_ruas_new = input_int("Novo número de ruas: ", 0)
        comp_new = input_float("Novo comprimento de rua (m): ", 0)
        num_ruas[i] = n_ruas_new
        comp_rua_m[i] = comp_new
        litros_necessarios[i] = calc_litros(insumos[i]['taxa_mL_por_m'], num_ruas[i], comp_rua_m[i])
    else:
        produto = input("Novo nome do produto: ").strip()
        taxa = input_float("Nova taxa (mL por m): ", 0)
        insumos[i]['produto'] = produto
        insumos[i]['taxa_mL_por_m'] = taxa
        litros_necessarios[i] = calc_litros(taxa, num_ruas[i], comp_rua_m[i])

    print("Registro atualizado.")
    mostrar_registro(i)

def deletar_dado():
    print("\n--- Deleção de dado ---")
    if not ids:
        print("Nenhum registro para deletar.")
        return
    print("IDs disponíveis:", ids)
    target = input_int("Informe o ID do registro que deseja deletar: ")
    if target not in ids:
        print("ID não encontrado.")
        return
    i = ids.index(target)
    # remover de todas as listas
    ids.pop(i)
    culturas.pop(i)
    geometrias.pop(i)
    params_area.pop(i)
    areas_m2.pop(i)
    num_ruas.pop(i)
    comp_rua_m.pop(i)
    insumos.pop(i)
    litros_necessarios.pop(i)
    print(f"Registro {target} deletado.")

def exportar_csv(filename="farm_data.csv"):
    if not ids:
        print("Nenhum dado para exportar.")
        return
    header = [
        'id', 'cultura', 'geometria', 'params_area', 'area_m2',
        'num_ruas', 'comp_rua_m', 'produto', 'taxa_mL_por_m', 'litros_necessarios_L'
    ]
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(len(ids)):
            writer.writerow([
                ids[i],
                culturas[i],
                geometrias[i],
                str(params_area[i]),
                f"{areas_m2[i]:.6f}",
                num_ruas[i],
                f"{comp_rua_m[i]:.6f}",
                insumos[i]['produto'],
                f"{insumos[i]['taxa_mL_por_m']:.6f}",
                f"{litros_necessarios[i]:.6f}"
            ])
    print(f"Dados exportados para {filename}.")

def carregar_csv(filename="farm_data.csv"):
    global next_id
    if not os.path.exists(filename):
        print(f"Arquivo {filename} não encontrado.")
        return
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # limpar dados atuais antes de carregar
        ids.clear(); culturas.clear(); geometrias.clear(); params_area.clear()
        areas_m2.clear(); num_ruas.clear(); comp_rua_m.clear(); insumos.clear(); litros_necessarios.clear()
        max_id = 0
        for row in reader:
            ids.append(int(row['id']))
            if int(row['id']) > max_id:
                max_id = int(row['id'])
            culturas.append(row['cultura'])
            geometrias.append(row['geometria'])
            # params_area estava salvo como string; vamos avaliar de forma segura:
            import ast
            try:
                params = ast.literal_eval(row['params_area'])
            except Exception:
                params = {}
            params_area.append(params)
            areas_m2.append(float(row['area_m2']))
            num_ruas.append(int(row['num_ruas']))
            comp_rua_m.append(float(row['comp_rua_m']))
            insumos.append({'produto': row['produto'], 'taxa_mL_por_m': float(row['taxa_mL_por_m'])})
            litros_necessarios.append(float(row['litros_necessarios_L']))
        next_id = max_id + 1
    print(f"Dados carregados de {filename}. {len(ids)} registros importados.")

def menu_principal():
    while True:
        print("\n=== FarmTech Solutions - Menu ===")
        print("1 - Entrada de dados")
        print("2 - Visualizar dados")
        print("3 - Atualizar dado")
        print("4 - Deletar dado")
        print("5 - Exportar dados para CSV (farm_data.csv)")
        print("6 - Carregar dados de CSV (farm_data.csv)")
        print("0 - Sair do programa")
        op = input("Escolha uma opção: ").strip()
        if op == '1':
            entrada_dados()
        elif op == '2':
            visualizar_dados()
        elif op == '3':
            atualizar_dado()
        elif op == '4':
            deletar_dado()
        elif op == '5':
            exportar_csv()
        elif op == '6':
            carregar_csv()
        elif op == '0':
            print("Saindo... Até mais.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    print("Bem-vindo ao sistema FarmTech (Python).")
    # opção rápida para carregar dados existentes
    if os.path.exists("farm_data.csv"):
        resp = input("Arquivo farm_data.csv encontrado. Deseja carregar? (s/n): ").lower()
        if resp == 's':
            carregar_csv()
    menu_principal()