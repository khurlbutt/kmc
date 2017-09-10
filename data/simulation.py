import data.enabled_collection
import data.lattice
import data.process


class Simulation(object):

    def __init__(self):
        self.lattice = data.lattice.Lattice()
        self.process_queue = data.enabled_collection.EnabledCollection(
            key_fn=data.process.Process.key_fn)
        self.time = 0  # Let's try staying integer/usec, can discuss options.
        # Enable processes
        # Draw a process, perform if possible, add new enabled processes.
        # (Repeat above)

    def __repr__(self):
        return "t=%d\nLattice:%r\nEnabledCollection:%r" % (
            self.time, self.lattice, self.process_queue)
