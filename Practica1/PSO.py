import random
import csv

# Función objetivo (proporcionada previamente)
def objective_function(x1, x2, x3, y1, y2, w1, w2, w3, w4):
    return -150*x1 - 230*x2 - 260*x3 - 238*y1 - 210*y2 + 170*w1 + 150*w2 + 36*w3 + 10*w4

# Comprobación de restricciones (proporcionada previamente)
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

# Generación de partículas
def generate_particles(size=50):
    particles = []
    for _ in range(size):
        particle = {
            'position': {
                'x1': random.uniform(0, 500),
                'x2': random.uniform(0, 500),
                'x3': random.uniform(0, 500),
                'y1': random.uniform(0, 200),
                'y2': random.uniform(0, 240),
                'w1': random.uniform(0, 300),
                'w2': random.uniform(0, 260),
                'w3': random.uniform(0, 6000),
                'w4': random.uniform(0, 6000)
            },
            'velocity': {
                'x1': random.uniform(-10, 10),
                'x2': random.uniform(-10, 10),
                'x3': random.uniform(-10, 10),
                'y1': random.uniform(-10, 10),
                'y2': random.uniform(-10, 10),
                'w1': random.uniform(-10, 10),
                'w2': random.uniform(-10, 10),
                'w3': random.uniform(-10, 10),
                'w4': random.uniform(-10, 10)
            },
            'best_position': None,
            'best_fitness': float('-inf')
        }
        particles.append(particle)
    return particles

# Evaluar fitness de una partícula
def evaluate_fitness(particle):
    position = particle['position']
    x1, x2, x3, y1, y2, w1, w2, w3, w4 = (position['x1'], position['x2'], position['x3'],
                                           position['y1'], position['y2'], position['w1'],
                                           position['w2'], position['w3'], position['w4'])
    
    # Verificar si las restricciones se cumplen
    if check_constraints(x1, x2, x3, y1, y2, w1, w2, w3, w4) > 0:
        return float('-inf')  # Penaliza partículas que no cumplen restricciones
    
    # Si cumple las restricciones, devuelve el valor de la función objetivo
    return objective_function(x1, x2, x3, y1, y2, w1, w2, w3, w4)

# Actualización de la velocidad de las partículas
def update_velocity(particle, global_best_position, w=0.5, c1=1.5, c2=1.5):
    new_velocity = {}
    for key in particle['position'].keys():
        r1, r2 = random.random(), random.random()
        new_velocity[key] = (w * particle['velocity'][key] + 
                             c1 * r1 * (particle['best_position'][key] - particle['position'][key]) + 
                             c2 * r2 * (global_best_position[key] - particle['position'][key]))
    return new_velocity

# Actualización de la posición de las partículas
def update_position(particle):
    for key in particle['position'].keys():
        particle['position'][key] += particle['velocity'][key]
        # Asegurar que la posición esté dentro de los límites
        if key in ['x1', 'x2', 'x3']:
            particle['position'][key] = max(0, min(particle['position'][key], 500))
        elif key == 'y1':
            particle['position'][key] = max(0, min(particle['position'][key], 200))
        elif key == 'y2':
            particle['position'][key] = max(0, min(particle['position'][key], 240))
        elif key in ['w1', 'w2', 'w3', 'w4']:
            particle['position'][key] = max(0, min(particle['position'][key], 6000))

# Función principal del algoritmo PSO
def pso_algorithm(population_size=50, generations=100, csv_file='Practica1/pso_results.csv'):
    # Generar partículas iniciales
    particles = generate_particles(population_size)

    # Inicialización de la mejor posición global
    global_best_position = None
    global_best_fitness = float('-inf')

    # Abrir el archivo CSV para guardar los resultados
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Generación', 'Mejor Posición Global', 'Fitness'])

        # Evolucionar por generaciones
        for gen in range(generations):
            # Evaluar fitness de todas las partículas
            for particle in particles:
                fitness = evaluate_fitness(particle)
                # Si la partícula tiene un mejor fitness, actualizar su mejor posición
                if fitness > particle['best_fitness']:
                    particle['best_fitness'] = fitness
                    particle['best_position'] = particle['position']

                # Actualizar la mejor posición global
                if fitness > global_best_fitness:
                    global_best_fitness = fitness
                    global_best_position = particle['position']

            # Actualización de la velocidad y posición de las partículas
            for particle in particles:
                # Asegurarse de que la partícula tiene una mejor posición
                if particle['best_position'] is None:
                    # Si no tiene mejor posición, asignar la posición actual
                    particle['best_position'] = particle['position']

                particle['velocity'] = update_velocity(particle, global_best_position)
                update_position(particle)

            # Guardar el mejor individuo y su fitness en el CSV
            writer.writerow([gen + 1, global_best_position, global_best_fitness])

            print(f"Generación {gen + 1}: Mejor fitness global = {global_best_fitness}")
    
    return global_best_position, global_best_fitness

# Ejecutar el algoritmo PSO y guardar resultados en un archivo CSV
best_position, best_fitness = pso_algorithm(population_size=50, generations=1000)

# Imprimir la mejor posición y su fitness
print("Mejor solución encontrada:")
print(best_position)
print(f"Fitness de la mejor solución: {best_fitness}")
