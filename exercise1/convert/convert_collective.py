# Imports ----------------------------------------------------------------------
import pandas as pd
import re
import os

cwd = os.getcwd()

# Convert txt to csv -----------------------------------------------------------
input_file = os.path.join(cwd, 'outputs/rn.txt')
output_file = os.path.join(cwd, 'datasets/rn.csv')
# algorithm  = 5

data = []
mapby = None
cores = None
with open(input_file, 'r') as f:
    for line in f:
        if 'A:' in line:
            parts = line.split('|')
            algorithm = int(parts[0].split(':')[1].strip())
            mapby = parts[1].split(':')[1].strip()
            cores = int(parts[2].split(':')[1].strip())
            comm = cores-1
        elif line[0].isdigit():
            size, latency, min, max, iterations, p50, p95, p99 = line.split()
            # data.append([mapby, cores, comm, size, latency, min, max, iterations, p50, p95, p99])
            data.append([algorithm, cores, iterations, size, latency, min, max])

# Create the DataFrame
# df = pd.DataFrame(data, columns=['mapby', 'p', 'comm', 'size', 'latency', 'min', 'max', 'iterations', 'p50', 'p95', 'p99'])
df = pd.DataFrame(data, columns=['algorithm','cores','iterations','size','latency','min','max'])

# Write the reshaped DataFrame to a new CSV file
df.to_csv(output_file, index=False)
