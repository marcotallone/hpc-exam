__version__ = '0.1.0'

# Constants for AMD EPYC 7H12 (Rome) ───────────────────────────────────────────
NODES = 2
SOCKETS_PER_NODE = 2
CORES_PER_SOCKET = 64
MAX_PROC_ID = NODES*SOCKETS_PER_NODE*CORES_PER_SOCKET - 1
ASSIGNED_IDS = set()

# Modules imports ──────────────────────────────────────────────────────────────
from .process import Process
from .core import Core
from .socket import Socket
from .node import Node
from .mpy import *
from .fit import fit_p2p, fit_nbft, fit_nbft_reduce

__all__ = ['Process', 'Core', 'Socket', 'Node', 'initialize',
           'linear_bcast', 'chain_bcast', 'binary_bcast',
           'linear_reduce', 'chain_reduce', 'binary_reduce',
           'fit_p2p', 'fit_nbft', 'fit_nbft_reduce']