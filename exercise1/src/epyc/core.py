from .process import Process
from . import ASSIGNED_IDS

# Core class ───────────────────────────────────────────────────────────────────
class Core:
    """A class to simulate a CPU core.

    Attributes
    ----------
    id : int
        The core ID.
    busy : bool
        The status of the core.
    socket_id : int
        The socket ID where the core is located.
    node_id : int
        The node ID where the core is located.
    process_id : int
        The process ID running on the core.
    process : Process
        The process running on the core.
    """

    # Class variable to keep track of IDs
    next_id = {}

    # Constructor
    def __init__(self, socket_id, node_id):

        if (socket_id, node_id) not in Core.next_id:
            Core.next_id[(socket_id, node_id)] = 0

        self.id = Core.next_id[(socket_id, node_id)]
        Core.next_id[(socket_id, node_id)] += 1

        self.busy = False
        self.socket_id = socket_id
        self.node_id = node_id
        self.process_id = None
        self.process = None

    # Method to check if the core has a process running
    def occupied(self):
        return self.busy
    
    # Method to add a process to the core
    def add_process(self, process_id):
        if self.busy:
            return False
        self.busy = True
        self.process_id = process_id
        self.process = Process(process_id, self.id, self.socket_id, self.node_id)
        return True

    # Method to get the process running on the core
    def get_process(self):
        return self.process 

    # Method to remove the process from the core
    def remove_process(self):
        ASSIGNED_IDS.remove(self.process_id)
        self.busy = False
        self.process_id = None
        self.process = None

        return True
