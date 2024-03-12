__version__ = '0.1.0'

# Mpdule imports ───────────────────────────────────────────────────────────────

from .preprocessing import preproc
from .plot import latency_vs_size, latency_vs_cores

__all__ = ['preproc', 'latency_vs_size', 'latency_vs_cores']