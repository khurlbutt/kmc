import data.enabled_collection
import data.lattice
import data.process


class Simulation(object):

    def __init__(self):
        self._initialize_lattice()
        self._initialize_process_queue()
        self.time = 0.0
        self.step = 0

        self.STOP_TIME = -1.0
        self.STOP_STEP = 100

        # 
        # Enable processes
        # Draw a process, perform if possible, add new enabled processes.
        # (Repeat above)

    def _initialize_lattice(self):
        self.lattice = data.lattice.Lattice()
        return lattice

    def _initialize_process_queue(self):
        self.process_queue = data.enabled_collection.EnabledCollection(
            key_fn=data.process.Process.key_fn)
        self._update_process_queue(self.lattice.enumerate_sites())

    def _update_process_queue(self, sites):
        running_process_set = set()
        for site in sites:
            running_process_set.add(
                self._update_process_queue_helper(site))
        for process in running_process_set:
            process.generate_expected_time()
            self.process_queue.add(process)

    def _update_process_queue_helper(self, site):
        # TODO...
        return set()


    def _continue_sim(self):
        # TODO include more flexibility on stop conditions
        if self.STOP_TIME > 0:
            return self.STOP_TIME > self.time
        else:
            return self.STOP_STEP > self.step

    def run(self):
        while self._continue_sim():
            next_process = self.process_queue.pop()
            if next_process.is_still_performable(self.lattice):
                self.step += 1
                self.time = next_process.occurence_time
                next_process.perform(self.lattice)
                self._update_process_queue(next_process.sites)

    def __repr__(self):
        return "t=%d\nLattice:%r\nEnabledCollection:%r" % (
            self.time, self.lattice, self.process_queue)
