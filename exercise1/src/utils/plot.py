import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# Latency vs Message Size (Mapped by Cores)
def latency_vs_size(df, algorithm, mapping='core'):
    plt.figure(figsize=(10, 6))

    # Set Seaborn theme, grid aesthetic and Matplotlib background and figure size
    sns.set_theme(style="whitegrid", palette="Blues_d", rc={"grid.linestyle": "--", "grid.color": "gray", "grid.alpha": 0.3})

    sns.lineplot(data=df[df['mapby']==mapping], x='size', y='latency', hue='cores', 
                 palette='Blues_d', marker='o', markersize=5, errorbar=None, legend=False)

    # --- Add error bars ---
    # for size in df0['Size'].unique():
    #     subset = df0[df0['Size'] == size]
        # plt.errorbar(subset['Cores'], subset['Avg'], yerr=[subset['Avg']-subset['Min'], subset['Max']-subset['Avg']], fmt='o')

    # --- log scale ---
    # plt.xscale('log')
    # plt.yscale('log')

    plt.title('Average Latency vs Message Size mapped by '+mapping+' (Algorithm ' + algorithm + ')')
    plt.xlabel('Message Size')
    plt.ylabel('Average Latency (us)')
    # plt.legend(title='Cores', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


# Latency vs Cores (Mapped by Message Size)
def latency_vs_cores(df, algorithm, mapping='core'):
    plt.figure(figsize=(10, 6))

    # Set Seaborn theme, grid aesthetic and Matplotlib background and figure size
    sns.set_theme(style="whitegrid", palette="Blues_d", rc={"grid.linestyle": "--", "grid.color": "gray", "grid.alpha": 0.3})

    # sns.lineplot(data=df[df['mapby']==mapping], x='cores', y='latency', hue='size', palette='tab10', marker='o', markersize=5, errorbar=None)
    sns.scatterplot(data=df[df['mapby']==mapping], x='cores', y='latency', hue='size', palette='tab10', marker='o', s=40, legend='full')

    # --- Add error bars ---
    # for size in df0['Size'].unique():
    #     subset = df0[df0['Size'] == size]
        # plt.errorbar(subset['Cores'], subset['Avg'], yerr=[subset['Avg']-subset['Min'], subset['Max']-subset['Avg']], fmt='o')

    # --- log scale ---
    # plt.xscale('log')
    # plt.yscale('log')

    # --- Set x-ticks and x-ticklabels ---
    x_values = np.arange(0, df['cores'].max() + 1, 10)
    plt.xticks(x_values, labels=x_values, rotation = 45)

    plt.title('Average Latency vs Cores mapped by '+mapping+' (Algorithm ' + algorithm + ')')
    plt.xlabel('Cores')
    plt.ylabel('Average Latency (us)')
    plt.legend(title='Message Size', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()