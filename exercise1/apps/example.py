from epyc import *
from utils import *

# Create a node
# The maximum number of nodes allocatabel is 2 but this can be modified by
# changing the MAX_NODES constant in the init module file
node1 = Node()
node2 = Node()

# The nodes status can be visualized simply using the print statement
print("Now these nodes are empty:")
print(node1)
print(node2)

# Nodes can be initialized with a number of processes and a mapby parameter as
# done by the map-by option in OpenMPI
print("Now we initialize the nodes with 2 processes each and mapby node:")
p = initialize(node1, node2, n_processes=2, mapby='node')
print(node1)
print(node2)

# Running another time the initialization function will reallocate the processes
print("Now we re-allocate the processes with socket mapping and going up to 132 processes")
p = initialize(node1, node2, n_processes=132, mapby='socket')

# One could also visualize the exact status of the nodes and see where each process is located
print("Let's see where each process is:")
node1.show_processes()
node2.show_processes()

# Onc the processes have been allocated, the module allows to simulate different
# algorithms for the broadcast and reduce collective operations as follows
p = initialize(node1, node2, n_processes=256, mapby='core') 

print("We now re-allocated the node filling them completely with 256 processes and mapby core")
print("In fact here is their status:")
node1.status()
node2.status()

print("We can simulate different collective operations seeing their latency, for instance here for a message size of 1B:")
print(f"\t - linear broadcast latency: {linear_bcast(p, 1)} us")
print(f"\t - chain broadcast latency: {chain_bcast(p, 1)} us")
print(f"\t - binary broadcast latency: {binary_bcast(p, 1)} us")
print(f"\t - linear reduce latency: {linear_reduce(p, 1)} us")
print(f"\t - chain reduce latency: {chain_reduce(p, 1)} us")
print(f"\t - binary reduce latency: {binary_reduce(p, 1)} us")