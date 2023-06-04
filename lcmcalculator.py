import numpy as np

# Your periods in tenths of days
periods = [80, 279, 1523]

# Calculate the least common multiple
lcm = np.lcm.reduce(periods)

# Print the result
print((lcm/10)/344)
