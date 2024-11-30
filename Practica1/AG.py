import random
import csv

# Función objetivo (ya proporcionada)
def objective_function(x1, x2, x3, y1, y2, w1, w2, w3, w4):
    return -150*x1 - 230*x2 - 260*x3 - 238*y1 - 210*y2 + 170*w1 + 150*w2 + 36*w3 + 10*w4

# Comprobación de restricciones (ya proporcionada)
def check_constraints(x1, x2, x3, y1, y2, w1, w2, w3, w4):
    violations = 0
    if x1 + x2 + x3 > 500:
        violations += 1
    if 2.5 * x1 + y1 - w1 < 200:
        violations += 1
    if 3 * x2 + y2 - w2 > 240:
        violations += 1
    if w3 + w4 > 20 * x3:
        violations += 1
    if w3 > 6000:
        violations += 1
    return violations

# Generación de población
def generate_population(size=50):
    population = []
    for _ in range(size):
        individual = {
            'x1': random.uniform(0, 500),
            'x2': random.uniform(0, 500),
            'x3': random.uniform(0, 500),
            'y1': random.uniform(0, 200),
            'y2': random.uniform(0, 240),
            'w1': random.uniform(0, 300),
            'w2': random.uniform(0, 260),
            'w3': random.uniform(0, 6000),
            'w4': random.uniform(0, 6000)
        }
        population.append(individual)
    return population

# Evaluar fitness de un individuo
def evaluate_fitness(individual):
    x1, x2, x3, y1, y2, w1, w2, w3, w4 = (individual['x1'], individual['x2'], individual['x3'],
                                           individual['y1'], individual['y2'], individual['w1'],
                                           individual['w2'], individual['w3'], individual['w4'])
    
    # Verificar si las restricciones se cumplen
    if check_constraints(x1, x2, x3, y1, y2, w1, w2, w3, w4) > 0:
        return float('-inf')  # Penaliza individuos que no cumplen restricciones
    
    # Si cumple las restricciones, devuelve el valor de la función objetivo
    return objective_function(x1, x2, x3, y1, y2, w1, w2, w3, w4)

# Selección por torneo
def tournament_selection(population, tournament_size=3):
    selected = random.sample(population, tournament_size)
    selected.sort(key=lambda ind: evaluate_fitness(ind), reverse=True)
    return selected[0]

# Operador de cruzamiento (crossover)
def crossover(parent1, parent2):
    child = {}
    crossover_point = random.randint(1, 8)  # Número aleatorio para cruzar entre variables
    
    for i, key in enumerate(parent1.keys()):
        if i < crossover_point:
            child[key] = parent1[key]
        else:
            child[key] = parent2[key]
    return child

# Operador de mutación
def mutation(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        mutation_point = random.choice(list(individual.keys()))
        individual[mutation_point] = random.uniform(0, 500)  # Cambia el valor dentro del rango
    return individual

# Función principal del algoritmo genético
def genetic_algorithm(population_size=50, generations=100, mutation_rate=0.1, csv_file='Practica1/genetic_algorithm_results.csv'):
    # Generar población inicial
    population = generate_population(population_size)

    # Abrir el archivo CSV para guardar los resultados
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Generacion', 'Mejor Individuo', 'Fitness'])
        
        # Evolucionar por generaciones
        for gen in range(generations):
            new_population = []
            
            # Selección, cruzamiento y mutación para crear la nueva población
            while len(new_population) < population_size:
                parent1 = tournament_selection(population)
                parent2 = tournament_selection(population)
                
                # Cruzamiento
                child = crossover(parent1, parent2)
                
                # Mutación
                child = mutation(child, mutation_rate)
                
                new_population.append(child)

            # Reemplazar la población anterior por la nueva
            population = new_population

            # Obtener el mejor individuo de la generación actual
            best_individual = max(population, key=lambda ind: evaluate_fitness(ind))
            best_fitness = evaluate_fitness(best_individual)
            
            # Guardar el mejor individuo y su fitness en el CSV
            writer.writerow([gen + 1, best_individual, best_fitness])

            print(f"Generación {gen + 1}: Mejor fitness = {best_fitness}")
    
    # Retornar el mejor individuo final
    best_individual = max(population, key=lambda ind: evaluate_fitness(ind))
    return best_individual

# Ejecutar el algoritmo genético y guardar resultados en un archivo CSV
best_solution = genetic_algorithm(population_size=50, generations=1000, mutation_rate=0.1)

# Evaluar el fitness de la mejor solución
best_fitness = evaluate_fitness(best_solution)

# Imprimir la mejor solución y su fitness
print("Mejor solución encontrada:")
print(best_solution)
print(f"Fitness de la mejor solución: {best_fitness}")
