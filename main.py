import random
import argparse
import pprint

"""
Things to define

Fitness Function -- Done

Mutation Rate

Parents

Crossover

Population Size -- Done

Survival Rate

Choosing Parents

Elitism

When to Stop?

"""

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
    help="You can supply your own text or use a default",
)

parser.add_argument(
    "-po",
    "--population",
    dest="population",
    type=int,
    default=500,
    action="store",
    help="You can supply your own integer or use a default",
)

parser.add_argument(
    "-m",
    "--mutation",
    dest="mutation",
    type=float,
    default=0.1,
    action="store",
    help="You can supply your own float or use a default",
)

parser.add_argument(
    "-s",
    "--survival",
    dest="survival",
    type=float,
    default=0.5,
    action="store",
    help="You can supply your own float or use a default",
)

parser.add_argument(
    "-pa",
    "--parents",
    dest="parents",
    type=int,
    default=2,
    action="store",
    help="You can supply your own int or use a default",
)

parser.add_argument(
    "-e",
    "--elitism",
    dest="allow_elitism",
    type=bool,
    default=False,
    action="store",
    help="You can supply your own boolean or use a default",
)

parser.add_argument(
    "-ct",
    "--crossover_type",
    dest="crossover_type",
    choices=["single", "two", "uniform"],
    default="uniform",
    action="store",
    help="You can supply your own boolean or use a default",
)

args = parser.parse_args()

TEXT = args.text
POPULATION_SIZE = args.population
SURVIVAL_RATE = args.survival
MUTATION = mutation_rate = args.mutation
PARENT_COUNT = args.parents

CROSSOVER = args.crossover_type
ALLOW_ELITISM = args.allow_elitism

print("Text:", TEXT)
print("Population:", POPULATION_SIZE)
print("Survival Rate:", SURVIVAL_RATE)
print("Mutation Rate:", mutation_rate)
print("Parent Count:", PARENT_COUNT)
print("Allow Elitism:", ALLOW_ELITISM)


def generate_sequence(length: int):
    return random.choices(ASCII, k=length)


def generate_population(
    length: int,
):
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


def sort_population(candidates: list):
    return sorted(candidates, key=lambda x: x[1])


def select_population(candidates: list):
    return candidates[: int(SURVIVAL_RATE * POPULATION_SIZE)]


def perform_crossover(parent_1, parent_2, mutation_rate):

    if CROSSOVER == "single":
        crossover_point = random.randint(range(len(parent_1)))
        return parent_1[:crossover_point] + parent_2[crossover_point]
    elif CROSSOVER == "double":
        crossover_point_1 = random.randint(range(len(parent_1)))
        crossover_point_2 = random.randint(range(crossover_point_1, len(parent_1)))
        return (
            parent_1[:crossover_point_1]
            + parent_2[crossover_point_1:crossover_point_2]
            + parent_1[crossover_point_2:]
        )
    else:
        child = []
        for chromosome_1, chromosome_2 in zip(parent_1, parent_2):
            child.append(
                random.choices(
                    [chromosome_1, chromosome_2, random.choice(ASCII)],
                    weights=[
                        (1 - mutation_rate) / 2,
                        (1 - mutation_rate) / 2,
                        mutation_rate,
                    ],
                )[0]
            )
        return child


def crossover_pool(selected_population, curr_population, mutation_rate):
    new_population = []
    for i in range(POPULATION_SIZE):
        parent_1 = random.choice(selected_population)[0]
        parent_2 = random.choice([i for i in curr_population if i not in parent_1])
        new_population.append(perform_crossover(parent_1, parent_2, mutation_rate))
    return new_population


def enact_survial(curr_population, new_population):
    survival_list = []
    replace_index = 0
    for i in curr_population:
        new_fit = calculate_fitness(new_population[replace_index])[1]
        if calculate_fitness(i)[1] < new_fit:
            survival_list.append(i)
            # print("Kept Old")
            # exit()
        else:
            survival_list.append(new_population[replace_index])
            replace_index += 1
            # print("Replace new")
            # exit()

    # pprint.pprint(survival_list)
    # exit()
    return survival_list


def main():
    curr_population = generate_population(len(TEXT))
    prev_best_fitness = float("inf")
    gens_without_improvement = 0
    max_gens_without_improvement = 100
    while True:
        fitness_list = [calculate_fitness(i) for i in curr_population]
        sorted_list = sort_population(fitness_list)
        print("fittest", fitness_list[0])
        selected_population = select_population(sorted_list)
        new_population = crossover_pool(
            selected_population, curr_population, mutation_rate
        )
        curr_population = enact_survial(curr_population, new_population)

        if fitness_list[0][1] == 0:
            break

        if sorted_list[0][1] >= prev_best_fitness:
            gens_without_improvement += 1
            mutation_rate = (
                MUTATION
                + (1 - MUTATION)
                * gens_without_improvement
                / max_gens_without_improvement
            )
        else:
            gens_without_improvement = 0
            mutation_rate = MUTATION


if __name__ == "__main__":
    main()
