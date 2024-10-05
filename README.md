# Jacob Lorenzo
# COS 470 Assignment 3
# 10 / 4 / 2024

# The main program of this file is main.py
# If you pass in the parameter -h you can see all of the different options for customization of the algorithm.
# Unfortunately, I've found that the dynamic mutation seems to start to stagnate which means that it has a difficult time reaching the ideal end state.
# It's able to reach the desired string with smaller texts, but when you reach the hundreds, it starts to slow down and the stagnation doesn't improve. 

# There are two .txt files provided, detault.txt contains a bunch of lorem ipsum text, and default_2.txt contains a smaller string. 

# There are arguments to control:
# Mutation Rate
# Crossover
# Population Size
# Survival Rate
# Crossover Type
# Elitism
# Max Generations

# command I was using: py -3.9 main.py -po 1000 -ma 4000 -e True -s .3 -ct single