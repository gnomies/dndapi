import numpy as np
from multiprocessing import Pool

# Target range of days
min_target_days = 65360
max_target_days = 72240

# Best LCM found so far, initialized to a large number
best_lcm = float('inf')

# Best cycle lengths found so far
best_cycles = None

# Range of possible cycle lengths to consider for each moon
min_cycle_length1 = 7  # You can adjust these values
max_cycle_length1 = 29  # You can adjust these values
min_cycle_length2 = 30  # You can adjust these values
max_cycle_length2 = 80  # You can adjust these values
min_cycle_length3 = 100  # You can adjust these values
max_cycle_length3 = 400  # You can adjust these values

# Step size for increasing cycle lengths
step_size = .01  # You can adjust this value

def find_best_cycles(cycle1):
    # Best LCM found so far, initialized to a large number
    best_lcm = float('inf')

    # Best cycle lengths found so far
    best_cycles = None

    for cycle2 in np.arange(min_cycle_length2, max_cycle_length2, step_size):
        for cycle3 in np.arange(min_cycle_length3, max_cycle_length3, step_size):
            # Calculate the LCM of these cycle lengths
            lcm = np.lcm.reduce([int(cycle1 * 100), int(cycle2 * 100), int(cycle3 * 100)]) / 100
            # If this LCM is within the target range and closer to the middle of the range than the best one found so far,
            # update the best LCM and best cycles
            if min_target_days <= lcm <= max_target_days and abs(lcm - (min_target_days + max_target_days) / 2) < abs(best_lcm - (min_target_days + max_target_days) / 2):
                best_lcm = lcm
                best_cycles = [cycle1, cycle2, cycle3]
    return best_lcm, best_cycles

if __name__ == '__main__':
    with Pool() as p:
        results = p.map(find_best_cycles, np.arange(min_cycle_length1, max_cycle_length1, step_size))

    # Find the best result
    best_result = min(results, key=lambda result: abs(result[0] - (min_target_days + max_target_days) / 2))

    # Print the best cycle lengths found
    print('Final best cycle lengths:', best_result[1])
    print('Final best LCM:', best_result[0])
