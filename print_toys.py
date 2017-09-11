import data.enabled_collection
import data.lattice
import data.process
import data.simulation

K_MAX_TOY_DUMMY_SITES = 5


def get_dummy_lattice(num_dummy_sites):
    if num_dummy_sites > K_MAX_TOY_DUMMY_SITES:
        raise PrintToysError("Too many dummy sites, no example defined.")
    return _populate_dummy_lattice(num_dummy_sites)


def lattice_examples():
    for num_sites in range(1, K_MAX_TOY_DUMMY_SITES + 1):
        print("%d site(s) per cell: " %
            num_sites)
        lattice = _populate_dummy_lattice(num_sites)
        print("Lattice: %r" % lattice)
        for cell in lattice.iter_cells():
            print(cell)
        print("\n\n")


def process_examples():
    def __current_sites_states(lattice, process):
        sites = []
        for site_coordinates in sorted(process.transition_by_site.keys()):
            sites.append(lattice.sites[site_coordinates])
        return sites
    for num_sites in range(1, K_MAX_TOY_DUMMY_SITES + 1):
        lattice = _populate_dummy_lattice(num_sites)
        process = None
        if num_sites == 1:
            remove = _populate_dummy_process(lattice, num_sites)
            process = remove
            print("%d site per cell: Removal of A" % num_sites)
        if num_sites == 2:
            introduce = _populate_dummy_process(lattice, num_sites)
            process = introduce
            print("%d sites per cell: Introduce O2" % num_sites)
        if num_sites == 3:
            swap_bridge = _populate_dummy_process(lattice, num_sites)
            process = swap_bridge
            print("%d sites per cell: "
                "SwapBridge-(bridge,bridge,hollow)(XYZ)" % num_sites)
        if num_sites == 4:
            clear_random = _populate_dummy_process(lattice, num_sites)
            process = clear_random
            print("%d site per cell: RandomFill" % num_sites)
        if num_sites == 5:
            breakdown = _populate_dummy_process(lattice, num_sites)
            process = breakdown
            print("%d site per cell: Breakdown of CO2" % num_sites)
        if process:
            print("\tProcess:\n\t%r" % process)
            print("before...")
            print("\tSites:\n\t%r" % __current_sites_states(lattice, process))
            print("\tLattice:\n\t%r" % lattice)
            process.perform(lattice)
            print("\nafter...")
            print("\tSites:\n\t%r" % __current_sites_states(lattice, process))
            print("\tLattice:\n\t%r" % lattice)
        print("\n\n")


def simulation_examples():
    simulation = data.simulation.Simulation()
    print("%r\n\n" % simulation)


def enabled_collection_examples():
    key_fn = data.process.Process.key_fn
    ec = data.enabled_collection.EnabledCollection(key_fn=key_fn)
    for num_sites in range(1, K_MAX_TOY_DUMMY_SITES + 1):
        lattice = _populate_dummy_lattice(num_sites)
        process = None
        if num_sites == 1:
            remove = _populate_dummy_process(lattice, num_sites)
            process = remove
            ec.add(process)
            print("%d site per cell: simple EnabledCollection .pop()" %
                num_sites)
            print("before:\n\t%r" % ec)
            popped_process = ec.pop()
            print("poppped process:\n\t%r" % popped_process)
            print("after:\n\t%r" % ec)
            print("\n\n")
        if num_sites == 2:
            introduce = _populate_dummy_process(lattice, num_sites)
            process = introduce
        if num_sites == 3:
            swap_bridge = _populate_dummy_process(lattice, num_sites)
            process = swap_bridge
        if num_sites == 4:
            clear_random = _populate_dummy_process(lattice, num_sites)
            process = clear_random
        if num_sites == 5:
            breakdown = _populate_dummy_process(lattice, num_sites)
            process = breakdown


def _populate_dummy_process(lattice, num_sites):
    possible_changes = {}
    if num_sites == 1:
        starting = ["A"]
        ending = ["*_0"]
        toy_cell = lattice.cells[(0, 0)]
        assert list(toy_cell.site_states()) == starting
        transition_by_site = {
            (0, 0, 0): (starting[0], ending[0]),
        }
        # TODO
        possible_changes.update({
            "*_0": ["A"],
            "A": ["*_0"],
        })
    elif num_sites == 2:
        starting = ["*_0", "CO"]
        ending = ["O2", "CO"]
        toy_cell = lattice.cells[(0, 1)]
        assert list(toy_cell.site_states()) == starting
        transition_by_site = {
            (0, 1, 0): (starting[0], ending[0]),
        }
        # TODO
        possible_changes.update({
            "*_0": ["O2"],
            "*_1": ["CO"],
            "O2": ["*_0"],
            "CO": ["*_1"],
        })
    elif num_sites == 3:
        starting = ["X_bridge", "*_1", "Z_hollow"]
        ending = ["*_0", "Y_bridge", "Z_hollow"]
        toy_cell = lattice.cells[(1, 0)]
        assert list(toy_cell.site_states()) == starting
        transition_by_site = {
            (1, 0, 0): (starting[0], ending[0]),
            (1, 0, 1): (starting[1], ending[1]),
        }
        # TODO
        possible_changes.update({
            "*_0": ["X_bridge"],
            "*_1": ["Y_bridge"],
            "*_2": ["Z_hollow"],
            "X_bridge": ["*_0"],
            "Y_bridge": ["*_1"],
            "Z_hollow": ["*_2"],
        })
    elif num_sites == 5:
        starting = ["*_0", "*_1", "CO2", "CO2", "*_4"]
        ending = ["CO", "CO", "*_2", "*_3", "O2"]
        toy_cell = lattice.cells[(0, 1)]
        assert list(toy_cell.site_states()) == starting
        transition_by_site = {
            (0, 1, 0): (starting[0], ending[0]),
            (0, 1, 1): (starting[1], ending[1]),
            (0, 1, 2): (starting[2], ending[2]),
            (0, 1, 3): (starting[3], ending[3]),
            (0, 1, 4): (starting[4], ending[4]),
        }
        # TODO
        possible_changes.update({
            "*_0": ["CO"],
            "*_1": ["CO"],
            "*_2": ["CO2"],
            "*_3": ["CO2"],
            "*_4": ["O2"],
            "CO": ["*_0", "*_1"],
            "CO2": ["*_2", "*_3"],
            "O2": ["*_4"],
        })
    else:
        starting = []
        ending = []
        for index in range(num_sites):
            hole_for_index = "*_%d" % index
            species = "<draw_allowable(cell, site_%d)>" % index
            # TODO
            possible_changes[species] = hole_for_index
            possible_changes[hole_for_index] = species
            starting.append(hole_for_index)
            ending.append(species)
        toy_cell = lattice.cells[(0, 1)]
        assert list(toy_cell.site_states()) == starting
        transition_by_site = {(0, 1, index): (starting[index], ending[index])
            for index in range(num_sites)}
    # TODO - Need some form of rules for enabling processes...
    for starting_site, ending_site in zip(starting, ending):
        valid_site_change = ending_site in possible_changes[starting_site]
        assert (starting_site == ending_site) or valid_site_change

    sim_step = 1  # Whatever for now.
    occurence_time = 0.027  # Whatever for now.
    return data.process.Process(sim_step, occurence_time, transition_by_site)


def _populate_dummy_lattice(num_sites):
    lattice = data.lattice.Lattice(num_sites=num_sites)
    if num_sites == 1:
        for index, state in enumerate(["A"]):
            lattice.sites[(0, 0, index)].state = state
    elif num_sites == 2:
        for index, state in enumerate(["O2", "CO"]):
            lattice.sites[(0, 0, index)].state = state
        for index, state in enumerate(["*_0", "CO"]):
            lattice.sites[(0, 1, index)].state = state
        for index, state in enumerate(["O2", "*_1"]):
            lattice.sites[(1, 0, index)].state = state
        # Empty (1, 1,)
    elif num_sites == 3:
        for index, state in enumerate(["X_bridge", "Y_bridge", "*_2"]):
            lattice.sites[(0, 0, index)].state = state
        for index, state in enumerate(["*_0", "*_1", "Z_hollow"]):
            lattice.sites[(0, 1, index)].state = state
        for index, state in enumerate(["X_bridge", "*_1", "Z_hollow"]):
            lattice.sites[(1, 0, index)].state = state
        for index, state in enumerate(["*_0", "Y_bridge", "Z_hollow"]):
            lattice.sites[(1, 1, index)].state = state
    elif num_sites == 5:
        for index, state in enumerate(["*_0", "*_1", "*_2", "*_3", "*_4"]):
            lattice.sites[(0, 0, index)].state = state
        for index, state in enumerate(["*_0", "*_1", "CO2", "CO2", "*_4"]):
            lattice.sites[(0, 1, index)].state = state
        for index, state in enumerate(["CO", "CO", "*_2", "*_3", "O2"]):
            lattice.sites[(1, 0, index)].state = state
        for index, state in enumerate(["CO", "CO", "*_2", "*_3", "O2"]):
            lattice.sites[(1, 1, index)].state = state

    else:
        # Exists a dist of "allowed" occupants, dependpent on cell's state.
        example_sites = ["<draw_allowable(cell, site_%d)>" % index
            for index in range(num_sites)]
        for index, state in enumerate(example_sites):
            lattice.sites[(0, 0, index)].state = state
    return lattice


class PrintToysError(Exception):
    pass
