import random
import math

# Helper function to initialize a random population
def initialize_population(pop_size, dim, lower_bound, upper_bound):
    population = []
    for _ in range(pop_size):
        solution = [random.uniform(lower_bound, upper_bound) for _ in range(dim)]
        population.append(solution)
    return population

# Helper function to calculate the objective function
def objective_function(solution):
    return math.sqrt((10 - solution[0])**2 + (5 - solution[1])**2 + (8 - solution[2])**2)

# Helper function to update a solution
def update_solution(solution, lower_bound, upper_bound, phi):
    new_solution = []
    for x in solution:
        delta = phi * (random.random() - 0.5)  # Shift the solution a bit with delta
        new_x = x + delta
        # Check to ensure the boundaries are not exceeded
        new_x = min(max(new_x, lower_bound), upper_bound)
        new_solution.append(new_x)
    return new_solution

# ABC algorithm
def abc(pop_size, dim, lower_bound, upper_bound, max_iter, limit):
    # Initialize population
    population = initialize_population(pop_size, dim, lower_bound, upper_bound)

    # Calculate the objective values for each solution
    objective_values = [objective_function(sol) for sol in population]

    # Trial counter to track how many times each solution exceeds the limit
    trial_counter = [0] * pop_size

    # Find the best solution
    best_solution = min(population, key=lambda sol: objective_function(sol))
    best_value = objective_function(best_solution)

    for iteration in range(max_iter):
        # Employed bee phase
        for i in range(pop_size):
            # Randomly select a solution and another random solution different from the first one
            k = random.randint(0, pop_size - 1)
            while k == i:
                k = random.randint(0, pop_size - 1)

            # Update the solution with a random value
            phi = random.uniform(-1, 1)

            # Generate a new solution
            new_solution = update_solution(population[i], lower_bound, upper_bound, phi)

            # Calculate the objective value of the new solution
            new_objective = objective_function(new_solution)
            # Update if improvement is found
            if new_objective < objective_values[i]:
                population[i] = new_solution
                objective_values[i] = new_objective
                trial_counter[i] = 0  # Reset if improvement is found
            else:
                trial_counter[i] += 1  # Increment if no improvement

        # Onlooker bee phase
        total_fitness = sum(1.0 / (1.0 + value) for value in objective_values)
        fitness = [1.0 / (1.0 + value) / total_fitness for value in objective_values]

        # We increase exploitation capacity here
        for i in range(pop_size):
            if random.random() < fitness[i]:  # Select based on fitness
                # Randomly select another solution
                k = random.randint(0, pop_size - 1)
                while k == i:
                    k = random.randint(0, pop_size - 1)

                # Update the solution with a random value
                phi = random.uniform(-1, 1)

                # Generate a new solution
                new_solution = update_solution(population[i], lower_bound, upper_bound, phi)

                # Calculate the objective value of the new solution
                new_objective = objective_function(new_solution)
                # Update if improvement is found
                if new_objective < objective_values[i]:
                    population[i] = new_solution
                    objective_values[i] = new_objective
                    trial_counter[i] = 0
                else:
                    trial_counter[i] += 1

        # Scout bee phase
        for i in range(pop_size):
            if trial_counter[i] >= limit:
                # If a solution hasn't improved for a while, generate a new random solution
                population[i] = [random.uniform(lower_bound, upper_bound) for _ in range(dim)]
                objective_values[i] = objective_function(population[i])
                trial_counter[i] = 0  # Reset

        # Check for the best solution
        current_best_solution = min(population, key=lambda sol: objective_function(sol))
        current_best_value = objective_function(current_best_solution)

        if current_best_value < best_value:
            best_solution = current_best_solution
            best_value = current_best_value

        print(f"Iteration {iteration}: Best Value = {best_value}")

    return best_solution, best_value

# Parameters for running the ABC algorithm
pop_size = 20  # Population size
dim = 3  # Dimensionality of the solution space
lower_bound = -10  # Lower bound of the solution space
upper_bound = 10  # Upper bound of the solution space
max_iter = 1000  # Maximum number of iterations
limit = 20  # Limit for scout bees

best_solution, best_value = abc(pop_size, dim, lower_bound, upper_bound, max_iter, limit)

print(f"Best Solution: {best_solution}")
print(f"Best Value: {best_value}")
