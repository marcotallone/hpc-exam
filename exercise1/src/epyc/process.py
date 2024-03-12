from .fit import fit_p2p, fit_nbft, fit_nbft_reduce

# MPI Process class ────────────────────────────────────────────────────────────
class Process:
    """A class to emulate an MPI process.

    Parameters
    ----------
    id : int
        Process ID.
    core_id : int
        The core ID where the process is running.
    socket_id : int
        The socket ID where the process is running.
    node_id : int
        The node ID where the process is running.
    
    Attributes
    ----------
    id : int
        Process ID.
    core_id : int
        The core ID where the process is running.
    socket_id : int
        The socket ID where the process is running.
    node_id : int
        The node ID where the process is running.

    Examples
    --------
    >>> p1 = Process(1, 0, 0, 0)
    >>> p2 = Process(2, 1, 0, 0)
    """

    # Dictionary to numerically identify the channels
    C = {'cache': 0, 'core': 1, 'socket': 2, 'node': 3}

    # Dictionary to store hockney model parameters
    hockney = fit_p2p()

    # Dictionary to store the linear NBFT fit parameters
    nbft_coefficients = fit_nbft()
    nbft_reduce_coefficients = fit_nbft_reduce()

    # Constructor
    def __init__(self, id, core_id, socket_id, node_id):
        self.id = id
        self.core_id = core_id
        self.socket_id = socket_id
        self.node_id = node_id
        self.sending = False
        self.sent_segments = 0
        self.received = False
        self.received_segments = 0
        self.receivers = []

    # Method to print the process
    def __repr__(self):
        return (f'(P{self.id}|'
                f'C:{self.core_id},'
                f'S:{self.socket_id},'
                f'N:{self.node_id})')

    # Method to determine if 2 processes are in the same node
    def same_node(self, other):
        return self.node_id == other.node_id
    
    # Method to determine if 2 processes are in the same socket
    def same_socket(self, other):
        if self.same_node(other):
            return self.socket_id == other.socket_id
        return False
    
    # Method to determine if 2 processes are in the same CCX (Core Complex)
    # (in this case it meanse that they share the L3 cache)
    def same_cache(self, other):
        if self.same_socket(other):
            return self.core_id // 4 == other.core_id // 4  # [groups of 4]
        return False

    # Time of the NBFT only using channel 'c'
    def t_c_nbft(self, p, size, channel: str):
        """Time of the Non-Blocking Fat Tree (NBFT) only using channel 'c'.

        Parameters
        ----------
        p : int
            Number of processes involved in the communication.
        size : int
            Size of the message to send.
        channel : str
            Channel of communication.

        Returns
        -------
        float
            The latency of the NBFT message transmission.
        """
        if channel == 'cache':
            try:
                return  self.nbft_coefficients['cache'][size][p]
            except KeyError:
                print(f'ERROR: t_c_nbft. '
                      f'No fit for size {size} and {p} processes.')
                exit(1)
        else:
            alpha, beta = self.nbft_coefficients[channel][size]
            return alpha + beta * p

    # Time of a point-to-point (P2P) communication
    def t_p2p(self, size, channel: str):
        """Time of a point-to-point (P2P) communication.

        Parameters
        ----------
        size : int
            Size of the message to send.
        channel : str
            Channel of communication.

        Returns
        -------
        float
            The latency of the P2P message transmission.
        """
        alpha, beta, alpha_big, beta_big = self.hockney[channel]
        if size <= 2**17:
            return alpha + beta * size
        else:
            return (alpha + alpha_big) + (beta + beta_big) * size
        
    # Parallelization factor gamma
    def gamma(self, p, size, channel: str):
        """Parallelization factor gamma.

        Parameters
        ----------
        p : int 
            Number of processes involved in the communication.
        size : int
            Size of the message to send.
        channel : str
            Channel of communication.

        Returns
        -------
        float 
            The parallelization factor gamma.
        """
        return self.t_c_nbft(p, size, channel) / self.t_p2p(size, channel)

    # Ratio od delay between two channels
    def q(self, size, channel1: str, channel2: str):
        """Ratio od delay between two channels for a given size.

        Parameters
        ----------
        size : int
            Size of the message to send.
        channel1 : str
            First channel of communication.
        channel2 : str
            Second channel of communication.

        Returns
        -------
        float
            The ratio of delay between the two channels.
        """
        # Check which channel is greater according to C
        if self.C[channel1] < self.C[channel2]:
            return self.t_p2p(size, channel2) / self.t_p2p(size, channel1)
        else:
            return self.t_p2p(size, channel1) / self.t_p2p(size, channel2)

    # Define a function that always compute a q > 1
    # def q_pos(size, channel1, channel2):
    #     q_value = q(size, channel1, channel2)
    #     if q_value < 1:
    #         return 1 / q_value
    #     else:
    #         return q_value

    # NBFT that can use any channel
    def t_nbft(self, p, size, channel: str):
        """Non-Blocking Fat Tree (NBFT) that can use any channel.

        Parameters
        ----------
        p : int 
            Number of processes involved in the communication.
        size : int
            Size of the message to send.
        channel : str
            Channel of communication.

        Returns
        -------
        float 
            The latency of the NBFT message transmission.
        """
        return self.gamma(p, size, channel) * self.t_p2p(size, channel)

    # Simulates sending a message to a group of processes
    def send(self, others, size=1, segments=1):
        """Simulates the process sending a message to a group of processes
        using a Non-Blocking Fat Tree (NBFT).

        Parameters
        ----------
        others : list
            A list of processes to send the message to.
        size : int, optional
            The size of the message to send. Default is 1 byte.
        segments : int, optional
            The number of segments to send. Default is 1.

        Returns
        -------
        float
            The latency of the NBFT message transmission.
        """

        # Number of communications for each channel
        n0, n1, n2, n3 = 0, 0, 0, 0

        for other in others:
            if self.id == other.id:
                ValueError(f'Process {self.id} cannot send messages to itself.')
            elif other is None:
                ValueError(f'Process {self.id} cannot send a message to'
                        ' a non-existing process.')

            # Determine the number of messages sent through each channel
            if not self.same_node(other): n3+=1
            elif not self.same_socket(other): n2+=1
            elif self.same_cache(other): n0+=1
            else: n1+=1

            # Update the segment count at each send
            other.received_segments += 1

            # Check if the receiver has at least 1 segment so it can send
            if other.received_segments == 1:
                other.sending = True

            # Check if each receivers should still be receiving
            if other.received_segments == segments:
                other.received = True
                self.sending = False 

        # Update the segment count at each send
        self.sent_segments += 1

        # Determing the q-values and compute the NBFT latency
        if n3 > 0:
            p = ( n3
                + n2 // self.q(size, 'node', 'socket')
                + n1 // self.q(size, 'node', 'core')
                + n0 // self.q(size, 'node', 'cache')
                + 1 )
            return self.t_nbft(p, size, 'node')
        
        elif n2 > 0:
            p = ( n2
                + n1 // self.q(size, 'socket', 'core')
                + n0 // self.q(size, 'socket', 'cache')
                + 1 )
            return self.t_nbft(p, size, 'socket')
        
        elif n1 > 0:
            p = ( n1
                + n0 // self.q(size, 'core', 'cache')
                + 1 )
            return self.t_nbft(p, size, 'core')
        
        else:
            return self.t_nbft(n0+1, size, 'cache')

    
    # Reduce functions
        
    # Time of the NBFT only using channel 'c' reduce
    def t_c_nbft_reduce(self, p, size, channel: str):
        """Time of the Non-Blocking Fat Tree (NBFT) only using channel 'c'.

        Parameters
        ----------
        p : int
            Number of processes involved in the communication.
        size : int
            Size of the message to send.
        channel : str
            Channel of communication.

        Returns
        -------
        float
            The latency of the NBFT message transmission.
        """
        if channel == 'cache':
            try:
                return  self.nbft_reduce_coefficients['cache'][size][p]
            except KeyError:
                print(f'ERROR: t_c_nbft. '
                      f'No fit for size {size} and {p} processes.')
                exit(1)
        else:
            alpha, beta = self.nbft_reduce_coefficients[channel][size]
            return alpha + beta * p
        
    # Parallelization factor gamma reduce
    def gamma_reduce(self, p, size, channel: str):
        """Parallelization factor gamma reduce.

        Parameters
        ----------
        p : int 
            Number of processes involved in the communication.
        size : int
            Size of the message to send.
        channel : str
            Channel of communication.

        Returns
        -------
        float 
            The parallelization factor gamma.
        """
        return self.t_c_nbft_reduce(p, size, channel) / self.t_p2p(size, channel)
        
    # NBFT that can use any channel reduce
    def t_nbft_reduce(self, p, size, channel: str):
        """Non-Blocking Fat Tree (NBFT) that can use any channel.

        Parameters
        ----------
        p : int 
            Number of processes involved in the communication.
        size : int
            Size of the message to send.
        channel : str
            Channel of communication.

        Returns
        -------
        float 
            The latency of the NBFT message transmission.
        """
        return self.gamma_reduce(p, size, channel) * self.t_p2p(size, channel)

    # Simulates sending a message to a group of processes reduce
    def send_reduce(self, others, size=1, segments=1):
        """Simulates the process sending a message to a group of processes
        using a Non-Blocking Fat Tree (NBFT).

        Parameters
        ----------
        others : list
            A list of processes to send the message to.
        size : int, optional
            The size of the message to send. Default is 1 byte.

        Returns
        -------
        float
            The latency of the NBFT message transmission.
        """

        # Number of communications for each channel
        n0, n1, n2, n3 = 0, 0, 0, 0

        for other in others:
            if self.id == other.id:
                ValueError(f'Process {self.id} cannot send messages to itself.')
            elif other is None:
                ValueError(f'Process {self.id} cannot send a message to'
                        ' a non-existing process.')

            # Determine the number of messages sent through each channel
            if not self.same_node(other): n3+=1
            elif not self.same_socket(other): n2+=1
            elif self.same_cache(other): n0+=1
            else: n1+=1

            # Update the segment count at each send
            other.received_segments += 1

            # Check if the receiver has at least 1 segment so it can send
            if other.received_segments == 1:
                other.sending = True

            # Check if each receivers should still be receiving
            if other.received_segments == segments:
                other.received = True
                self.sending = False 

        # Update the segment count at each send
        self.sent_segments += 1

        # Determing the q-values and compute the NBFT latency
        if n3 > 0:
            p = ( n3
                + n2 // self.q(size, 'node', 'socket')
                + n1 // self.q(size, 'node', 'core')
                + n0 // self.q(size, 'node', 'cache')
                + 1 )
            return self.t_nbft_reduce(p, size, 'node')
        
        elif n2 > 0:
            p = ( n2
                + n1 // self.q(size, 'socket', 'core')
                + n0 // self.q(size, 'socket', 'cache')
                + 1 )
            return self.t_nbft_reduce(p, size, 'socket')
        
        elif n1 > 0:
            p = ( n1
                + n0 // self.q(size, 'core', 'cache')
                + 1 )
            return self.t_nbft_reduce(p, size, 'core')
        
        else:
            return self.t_nbft_reduce(n0+1, size, 'cache')
