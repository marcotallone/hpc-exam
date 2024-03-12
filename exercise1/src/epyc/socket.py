from .core import Core
from . import CORES_PER_SOCKET

# Socket class ─────────────────────────────────────────────────────────────────
class Socket:
    """A class to simulate the socket of a computing node.

    Attributes
    ----------
    id : int
        The socket ID.
    node_id : int
        The node ID where the socket is located.
    cores : list
        The list of cores in the socket.
    active_cores : int
        The number of cores running a process.
    """

    # Class variable to keep track of IDs
    next_id = {}

    # Constructor
    def __init__(self, node_id):
        
        if node_id not in Socket.next_id:
            Socket.next_id[node_id] = 0

        self.id = Socket.next_id[node_id]
        Socket.next_id[node_id] += 1
        self.node_id = node_id
        self.cores = [Core(self.id, self.node_id) for i in range(CORES_PER_SOCKET)]
        self.active_cores = 0

    # Method to check if the socket is empty
    def is_empty(self):
        for core in self.cores:
            if core.occupied():
                return False
        return True
    
    # Method to check if the socket is full
    def is_full(self):
        for core in self.cores:
            if not core.occupied():
                return False
        return True

    # Method to add a process to one core of the socket
    def add_process(self, process_id):
        for core in self.cores:
            if not core.occupied():
                core.add_process(process_id)
                self.active_cores += 1
                return True
        return False

    # Method to get a list of processes running on the socket
    def get_processes(self):
        return [core.get_process() for core in self.cores if core.occupied()]

    # Method to get a specific process running on the socket
    def get_process(self, process_id):
        for core in self.cores:
            if core.occupied() and core.process_id == process_id:
                return core.get_process()
        return None

    # Method to count how many cores are occupied
    def get_active_cores(self):
        return self.active_cores

    # Method to remove a process from the socket
    def remove_process(self, process_id):
        for core in self.cores:
            if core.occupied() and core.process_id == process_id:
                core.remove_process()
                self.active_cores -= 1
                return True
        return False

    # Method to remove all processes from the socket
    def remove_all_processes(self):
        for core in self.cores:
            if core.occupied():
                core.remove_process()
                self.active_cores -= 1
        return True
