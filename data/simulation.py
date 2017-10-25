import base64
import data.enabled_collection
import data.lattice
import data.process

import proto.simulation_pb2 as proto_simulation


class Simulation(object):

    def __init__(self, stop_step=None, lattice=None):
        self.STOP_STEP = stop_step or 1000  # Fix. Fail fast.
        self.STOP_TIME = -1

        self.time_usec = 0  # Keep as an int or long, either usec or nsec etc.
        self.step = 0
        self.lattice = (
            lattice if isinstance(lattice, data.lattice.Lattice) else None)
        self.process_queue = None
        self.ELEM_RXNS = None
        self._initialize_lattice()
        self._initialize_process_queue()
        self._initialize_elem_rxns()

        # Enable processes
        # Draw a process, perform if possible, add new enabled processes.
        # (Repeat above)

    def run(self, interactive=False):
        while self._continue_sim():
            # What would it mean if this popped None (was empty)?
            next_process = self.process_queue.pop()
            if next_process.is_still_performable(self.lattice):
                self.step += 1
                self.time_usec = int(next_process.occurence_usec)
                next_process.perform(self.step, self.lattice)
                self.update_process_queue(next_process.sites_coordinates)
                if interactive:
                    cin = input(">>>")
                    if cin == "exit":
                        print(self)
                        print("EXITING")
                        break
                    print(self)

    def _initialize_lattice(self):
        if self.lattice is None:
            self.lattice = data.lattice.Lattice()

    def _initialize_process_queue(self):
        self.process_queue = data.enabled_collection.EnabledCollection(
            key_fn=data.process.Process.key_fn)
        self.update_process_queue([], from_scratch=True)

    def _initialize_elem_rxns(self):
        import settings.elem_rxns_configs.v4.toy_A as toy1_config
        self.ELEM_RXNS = toy1_config.build_rxns_list()
        # print(self.ELEM_RXNS)

    def update_process_queue(self, sites_coordinates, from_scratch=False):
        newly_enabled_processes = set()
        if from_scratch:
            assert not sites_coordinates
            self.process_queue.clear()
            for site in self.lattice.iter_sites():
                newly_enabled_processes.update(
                    self._find_enabled_processes(site))
        else:
            for sites_coordinates in sites_coordinates:
                site = self.lattice[sites_coordinates]
                newly_enabled_processes.update(
                    self._find_enabled_processes(site))
        for process in newly_enabled_processes:
            process.generate_occurence_usec(self.time_usec)
            self.process_queue.add(process)

    def _find_enabled_processes(self, site):
        # Only for /print-toys/{1, 2}
        # BELOW ARE TOY CASES... FOR NOW
        # Move imports to top once done iterating...
        if self.lattice.sites_per_cell == 1:
            # import settings.elem_rxns_configs.v3.toy_A as toy1_config
            if site.state == "A":
                after = "*_0"
            elif site.state == "*_0":
                after = "A"
        elif self.lattice.sites_per_cell == 2:
            site_index = site.coordinates[-1]
            if site_index == 0:
                if site.state == "*_0":
                    after = "O2"
                elif site.state == "O2":
                    after = "*_0"
            elif site_index == 1:
                if site.state == "*_1":
                    after = "CO"
                elif site.state == "CO":
                    after = "*_1"
        else:
            raise NotImplementedError
        return set([
            data.process.Process(
                self.step, {site.coordinates: (site.state, after)}),
        ])

    def _continue_sim(self):
        # TODO include more flexibility on stop conditions
        if self.STOP_TIME > 0:
            return self.STOP_TIME > self.time_usec
        else:
            return self.STOP_STEP > self.step

    def __repr__(self):
        return "s=%d\nt=%d\nLattice:%r\nEnabledCollection:%r" % (
            self.step, self.time_usec, self.lattice, self.process_queue)


# Protocol Buffers (proto or pb) are for the display server.
def to_proto(simulation):
    lattice_pb = data.lattice.to_proto(simulation.lattice)
    pb = proto_simulation.Simulation(lattice=lattice_pb)
    pb.stop_time = simulation.STOP_TIME
    pb.stop_step = simulation.STOP_STEP
    pb.time_usec = simulation.time_usec
    pb.step = simulation.step
    # pb.enabled_collection = (
    #     data.enabled_collection.to_proto(simulation.process_queue))
    # pg.elementary_reaction = (
    #     data.elementary_reaction.to_proto(simulation.ELEM_RXNS))
    return pb


# Protocol Buffers (proto or pb) are for the display server.
def from_proto(pb):
    simulation = Simulation(stop_step=pb.stop_step, lattice=pb.lattice)
    simulation.STOP_TIME = pb.stop_time
    simulation.STOP_STEP = pb.stop_step
    simulation.time_usec = pb.time_usec
    simulation.step = pb.step
    simulation.lattice = data.lattice.from_proto(pb.lattice)
    simulation.enabled_collection = pb.process_queue
    simulation.ELEM_RXNS = pb.elem_rxns
    return simulation


# Protocol Buffers (proto or pb) are for the display server.
def to_proto_b64str(simulation):
    # Serialized bytes as a utf-8 encoded str.
    return base64.b64encode(to_proto(simulation).SerializeToString())


# Protocol Buffers (proto or pb) are for the display server.
def from_proto_b64str(proto_b64str):
    try:
        import binascii
        proto_str = base64.b64decode(proto_b64str)
    except binascii.Error as e:
        raise Exception("Not a valid base64-encoded protobuf.")
    try:
        pb = proto_simulation.Simulation.FromString(proto_str)
    except TypeError as e:
        raise Exception("Not a valid base64-encoded protobuf.")
    return from_proto(pb)
