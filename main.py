import math
import random
import time

# Função para calcular a distância euclidiana entre dois pontos
def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2) # Calcula a distância entre dois pontos no plano cartesiano usando a fórmula de Pitágoras


# Leitura dos dados da instância a partir de um arquivo O(n)
def read_instance(file_path):
    nodes = [] # Lista para armazenar os vértices(cidades) e suas coordenadas
    with open(file_path, "r") as file:
        # Ignorar as 5 primeiras linhas
        for _ in range(5):
            next(file)
        
        # Processar as linhas restantes até encontrar "EOF"(indicando o fim do arquivo de instância)
        for line in file:
            line = line.strip() # Remove espaços em branco extras
            if line == "EOF":
                break
            parts = line.split() # Delimita os valores da linha pelos espaços
            node_id = int(parts[0]) # Identificador da cidade
            x = float(parts[1]) 
            y = float(parts[2])
            nodes.append((node_id, x, y)) # Adiciona a cidade id e corrdenadas x e y a lista de vértices
    return nodes # Retorna a lista de cidades


# Criar matriz de distâncias O(n^2)
def create_distance_matrix(nodes):
    dimension = len(nodes) # Número de cidades
    distance_matrix = [[0] * dimension for _ in range(dimension)] # Cria uma matriz bidimensional inicializada com zeros

    # Preenche a matriz com as distâncias entre todas as cidades.
    for i in range(dimension):
        for j in range(dimension):
            if i != j:  # Evita calcular a distância de uma cidade para ela mesma
                _, x1, y1 = nodes[i] # Coordenadas da cidade i
                _, x2, y2 = nodes[j]  # Coordenadas da cidade j
                distance_matrix[i][j] = euclidean_distance(x1, y1, x2, y2) # Calcula a distância entre duas cidades e preenche a matriz
    return distance_matrix # Retorna a matriz de distâncias


# Heurística do vizinho mais próximo com fator alpha O(n^2)
def nearest_neighbor(distance_matrix):
    n = len(distance_matrix) # Número de cidades
    unvisited = set(range(1, n)) # Conjunto de cidades ainda não visitadas (exclui a cidade inicial, 0)
    tour = [0] # O tour começa na cidade inicial (0)
    current = 0 # Cidade atual é a cidade inicial
    alpha = random.uniform(0, 0.5) # Fator alpha aleatório para ajustar os custos
    while unvisited: # Enquanto houver cidades não visitadas
        next_node = min(unvisited, key=lambda j: (1 - alpha) * distance_matrix[current][j] + alpha * distance_matrix[j][0])  # Escolhe a próxima cidade minimizando o custo ajustado pela fórmula com alpha
        unvisited.remove(next_node) # Remove a cidade escolhida do conjunto de cidades não visitadas
        tour.append(next_node) # Adiciona a cidade escolhida ao tour
        current = next_node # Atualiza a cidade atual
    tour.append(0) # Retornar ao ponto inicial
    return tour # Retorna o tour completo


# Caminho do arquivo de instância
print("Digite o nome da instancia a ser executada: ")
instance = input()
instance_file = "instances/" + instance

# Nome do arquivo de destino
print("Digite o nome do arquivo a ser salvo o melhor tour encontrado: ")
file_final = "results/" + input()

# Ler os dados e calcular a matriz de distâncias
nodes = read_instance(instance_file)
distance_matrix = create_distance_matrix(nodes)

# Variáveis para armazenar resultados
iterations = 5 # Número de vezes que a heurística será executada
solutions = [] # Lista para armazenar os custos das soluções encontradas
tours = [] # Lista para armazenar os tours encontrados
execution_times = [] # Lista para armazenar os tempos de execução de cada iteração

for iteration in range(iterations): # Executa o algoritmo pela quantidade de iterações que foi definida, no caso são 5
    start_time = time.time() # Registra o tempo de início da iteração
    tour = nearest_neighbor(distance_matrix)  # Calcula o tour usando a heurística do vizinho mais próximo com fator alpha
    
    # Calcular o custo máximo da solução
    dist_max = 0 # Inicializa o custo máximo como 0
    for i, j in enumerate(tour[:-1]): # Itera sobre os pares consecutivos no tour
        dist_max = max(dist_max, distance_matrix[j][tour[i + 1]]) # Caso o custo máximo se alterar, ele é atualizado
    
    # Registrar tempo, solução e tour
    execution_times.append(time.time() - start_time) # Calcula e registra o tempo de execução da iteração
    solutions.append(dist_max) # Armazena o custo máximo da solução
    tours.append(tour) # Armazena o tour encontrado

# Estatísticas
best_solution_index = solutions.index(min(solutions)) # Índice da melhor solução encontrada
best_solution = solutions[best_solution_index] # Melhor custo máximo
best_tour = tours[best_solution_index] # Melhor tour correspondente
worst_solution = max(solutions) # Pior custo máximo encontrado
average_solution = sum(solutions) / iterations # Média dos custos máximos
average_execution_time = sum(execution_times) / iterations # Média dos tempos de execução

# Resultados
print("\n--- Resultados ---")
print(f"Melhor solução: {best_solution:.2f}") # Imprime a melhor solução
print(f"Pior solução: {worst_solution:.2f}") # Imprime a pior solução
print(f"Valor médio das soluções: {average_solution:.2f}") # Imprime a média das soluções
print(f"Tempo médio de execução: {average_execution_time:.4f} segundos") # Imprime o tempo médio de execução

# Salvar o melhor tour no arquivo especificado pelo usuário
with open(file_final, "w") as file:
    for point in tour: # Escreve cada ponto do tour no arquivo
        file.write("{} ".format(point))

print(f"\nO melhor tour foi salvo no arquivo '{file_final}'.") # Imprime informando que o melhor tour encontrado foi salvo no arquivo de nome informado pelo usuário
