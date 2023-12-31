# -*- coding: utf-8 -*-
"""Pregunta1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qvv__jGBq5geEhdjqqo5haNjH4UCL46S
"""

pip install deap

import random
from deap import base, creator, tools, algorithms

# Parámetros del problema
num_ants = 10  # Número de hormigas
grid_size = 10  # Tamaño del entorno bidimensional
max_moves = 100  # Número máximo de movimientos permitidos para cada hormiga

# Función de evaluación
def evaluate(individual):
    # Inicializar la posición de las hormigas
    positions = [(0, 0)] * num_ants

    # Calcular la distancia total recorrida
    total_distance = 0

    for move in individual:
        # Actualizar las posiciones de las hormigas
        for i in range(num_ants):
            x, y = positions[i]

            if move == 0:  # Arriba
                y = max(y - 1, 0)
            elif move == 1:  # Abajo
                y = min(y + 1, grid_size - 1)
            elif move == 2:  # Izquierda
                x = max(x - 1, 0)
            elif move == 3:  # Derecha
                x = min(x + 1, grid_size - 1)

            positions[i] = (x, y)

        # Calcular la distancia recorrida en el movimiento actual
        total_distance += sum(abs(x - grid_size // 2) + abs(y - grid_size // 2) for x, y in positions)

    return total_distance,

# Configuración de DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()
toolbox.register("attr_int", random.randint, 0, 3)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=max_moves)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=3, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(42)

    population_size = 100
    num_generations = 50

    population = toolbox.population(n=population_size)

    for generation in range(num_generations):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)

        fitnesses = toolbox.map(toolbox.evaluate, offspring)
        for ind, fit in zip(offspring, fitnesses):
            ind.fitness.values = fit

        population = toolbox.select(offspring, k=population_size)

    best_individual = tools.selBest(population, k=1)[0]
    best_fitness = evaluate(best_individual)[0]

    print("Mejor individuo:", best_individual)
    print("Fitness:", best_fitness)

if __name__ == "__main__":
    main()

