# Jacob Lorenzo
# COS 470 Assignment 3
# 10 / 4 / 2024

import random
import argparse
import pprint
import os
from pathlib import Path

ASCII = "".join(chr(x) for x in range(256))

parser = argparse.ArgumentParser(
    prog="Gentic Algorithm",
    description="""
                   This program takes in a string followed by 
                   other optional parameters to use a Genetic Algorithm 
                   to recreate the string.
                   """,
)

parser.add_argument(
    "-t",
    "--text",
    dest="text",
    type=str,
    default="default.txt",
    action="store",
    help="You can supply your own text here or provide a filename",
)

parser.add_argument(
    "-po",
    "--population",
    dest="population",
    type=int,
    default=250,
    action="store",
    help="Set population size, must be a positive integer",
)

parser.add_argument(
    "-m",
    "--mutation",
    dest="mutation",
    type=float,
    default=0.1,
    action="store",
    help="set mutation rate between 1 and 0.0",
)

parser.add_argument(
    "-s",
    "--survival",
    dest="survival",
    type=float,
    default=0.1,
    action="store",
    help="Set survival percent between 1 and 0.0",
)

parser.add_argument(
    "-e",
    "--elitism",
    dest="allow_elitism",
    type=bool,
    default=True,
    action="store",
    help="Allow parents to be in next generation, boolean",
)

parser.add_argument(
    "-ct",
    "--crossover_type",
    dest="crossover_type",
    choices=["single", "double", "uniform"],
    default="uniform",
    action="store",
    help="Types of crossover: single, double, uniform",
)

parser.add_argument(
    "-ma",
    "--max_generations",
    dest="max_generations",
    type=int,
    default=1000,
    action="store",
    help="Max Generations, must be a positive integer",
)


args = parser.parse_args()

text_path = os.path.join(os.path.dirname(__file__), args.text)
if os.path.exists(text_path):
    TEXT = Path(text_path).read_text().replace("\n", "")
else:
    TEXT = args.text

POPULATION_SIZE = args.population
SURVIVAL_RATE = args.survival
MUTATION = mutation_rate = args.mutation

CROSSOVER = args.crossover_type
ALLOW_ELITISM = args.allow_elitism
MAX_GENERATIONS = args.max_generations
TEXT_LEN = len(TEXT)


def generate_sequence(length):
    return random.choices(ASCII, k=length)


def generate_population(length):
    population = []
    for i in range(POPULATION_SIZE):
        population.append(generate_sequence(length))
    return population


def calculate_fitness(genetic_sequence):
    difference = 0
    for text_char, genetic_char in zip(TEXT, genetic_sequence):
        if text_char != genetic_char:
            difference += 1
    return [genetic_sequence, difference]


def sort_population(candidates):
    return sorted(candidates, key=lambda x: x[1])


def select_population(candidates):
    return candidates[: int(SURVIVAL_RATE * POPULATION_SIZE)]


def mutate(child, mutation_rate):
    for i in range(len(child)):
        if random.random() <= mutation_rate:
            child[i] = random.choice(ASCII)
    return child


def perform_crossover(parent_1, parent_2, mutation_rate):

    if CROSSOVER == "single":
        crossover_point = random.randint(0, len(parent_1) - 1)
        child = parent_1[0:crossover_point] + parent_2[crossover_point:]
    elif CROSSOVER == "double":
        crossover_point_1 = random.randint(0, len(parent_1) - 1)
        crossover_point_2 = random.randint(crossover_point_1, len(parent_1) - 1)
        child = (
            parent_1[:crossover_point_1]
            + parent_2[crossover_point_1:crossover_point_2]
            + parent_1[crossover_point_2:]
        )
    else:
        child = [random.choice([c1, c2]) for c1, c2 in zip(parent_1, parent_2)]

    return mutate(child, mutation_rate)


def crossover_pool(selected_population, curr_population, mutation_rate):
    new_population = []
    parent_1 = random.choices(selected_population, k=POPULATION_SIZE)
    parent_2 = random.choices([i for i in curr_population], k=POPULATION_SIZE)

    for i in range(POPULATION_SIZE):
        new_population.append(
            perform_crossover(parent_1[i][0], parent_2[i], mutation_rate)
        )
    return new_population


def enact_survial(sorted_list, selected_population, new_sorted_list):
    survival_list = []
    replace_index = 0
    iter_list = sorted_list
    if ALLOW_ELITISM:
        iter_list = iter_list[int(SURVIVAL_RATE * POPULATION_SIZE) :]
        survival_list = [x[0] for x in selected_population]
    for i in range(len(iter_list)):
        if iter_list[i][1] < new_sorted_list[replace_index][1]:
            survival_list.append(iter_list[i][0])
        else:
            survival_list.append(new_sorted_list[replace_index][0])
            replace_index += 1
    return survival_list


def dynamic_mutation(curr_population, best_candidate):
    diversity = len(set(["".join(x) for x in curr_population])) / len(curr_population)
    return MUTATION * (1 - (diversity * 1))


def main():
    generations_total = 0
    curr_population = generate_population(TEXT_LEN)
    mutation_rate = MUTATION
    while True:
        fitness_list = [calculate_fitness(i) for i in curr_population]
        sorted_list = sort_population(fitness_list)

        selected_population = select_population(sorted_list)

        new_population = crossover_pool(
            selected_population, curr_population, mutation_rate
        )
        new_fitness_list = [calculate_fitness(i) for i in new_population]
        new_sorted_list = sort_population(new_fitness_list)

        curr_population = enact_survial(
            sorted_list, selected_population, new_sorted_list
        )
        fitness_list = [calculate_fitness(i) for i in curr_population]
        sorted_list = sort_population(fitness_list)

        if sorted_list[0][1] == 0 or generations_total == MAX_GENERATIONS:
            print("generations", generations_total, "fittest", sorted_list[0])
            break
        else:
            print("generations", generations_total, "fittest", sorted_list[0][1])

        generations_total += 1
        mutation_rate = dynamic_mutation(curr_population, sorted_list[0][1])


if __name__ == "__main__":
    main()
