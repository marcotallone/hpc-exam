# Imports ----------------------------------------------------------------------
import pandas as pd
import re
import os

cwd = os.getcwd()

# Version for single file ------------------------------------------------------
# Convert txt to csv -----------------------------------------------------------
input_file = os.path.join(cwd, 'outputs/nbft_reduce.txt')
output_file = os.path.join(cwd, 'datasets/nbft_reduce.csv')

data = []
mapby = None
cores = None
with open(input_file, 'r') as f:
    for line in f:
        if 'A:1|M:' in line:
            parts = line.split('|')
            mapby = parts[1].split(':')[1].strip()
            cores = int(parts[2].split(':')[1].strip())
            comm = cores-1
        elif line[0].isdigit():
            size, latency, min, max, iterations, p50, p95, p99 = line.split()
            data.append([mapby, cores, comm, size, latency, min, max, iterations, p50, p95, p99])

# Create the DataFrame
df = pd.DataFrame(data, columns=['mapby', 'p', 'comm', 'size', 'latency', 'min', 'max', 'iterations', 'p50', 'p95', 'p99'])

# Write the reshaped DataFrame to a new CSV file
df.to_csv(output_file, index=False)

# Version for splitted files ---------------------------------------------------
# Convert txt to csv -----------------------------------------------------------

# input_file_cache = os.path.join(cwd, 'outputs/nbft_cache.txt')
# input_file_core = os.path.join(cwd, 'outputs/nbft_core.txt')
# input_file_socket = os.path.join(cwd, 'outputs/nbft_socket.txt')
# input_file_node = os.path.join(cwd, 'outputs/nbft_node.txt')

# output_file = os.path.join(cwd, 'datasets/nbft.csv')

# # Cache
# data_cache = []
# mapby = None
# cores = None
# with open(input_file_cache, 'r') as f:
#     for line in f:
#         if 'A:1|M:' in line:
#             parts = line.split('|')
#             mapby = parts[1].split(':')[1].strip()
#             cores = int(parts[2].split(':')[1].strip())
#             comm = cores-1
#         elif line[0].isdigit():
#             size, latency, min, max, iterations, p50, p95, p99 = line.split()
#             data_cache.append([size, latency, min, max, iterations, p50, p95, p99, cores, comm, mapby])

# # Core
# data_core = []
# mapby = None
# cores = None
# with open(input_file_core, 'r') as f:
#     for line in f:
#         if 'A:1|M:' in line:
#             parts = line.split('|')
#             mapby = parts[1].split(':')[1].strip()
#             cores = int(parts[2].split(':')[1].strip())
#             comm = cores-1
#         elif line[0].isdigit():
#             size, latency, min, max, iterations, p50, p95, p99 = line.split()
#             data_core.append([size, latency, min, max, iterations, p50, p95, p99, cores, comm, mapby])

# # Socket
# data_socket = []
# mapby = None
# cores = None
# with open(input_file_socket, 'r') as f:
#     for line in f:
#         if 'A:1|M:' in line:
#             parts = line.split('|')
#             mapby = parts[1].split(':')[1].strip()
#             cores = int(parts[2].split(':')[1].strip())
#             comm = cores-1
#         elif line[0].isdigit():
#             size, latency, min, max, iterations, p50, p95, p99 = line.split()
#             data_socket.append([size, latency, min, max, iterations, p50, p95, p99, cores, comm, mapby])

# # Node
# data_node = []
# mapby = None
# cores = None
# with open(input_file_node, 'r') as f:
#     for line in f:
#         if 'A:1|M:' in line:
#             parts = line.split('|')
#             mapby = parts[1].split(':')[1].strip()
#             cores = int(parts[2].split(':')[1].strip())
#             comm = cores-1
#         elif line[0].isdigit():
#             size, latency, min, max, iterations, p50, p95, p99 = line.split()
#             data_node.append([size, latency, min, max, iterations, p50, p95, p99, cores, comm, mapby])

# # Create the dataframes
# df_cache = pd.DataFrame(data_cache, columns=['size', 'latency', 'min', 'max', 'iterations', 'p50', 'p95', 'p99', 'cores', 'comm', 'mapby'])
# df_core = pd.DataFrame(data_core, columns=['size', 'latency', 'min', 'max', 'iterations', 'p50', 'p95', 'p99', 'cores', 'comm', 'mapby'])
# df_socket = pd.DataFrame(data_socket, columns=['size', 'latency', 'min', 'max', 'iterations', 'p50', 'p95', 'p99', 'cores', 'comm', 'mapby'])
# df_node = pd.DataFrame(data_node, columns=['size', 'latency', 'min', 'max', 'iterations', 'p50', 'p95', 'p99', 'cores', 'comm', 'mapby'])

# # Merge the dataframes
# df = pd.concat([df_cache, df_core, df_socket, df_node])

# # Write the reshaped DataFrame to a new CSV file
# df.to_csv(output_file, index=False)
