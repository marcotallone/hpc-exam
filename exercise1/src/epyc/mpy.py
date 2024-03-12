import itertools
from .node import Node
from . import NODES, CORES_PER_SOCKET, SOCKETS_PER_NODE

# MPI simulation functions ─────────────────────────────────────────────────────

# Function to fill the node with processes according to different mappings
def initialize(*nodes, n_processes=1, mapby='core'):
    """Initialize the nodes with processes simulating MPI initialization.

    Parameters
    ----------
    nodes : Node
        The nodes to initialize.
    n_processes : int, optional
        The number of processes to initialize, by default 1.
    mapby : str, optional
        The mapping method to use, by default 'core'.

    Returns
    -------
    list
        A list of processes initialized in the nodes in id order.
    """

    # Remove all resudual processes if there are any
    for node in nodes:
        node.remove_all_processes()

    processes_list = []
    n_id = 0
    p = 0
    if mapby == 'core':
        s_id = 0
        while n_processes > 0:
            if nodes[n_id].is_full():
                n_id += 1
                s_id = 0
            if not nodes[n_id].add_process(p, s_id):
                s_id += 1
            else:
                processes_list.append(nodes[n_id].get_process(p))
                p += 1
                n_processes -= 1
    elif mapby == 'socket':
        s_iter = itertools.cycle(range(SOCKETS_PER_NODE))
        while n_processes > 0:
            if nodes[n_id].is_full():
                n_id += 1
            if not nodes[n_id].add_process(p, next(s_iter)):
                n_id += 1
            else:
                processes_list.append(nodes[n_id].get_process(p))
                p += 1
                n_processes -= 1
    elif mapby == 'node':
        n_iter = itertools.cycle(range(NODES))
        s_seq = [i for i in range(SOCKETS_PER_NODE) for _ in range(NODES)]
        s_iter = itertools.cycle(s_seq)
        while n_processes > 0:
            n_id = next(n_iter)
            s_id = next(s_iter)
            nodes[n_id].add_process(p, s_id)
            processes_list.append(nodes[n_id].get_process(p))
            p += 1
            n_processes -= 1
    else:
        raise ValueError(f"Invalid mapping method: {mapby}."
                         f" Use 'core', 'socket' or 'node'.")
    
    return processes_list

# Broadcast algorithms ─────────────────────────────────────────────────────────

# Linear Broadcast
def linear_bcast(processes_list, size=1):

    # Pick the master process and give it the message to broadcast
    master = processes_list[0]

    # Prepare all the other processes to receive the message
    receivers = processes_list[1:]

    return master.send(receivers, size)

# Chain Broadcast
def chain_bcast(processes_list, size=1, segments=1):

    latency = 0

    # Prepare receivers
    for process in processes_list:
        process.sending = False
        process.sent_segments = 0
        process.received = False
        process.received_segments = 0

        # Each process will be sending to the next one (except last)
        if process.id < len(processes_list) - 1:
            process.receivers = [processes_list[process.id + 1]]

    # Prepare master
    master = processes_list[0]
    master.sending = True
    master.received = True
    master.received_segments = segments

    while not all([process.received for process in processes_list]):

        # Initialize empty times list
        times = []

        # Find all the senders that did not finished last iteration
        senders = [p for p in processes_list[:-1] if p.sending]

        # Send the message to the receivers
        for sender in senders:
            times.append(sender.send(sender.receivers, size, segments)/segments)

        # Update latency
        latency += max(times)
    
    return latency

# Binary tree Broadcast
def binary_bcast(processes_list, size=1, segments=1):

    latency = 0

    # Prepare receivers
    for process in processes_list:
        process.sending = False
        process.sent_segments = 0
        process.received = False
        process.received_segments = 0
        process.receivers = []

        # In a binary tree, each process will be sending to two others
        child1 = 2*process.id + 1
        child2 = 2*process.id + 2
        if child1 < len(processes_list):
            process.receivers.append(processes_list[child1])
        if child2 < len(processes_list):
            process.receivers.append(processes_list[child2])

    # Prepare master
    master = processes_list[0]
    master.sending = True
    master.received = True
    master.received_segments = segments

    while not all([process.received for process in processes_list]):

        # Initialize empty times list
        times = []

        # Find all the senders that did not finished last iteration
        senders = [p for p in processes_list[:-1] if p.sending and not p.receivers == []]

        # Send the message to the receivers
        for sender in senders:
            times.append(sender.send(sender.receivers, size, segments)/segments)
            
        # Update latency
        latency += max(times)
    
    return latency

# Reduce algorithms ────────────────────────────────────────────────────────────

# Linear Reduce
def linear_reduce(processes_list, size=1):

    # Pick the master process and give it the message to reduce
    master = processes_list[0]

    # Prepare all the other processes to receive the message
    receivers = processes_list[1:]

    return master.send_reduce(receivers, size)

# Chain Reduce
def chain_reduce(processes_list, size=1, segments=1):

    latency = 0

    # Prepare receivers
    for process in processes_list:
        process.sending = False
        process.sent_segments = 0
        process.received = False
        process.received_segments = 0

        # Each process will be sending to the next one (except last)
        if process.id < len(processes_list) - 1:
            process.receivers = [processes_list[process.id + 1]]

    # Prepare master
    master = processes_list[0]
    master.sending = True
    master.received = True
    master.received_segments = segments

    while not all([process.received for process in processes_list]):

        # Initialize empty times list
        times = []

        # Find all the senders that did not finished last iteration
        senders = [p for p in processes_list[:-1] if p.sending]

        # Send the message to the receivers
        for sender in senders:
            times.append(sender.send_reduce(sender.receivers, size, segments)/segments)

        # Update latency
        latency += max(times)
    
    return latency

# Binary tree Reduce
def binary_reduce(processes_list, size=1, segments=1):

    latency = 0

    # Prepare receivers
    for process in processes_list:
        process.sending = False
        process.sent_segments = 0
        process.received = False
        process.received_segments = 0
        process.receivers = []

        # In a binary tree, each process will be sending to two others
        child1 = 2*process.id + 1
        child2 = 2*process.id + 2
        if child1 < len(processes_list):
            process.receivers.append(processes_list[child1])
        if child2 < len(processes_list):
            process.receivers.append(processes_list[child2])

    # Prepare master
    master = processes_list[0]
    master.sending = True
    master.received = True
    master.received_segments = segments

    while not all([process.received for process in processes_list]):

        # Initialize empty times list
        times = []

        # Find all the senders that did not finished last iteration
        senders = [p for p in processes_list[:-1] if p.sending and not p.receivers == []]

        # Send the message to the receivers
        for sender in senders:
            times.append(sender.send_reduce(sender.receivers, size, segments)/segments)
            
        # Update latency
        latency += max(times)
    
    return latency
