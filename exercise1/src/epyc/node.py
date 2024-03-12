from .socket import Socket
from . import NODES, SOCKETS_PER_NODE, CORES_PER_SOCKET, MAX_PROC_ID, ASSIGNED_IDS

# Node class ───────────────────────────────────────────────────────────────────
class Node:
    """A class to simulate a computing node.

    Parameters
    ----------
    None

    Attributes
    ----------
    id : int
        The node ID.
    sockets : list
        The list of sockets in the node.

    Examples
    --------
    >>> n1 = Node()
    >>> n2 = Node()
    """

    # Class variable to keep track of IDs
    next_id = 0

    # Constructor
    def __init__(self):
        self.id = Node.next_id

        # Check if the maximum number of nodes has been reached
        if Node.next_id == NODES:
            raise ValueError(f"Maximum number of nodes ({NODES})"
                             f" already reached.")
        Node.next_id += 1
        self.sockets = [Socket(self.id) for i in range(SOCKETS_PER_NODE)]

    # Method to check if the node is empty
    def is_empty(self):
        for socket in self.sockets:
            if not socket.is_empty():
                return False
        return True
    
    # Method to check if the node is full
    def is_full(self):
        for socket in self.sockets:
            if not socket.is_full():
                return False
        return True
    
    # Method to add a process to the node
    def add_process(self, process_id, socket_id):

        # Check if the user is asking for a socket out of range
        if socket_id < 0 or socket_id >= SOCKETS_PER_NODE:
            raise ValueError(f"Socket {socket_id} does not exist"
                             f" in node {self.id}. Only {SOCKETS_PER_NODE}"
                             f" sockets available")

        # Check if the process ID is out of range
        if process_id < 0 or process_id > MAX_PROC_ID:
            raise ValueError(f"Process ID {process_id} is out of range."
                             f" IDs must be in range [0, {MAX_PROC_ID}].")

        # Check if the process ID has already been assigned
        if process_id in ASSIGNED_IDS:
            raise ValueError(f"Process ID {process_id} has already"
                             f" been assigned.")
        
        if self.sockets[socket_id].add_process(process_id):
            # Add the process ID to the set of assigned process IDs
            ASSIGNED_IDS.add(process_id)
            return True
        return False

    # Method to remove a process from the node
    def remove_process(self, process_id):
        for socket in self.sockets:
            if socket.remove_process(process_id):
                return True
        return False
    
    # Method to remove all processes from the node
    def remove_all_processes(self):
        for socket in self.sockets:
            socket.remove_all_processes()

    # Method to get a list of processes running on the node
    def get_processes(self):
        processes = []
        for socket in self.sockets:
            processes.extend(socket.processes())
        return processes

    # Method to get a specific process running on the node
    def get_process(self, process_id):
        for socket in self.sockets:
            process = socket.get_process(process_id)
            if process:
                return process
        return None

    # Method to count how many cores are occupied
    def active_cores(self):
        count = 0
        for socket in self.sockets:
            count += socket.get_active_cores()
        return count

    # Method to count how many sockets are occupied
    def active_sockets(self):
        count = 0
        for socket in self.sockets:
            if not socket.is_empty():
                count += 1
        return count

    # Method to get a list of sockets ids
    def get_sockets_ids(self):
        return [socket.id for socket in self.sockets]

    # Method to print the node with sockets stacked vertically (replaced)
    # def __repr__(self):
    #     node_repr = f'Node {self.id}:\n'
    #     for i, socket in enumerate(self.sockets):
    #         node_repr += '┌──────────────────────────────────┐\n'
    #         node_repr += '│ '
    #         for j, core in enumerate(socket.cores):
    #             status = '🈯' if core.occupied() else '⬛'
    #             if j % 16 == 0 and j != 0:
    #                 node_repr += ' │\n│ '
    #             node_repr += f'{status}'
    #         node_repr += ' │\n'
    #         node_repr += '└──────────────────────────────────┘\n'
    #     return node_repr

    # Method to print the node with sockets stacked horizontally
    def __repr__(self):
        core_ppr = 8
        node_repr = f'\nNode {self.id}:\n'
        # Print top borders
        for i, socket in enumerate(self.sockets):
            if i > 0:  # Add space between sockets
                node_repr += '  '
            node_repr += '┌' + '─' * (core_ppr * 2 + 2) + '┐'
        node_repr += '\n'
        # Print cores
        for row in range(CORES_PER_SOCKET // core_ppr):
            for i, socket in enumerate(self.sockets):
                if i > 0:  # Add space between sockets
                    node_repr += '  '
                node_repr += '│ '
                for j in range(core_ppr):  # Each row has 16 cores
                    core = socket.cores[row * core_ppr + j]
                    status = '✅' if core.occupied() else '⬛'
                    node_repr += f'{status}'
                node_repr += ' │'
            node_repr += '\n'
        # Print bottom borders
        for i, socket in enumerate(self.sockets):
            if i > 0:  # Add space between sockets
                node_repr += '  '
            node_repr += '└' + '─' * (core_ppr * 2 + 2) + '┘'
        return node_repr

    # Method to print the node status
    def status(self):
        print(self)
        print(f'Active cores:\t'
              f'{self.active_cores()} / {SOCKETS_PER_NODE * CORES_PER_SOCKET}')
        print(f'Empty cores:\t'
              f'{SOCKETS_PER_NODE * CORES_PER_SOCKET - self.active_cores()} /' f'{SOCKETS_PER_NODE * CORES_PER_SOCKET}')
        print(f'Active sockets:\t{self.active_sockets()} / {SOCKETS_PER_NODE}')
        print(f'Empty sockets:\t'
              f'{SOCKETS_PER_NODE - self.active_sockets()} /'
              f' {SOCKETS_PER_NODE}')

    # Method to show the numbered processes running on each core
    def show_processes(self):
        core_ppr = 8  # Keep 8 cores per line
        node_repr = f'\nNode {self.id}:\n'
        # Print top borders
        for i, socket in enumerate(self.sockets):
            if i > 0:  # Add space between sockets
                node_repr += '  '
            node_repr += '┌' + '─' * (core_ppr * 4 + 1) + '┐'
        node_repr += '\n'
        # Print cores
        for row in range(CORES_PER_SOCKET // core_ppr):
            for i, socket in enumerate(self.sockets):
                if i > 0:  # Add space between sockets
                    node_repr += '  '
                node_repr += '│ '
                for j in range(core_ppr):  # Each row has 8 cores
                    core = socket.cores[row * core_ppr + j]
                    process_id = core.process_id if core.occupied() else '   '
                    node_repr += f'{process_id:3} '
                node_repr += '│'
            node_repr += '\n'
        # Print bottom borders
        for i, socket in enumerate(self.sockets):
            if i > 0:  # Add space between sockets
                node_repr += '  '
            node_repr += '└' + '─' * (core_ppr * 4 + 1) + '┘'
        print(node_repr)
