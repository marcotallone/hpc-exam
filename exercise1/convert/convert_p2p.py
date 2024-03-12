# Imports ----------------------------------------------------------------------
import pandas as pd
import re
import os

# Current working directory
cwd = os.getcwd()

# Convert p2p latencies to csv -------------------------------------------------

input_file = os.path.join(cwd, 'outputs_full/p2p.txt')
# outout_file_full = os.path.join(cwd, 'datasets/p2p_full.csv')
output_file = os.path.join(cwd, 'datasets/p2p.csv') # <- now this is the full output file

data = []
mapby = None
with open(input_file, 'r') as f:
    for line in f:
        if 'T:osu_latency|M:' in line:
            parts = line.split('|')
            mapby = parts[1].split(':')[1].strip()
            recv = parts[2].split(',')[1].strip()
            iterations = int(parts[3].split(':')[1].strip())
            # iterations = 1000
        elif line[0].isdigit():
            size, latency, p50, p95, p99 = line.split()
            data.append([mapby, size, latency, iterations, p50, p95, p99, recv])

df = pd.DataFrame(data, columns=['mapby', 'size', 'latency', 'iterations',
                                 'p50', 'p95', 'p99', 'recv'])

# Save the  DataFrame to a CSV file
df.to_csv(output_file, index=False)

# Averages (not needed anymore) ------------------------------------------------
# df = df.drop(columns=['recv'])

# # Convert to numeric
# try:
#     df['latency'] = pd.to_numeric(df['latency'])
#     df['iterations'] = pd.to_numeric(df['iterations'])
#     df['p50'] = pd.to_numeric(df['p50'])
#     df['p95'] = pd.to_numeric(df['p95'])
#     df['p99'] = pd.to_numeric(df['p99'])
# except ValueError as e:
#     print("Error:", e)
#     print(df[df['latency'].apply(lambda x: not x.replace('.', '', 1).isdigit())])
#     print(df[df['iterations'].apply(lambda x: not x.isdigit())])
#     print(df[df['p50'].apply(lambda x: not x.replace('.', '', 1).isdigit())])
#     print(df[df['p95'].apply(lambda x: not x.replace('.', '', 1).isdigit())])
#     print(df[df['p99'].apply(lambda x: not x.replace('.', '', 1).isdigit())])

# # Clean the socket: remove rows in which mapby == 'socket' and latency > 4us
# df = df[~((df['mapby'] == 'socket') & (df['latency'] > 4))]

# df_avg = df.groupby(['mapby', 'size'])[['latency', 'iterations', 'p50', 'p95', 'p99']].mean()
# df_avg = df_avg.reset_index()
# df_avg = df_avg.round(2)
# df_avg['size'] = df_avg['size'].astype(int)
# df_avg['iterations'] = df_avg['iterations'].astype(int)
# df_avg.sort_values(by=['mapby', 'size'], inplace=True)

# # Save the result to a CSV file
# df_avg.to_csv(output_file, index=False)