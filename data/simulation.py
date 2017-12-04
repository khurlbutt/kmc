import data.enabled_collection
import data.lattice
import data.process


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
        self._maybe_initialize_lattice()
        self._maybe_initialize_elem_rxns()
        self._maybe_initialize_process_queue()

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
                self.update_process_queue(next_process.sites_coordinates())
                if interactive:
                    cin = input(">>>")
                    if cin == "exit":
                        print("EXITING")
                        break
                    print(self)
        print("ending simulation run...\n%r" % self)

    def _maybe_initialize_lattice(self):
        if self.lattice is None:
            self.lattice = data.lattice.Lattice()

    def _maybe_initialize_process_queue(self):
        if self.process_queue is None:
            self.process_queue = data.enabled_collection.EnabledCollection(
                sorting_fn=data.process.Process.enabled_collection_sorting_fn)
            self.update_process_queue(None, from_scratch=True)

    def _maybe_initialize_elem_rxns(self):
        # Only for /print-toys/{1, 2, 3}
        # BELOW ARE TOY CASES... FOR NOW
        # Move imports to top once done iterating...
        if self.ELEM_RXNS is None:
            if self.lattice.sites_per_cell == 1:
                import settings.elem_rxns_configs.v5.toy_A as toy1_config
                self.ELEM_RXNS = toy1_config.build_rxns_list()
            elif self.lattice.sites_per_cell == 2:
                import settings.elem_rxns_configs.v5.XY_oxidation as toy2_config
                self.ELEM_RXNS = toy2_config.build_rxns_list()
            elif self.lattice.sites_per_cell == 3:
                import settings.elem_rxns_configs.v5.CO_oxidation as toy3_config
                self.ELEM_RXNS = toy3_config.build_rxns_list()
            # TODO: moar dummies n toys... yippee

        if not self.ELEM_RXNS:
            raise NotImplementedError("ELEM_RXNS not initialized.")

    def update_process_queue(self, sites_coordinates, from_scratch=False):
        newly_enabled_processes = set()
        if from_scratch:
            assert not sites_coordinates
            self.process_queue.clear()
            for site in self.lattice.iter_sites():
                newly_enabled_processes.update(
                    self._find_enabled_processes(site))
        else:
            for site_coordinates in sites_coordinates:
                site = self.lattice[site_coordinates]
                newly_enabled_processes.update(
                    self._find_enabled_processes(site))
        for process in newly_enabled_processes:
            process.generate_occurence_usec(self.time_usec)
            self.process_queue.add(process)

    def _find_enabled_processes(self, site):
        enabled_processes = set()
        # Iterate over all possible elementary reactions in this simulation.
        for elem_rxn in self.ELEM_RXNS:
            # Consider every transition for this reaction, and whether the site
            # could validly play a part.
            for potential_site_transition in elem_rxn.transitions:
                cell_offset = [
                    int(c) for c in potential_site_transition.cell_coordinates
                ]
                # Valid transitions have reactant matching the site's adsorbate.
                if potential_site_transition.reactant == site.state:
                    # Before we promote reaction to enabled process, must check
                    # validity of other transitions.
                    num_valid_transitions = 0
                    transition_by_site = {}
                    for inner_transition in elem_rxn.transitions:
                        # Given outer-loop's site has a known lattice position
                        # and offset, now find coordinates on lattice for inner.
                        inner_cell_offset = [
                            int(c) for c in inner_transition.cell_coordinates
                        ]
                        # Vector operation using lists performs a translation,
                        #   e.g. site at (42, 3) has cell_offset of (1, 0) while
                        #        inner_transition offset is (1,1)... so (42, 4).
                        translated_site_coords = []
                        for i in range(len(site.coordinates) - 1):
                            translated_site_coords.append(
                                site.coordinates[i] + (
                                    inner_cell_offset[i] - cell_offset[i])
                            )
                        # Offset doesn't apply, no translatation necessary.
                        translated_site_coords.append(
                            inner_transition.site_index)
                        inner_site_key = tuple(translated_site_coords)
                        if (inner_transition.reactant ==
                                self.lattice[inner_site_key].state):
                            num_valid_transitions += 1
                            transition_by_site[inner_site_key] = (
                                inner_transition.reactant,
                                inner_transition.product,
                            )
                    if num_valid_transitions == len(elem_rxn.transitions):
                        enabled_processes.add(
                            data.process.Process(self.step, transition_by_site))
        return enabled_processes

    def _continue_sim(self):
        # TODO include more flexibility on stop conditions
        # if self.STOP_TIME > 0:
        #     return self.STOP_TIME > self.time_usec
        # else:
        #     return self.STOP_STEP > self.step
        return self.STOP_STEP > self.step

    def __repr__(self):
        return "step=%d\ntime=%d\nLattice:%r\nEnabledCollection:%r" % (
            self.step, self.time_usec, self.lattice, self.process_queue)
