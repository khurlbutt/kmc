import data.enabled_collection
import data.lattice
import data.process


class Simulation(object):

    def __init__(self):
        self.STOP_TIME = -1
        self.STOP_STEP = 100

        self.time = int(0)  # Keep as an int or long, either usec or nsec etc.
        self.step = 0
        self._initialize_lattice()
        self._initialize_process_queue()

        # Enable processes
        # Draw a process, perform if possible, add new enabled processes.
        # (Repeat above)

    def run(self):
        while self._continue_sim():
            # What would it mean if this popped None (was empty)?
            next_process = self.process_queue.pop()
            if next_process.is_still_performable(self.lattice):
                self.step += 1
                self.time = next_process.occurence_usec
                next_process.perform(self.lattice)
                self._update_process_queue(next_process.sites)

    def _initialize_lattice(self):
        self.lattice = data.lattice.Lattice()

    def _initialize_process_queue(self):
        self.process_queue = data.enabled_collection.EnabledCollection(
            key_fn=data.process.Process.key_fn)
        self.update_process_queue(self.lattice.iter_sites())

    def update_process_queue(self, sites):
        newly_enabled_processes = set()
        # Times not generated, avoid enqueuing the same process more than once.
        for site in sites:
            newly_enabled_processes.update(self._find_enabled_processes(site))
        for process in newly_enabled_processes:
            process.generate_occurence_usec(self.time)
            self.process_queue.add(process)

    def _find_enabled_processes(self, site):
        # Only for /print-toys/1
        if site.state == "A":
            after = "*_0"
        elif site.state == "*_0":
            after = "A"
        return set([
            data.process.Process(
                self.step, {site.coordinates: (site.state, after)}),
        ])

    def _continue_sim(self):
        # TODO include more flexibility on stop conditions
        if self.STOP_TIME > 0:
            return self.STOP_TIME > self.time
        else:
            return self.STOP_STEP > self.step

    def __repr__(self):
        return "t=%d\nLattice:%r\nEnabledCollection:%r" % (
            self.time, self.lattice, self.process_queue)
