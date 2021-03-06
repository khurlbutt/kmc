import data.enabled_collection
import data.lattice
import data.process
import data.simulation

K_MAX_TOY_DUMMY_SITES = 5


def simulation_from_scratch(num_dummy_sites, stop_step):
    axis_lengths = (10, 10)
    lattice = get_dummy_lattice(
        axis_lengths, num_dummy_sites, empty=True)
    simulation = data.simulation.Simulation(
        lattice=lattice, stop_step=stop_step)
    return simulation


def get_dummy_lattice(axis_lengths, num_dummy_sites, empty=False):
    if num_dummy_sites > K_MAX_TOY_DUMMY_SITES:
        raise PrintToysError("Too many dummy sites, no example defined.")
    return _populate_dummy_lattice(num_dummy_sites, axis_lengths=axis_lengths,
        empty=empty)


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
        for site_coordinates in sorted(process.sites_coordinates()):
            sites.append(lattice[site_coordinates])
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
            print("%d sites per cell: XY split sites" % num_sites)
        if num_sites == 3:
            swap_bridge = _populate_dummy_process(lattice, num_sites)
            process = swap_bridge
            print("%d sites per cell: XYZ (br,br,hol) for CO2" % num_sites)
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
            step = 0
            process.perform(step, lattice)
            print("\nafter...")
            print("\tSites:\n\t%r" % __current_sites_states(lattice, process))
            print("\tLattice:\n\t%r" % lattice)
        print("\n\n")


def simulation_examples():
    simulation = data.simulation.Simulation()
    print("%r\n\n" % simulation)


def simulation_interactive(num_sites=1):
    simulation = data.simulation.Simulation()
    simulation.run(interactive=True)


def simulate_lattice(lattice, stop_step=None):
    if stop_step is None:
        raise PrintToysError("Need stop step to simulate to.")
    if lattice.sites_per_cell == 1:
        if lattice.coordinate_cardinalities[0:2] != (10, 10):
            axis = lattice.coordinate_cardinalities[0:2]
            print("Bad news, but shrugz for now: lattice axis: %r" % (
                list(axis)))
            lattice = data.lattice.Lattice()
    elif lattice.sites_per_cell == 2:
        if lattice.coordinate_cardinalities[0:2] != (10, 10):
            print("Bad news, but shrugz for now.")
            lattice = data.lattice.Lattice(sites_per_cell=2)
    elif lattice.sites_per_cell == 3:
        if lattice.coordinate_cardinalities[0:2] != (10, 10):
            print("Bad news, but shrugz for now.")
            lattice = data.lattice.Lattice(sites_per_cell=3)
    else:
        raise PrintToysError("Haven't built stop_step for this toy... yet!")
    simulation = data.simulation.Simulation(
        lattice=lattice, stop_step=stop_step)
    simulation.run()
    return simulation.lattice


def enabled_collection_examples():
    sorting_fn = data.process.Process.enabled_collection_sorting_fn
    ec = data.enabled_collection.EnabledCollection(sorting_fn=sorting_fn)
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
        toy_cell = lattice[(0, 0)]
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
        starting = ["*_0", "Y"]
        ending = ["X", "Y"]
        toy_cell = lattice[(0, 1)]
        assert list(toy_cell.site_states()) == starting
        transition_by_site = {
            (0, 1, 0): (starting[0], ending[0]),
        }
        # TODO
        possible_changes.update({
            "*_0": ["X"],
            "*_1": ["Y"],
            "X": ["*_0"],
            "Y": ["*_1"],
        })
    elif num_sites == 3:
        starting = ["O", "*_1", "CO"]
        ending = ["*_0", "CO", "CO"]
        toy_cell = lattice[(2, 1)]
        assert list(toy_cell.site_states()) == starting
        transition_by_site = {
            (2, 1, 0): (starting[0], ending[0]),
            (2, 1, 1): (starting[1], ending[1]),
        }
        # TODO
        possible_changes.update({
            "*_0": ["O"],
            "*_1": ["CO"],
            "*_2": ["CO"],
            "O": ["*_0"],
            "CO": ["*_1", "*_2"],
        })
    elif num_sites == 5:
        starting = ["*_0", "*_1", "CO2", "CO2", "*_4"]
        ending = ["CO", "CO", "*_2", "*_3", "O2"]
        toy_cell = lattice[(0, 1)]
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
        toy_cell = lattice[(0, 1)]
        assert list(toy_cell.site_states()) == starting
        transition_by_site = {(0, 1, index): (starting[index], ending[index])
            for index in range(num_sites)}
    # TODO - Need some form of rules for enabling processes...
    for starting_site, ending_site in zip(starting, ending):
        valid_site_change = ending_site in possible_changes[starting_site]
        assert (starting_site == ending_site) or valid_site_change

    sim_step = 1  # Whatever for now.
    current_usec = 7  # Whatever for now.
    process = data.process.Process(sim_step, transition_by_site,
        rate_constant=1)  # Whatever for now.
    process.generate_occurence_usec(current_usec)
    return process


def _populate_dummy_lattice(num_sites, axis_lengths=None, empty=False):
    def __update_lattice_cell(lattice, cell_coordinates, new_states):
        for index, state in enumerate(new_states):
            site_coordinates = cell_coordinates + (index,)
            step = 0
            lattice[site_coordinates].transition(step, state)

    lattice = data.lattice.Lattice(
        axis_lengths=axis_lengths, sites_per_cell=num_sites)
    if empty:
        return lattice

    if num_sites == 1:
        __update_lattice_cell(lattice, (0, 0), ["A"])
    elif num_sites == 2:
        __update_lattice_cell(lattice, (0, 0), ["X", "Y"])
        __update_lattice_cell(lattice, (0, 1), ["*_0", "Y"])
        __update_lattice_cell(lattice, (1, 0), ["X", "*_1"])
        # Empty (1, 1,)
    elif num_sites == 3:
        __update_lattice_cell(
            lattice, (0, 1), ["*_0", "CO", "*_2"])
        __update_lattice_cell(
            lattice, (0, 3), ["*_0", "CO", "*_2"])
        __update_lattice_cell(
            lattice, (1, 0), ["O", "*_1", "*_2"])
        __update_lattice_cell(
            lattice, (1, 1), ["O", "CO", "*_2"])
        __update_lattice_cell(
            lattice, (1, 2), ["*_0", "CO", "*_2"])
        __update_lattice_cell(
            lattice, (1, 3), ["O", "CO", "*_2"])
        for coords in [(2, 0), (2, 1)]:
            __update_lattice_cell(
                lattice, coords, ["O", "*_1", "CO"])
        __update_lattice_cell(
            lattice, (2, 2), ["O", "CO", "CO"])
        __update_lattice_cell(
            lattice, (2, 3), ["O", "CO", "*_2"])
        for coords in [(3, 0), (3, 1)]:
            __update_lattice_cell(
                lattice, coords, ["*_0", "*_1", "CO"])
        __update_lattice_cell(
            lattice, (3, 2), ["*_0", "CO", "CO"])
        __update_lattice_cell(
            lattice, (3, 3), ["O", "CO", "CO"])
    elif num_sites == 5:
        __update_lattice_cell(
            lattice, (0, 0), ["*_0", "*_1", "*_2", "*_3", "*_4"])
        __update_lattice_cell(
            lattice, (0, 1), ["*_0", "*_1", "CO2", "CO2", "*_4"])
        __update_lattice_cell(
            lattice, (0, 2), ["*_0", "*_1", "CO2", "CO2", "*_4"])
        __update_lattice_cell(
            lattice, (0, 3), ["*_0", "*_1", "CO2", "*_3", "*_4"])
        __update_lattice_cell(
            lattice, (1, 0), ["*_0", "*_1", "*_2", "CO2", "O2"])
        __update_lattice_cell(
            lattice, (1, 1), ["CO", "CO", "*_2", "*_3", "O2"])
        __update_lattice_cell(
            lattice, (1, 2), ["CO", "CO", "*_2", "*_3", "O2"])
        __update_lattice_cell(
            lattice, (1, 3), ["*_0", "CO", "CO2", "*_3", "O2"])
        __update_lattice_cell(
            lattice, (2, 0), ["*_0", "CO", "*_2", "CO2", "O2"])
        __update_lattice_cell(
            lattice, (2, 1), ["CO", "CO", "*_2", "*_3", "*_4"])
        __update_lattice_cell(
            lattice, (2, 2), ["*_0", "CO", "*_2", "*_3", "O2"])
        __update_lattice_cell(
            lattice, (2, 3), ["CO", "*_1", "*_2", "*_3", "O2"])
        __update_lattice_cell(
            lattice, (3, 0), ["CO", "*_1", "*_2", "*_3", "*_4"])
        __update_lattice_cell(
            lattice, (3, 1), ["*_0", "CO", "*_2", "*_3", "O2"])
        __update_lattice_cell(
            lattice, (3, 2), ["*_0", "*_1", "*_2", "*_3", "O2"])
        __update_lattice_cell(
            lattice, (3, 3), ["*_0", "*_1", "*_2", "*_3", "O2"])

    else:
        # Exists a dist of "allowed" occupants, dependpent on cell's state.
        example_site_states = ["<draw_allowable(cell, site_%d)>" % index
            for index in range(num_sites)]
        __update_lattice_cell(lattice, (0, 0), example_site_states)
    return lattice


def bgcolor_for_cell(cell):
    states = list(cell.site_states())
    assert len(states) <= K_MAX_TOY_DUMMY_SITES, "Likely undefined."
    if states == ["A"]:
        return "lightblue"
    elif len(states) == 2:
        if states == ["*_0", "Y"]:
            return "orange"
        if states == ["X", "*_1"]:
            return "yellow"
        if states == ["X", "Y"]:
            return "red"
    elif len(states) == 3:
        if states == ["*_0", "CO", "CO"]:
            return "salmon"
        if states == ["O", "*_1", "*_2"]:
            return "cyan"
        if (states == ["*_0", "CO", "*_2"] or
                states == ["*_0", "*_1", "CO"]):
            return "lightblue"
        if (states == ["O", "CO", "*_2"] or
                states == ["O", "*_1", "CO"]):
            return "orchid"
        if states == ["O", "CO", "CO"]:
            return "darkorchid"
    elif len(states) == 5:
        if states == ["*_0", "*_1", "CO2", "CO2", "*_4"]:
            return "crimson"
        if (states == ["*_0", "*_1", "*_2", "CO2", "*_4"] or
                states == ["*_0", "*_1", "CO2", "*_3", "*_4"]):
            return "salmon"
        if (states == ["*_0", "*_1", "CO2", "*_3", "O2"] or
                states == ["*_0", "*_1", "*_2", "CO2", "O2"]):
            return "yellow"
        if states == ["CO", "CO", "*_2", "*_3", "*_4"]:
            return "darkorange"
        if (states == ["*_0", "CO", "CO2", "*_3", "O2"] or
                states == ["*_0", "CO", "*_2", "CO2", "O2"] or
                states == ["CO", "*_1", "CO2", "*_3", "O2"] or
                states == ["CO", "*_1", "*_2", "CO2", "O2"]):
            return "sandybrown"
        if (states == ["CO", "*_1", "*_2", "*_3", "*_4"] or
                states == ["*_0", "CO", "*_2", "*_3", "*_4"]):
            return "orange"
        if states == ["CO", "CO", "*_2", "*_3", "O2"]:
            return "aquamarine"
        if (states == ["CO", "*_1", "*_2", "*_3", "O2"] or
                states == ["*_0", "CO", "*_2", "*_3", "O2"]):
            return "lightgreen"
        if states == ["*_0", "*_1", "*_2", "*_3", "O2"]:
            return "limegreen"

    return "white"


class PrintToysError(Exception):
    pass
