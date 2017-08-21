from classes_sandbox import Lattice as Lattice
from classes_sandbox import Process as Process
from classes_sandbox import Simulation as Simulation

K_MAX_TOY_DUMMY_SITES = 5


def lattice_examples():
    for num_sites in range(1, K_MAX_TOY_DUMMY_SITES + 1):
        print("\n\n%d site(s) per cell:" %
            num_sites)
        lattice = _populate_dummy_lattice(num_sites)
        print("Lattice: %r" % lattice)
        for cell in lattice.enumerate_cells():
            print(cell)


def process_examples():
    for num_sites in range(1, K_MAX_TOY_DUMMY_SITES + 1):
        lattice = _populate_dummy_lattice(num_sites)
        process = None
        if num_sites == 1:
            remove = _populate_dummy_process(lattice, num_sites)
            process = remove
            print("\n\n%d site(s) per cell: Removal of A" % num_sites)
        if num_sites == 2:
            remove = _populate_dummy_process(lattice, num_sites)
            process = remove
            print("\n\n%d site(s) per cell: Introduce O2 of A" % num_sites)
        if num_sites == 3:
            remove = _populate_dummy_process(lattice, num_sites)
            process = remove
            print("\n\n%d site(s) per cell: Bridge,Bridge,Hollow_(X,Y,Z)" %
                num_sites)
        if num_sites == 4:
            clear_random = _populate_dummy_process(lattice, num_sites)
            process = clear_random
            print("\n\n%d site(s) per cell: ClearRandom" % num_sites)
        if num_sites == 5:
            breakdown = _populate_dummy_process(lattice, num_sites)
            process = breakdown
            print("\n\n%d site(s) per cell: Breakdown of CO2" % num_sites)
        if process:
            print("before...")
            print("\tLattice:\n\t%r" % lattice)
            print("\tProcess:\n\t%r" % process)
            print(process.cell)
            process.perform()
            print("\nafter...")
            print("\tLattice:\n\t%r" % lattice)
            print("\tProcess:\n\t%r" % process)
            print(process.cell)


def simulation_examples():
    simulation = Simulation()
    print("\n\n%r" % simulation)


def _populate_dummy_process(lattice, num_sites):
    possible_changes = {}
    if num_sites == 1:
        starting_sites = ["A"]
        ending_sites = ["*_0"]
        toy_cell = lattice.cells[0][0]
        assert toy_cell.sites == starting_sites
        possible_changes.update({
            "*_0": ["A"],
            "A": ["*_0"],
        })
    elif num_sites == 2:
        starting_sites = ["*_0", "CO"]
        ending_sites = ["O2", "CO"]
        toy_cell = lattice.cells[0][1]
        assert toy_cell.sites == starting_sites
        possible_changes.update({
            "*_0": ["O2"],
            "*_1": ["CO"],
            "O2": ["*_0"],
            "CO": ["*_1"],
        })
    elif num_sites == 3:
        starting_sites = ["X_bridge", "*_1", "Z_hollow"]
        ending_sites = ["*_0", "Y_bridge", "Z_hollow"]
        toy_cell = lattice.cells[1][0]
        assert toy_cell.sites == starting_sites
        possible_changes.update({
            "*_0": ["X_bridge"],
            "*_1": ["Y_bridge"],
            "*_2": ["Z_hollow"],
            "X_bridge": ["*_0"],
            "Y_bridge": ["*_1"],
            "Z_hollow": ["*_2"],
        })
    elif num_sites == 5:
        starting_sites = ["*_0", "*_1", "CO2", "CO2", "*_4"]
        ending_sites = ["CO", "CO", "*_2", "*_3", "O2"]
        toy_cell = lattice.cells[0][1]
        assert toy_cell.sites == starting_sites
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
        starting_sites = []
        ending_sites = []
        for index in range(num_sites):
            hole_for_index = "*_%d" % index
            species = "<draw_allowable(cell, site_%d)>" % index
            possible_changes[species] = hole_for_index
            possible_changes[hole_for_index] = species
            starting_sites.append(hole_for_index)
            ending_sites.append(species)
        toy_cell = lattice.cells[0][0]
        assert toy_cell.sites == starting_sites
    for starting_site, ending_site in zip(starting_sites, ending_sites):
        assert ending_site in possible_changes[starting_site]

    def is_enabled_still_fn(cell):
        # TODO: Quite naive, need to check whether sites have updated since time
        #       when process became enabled.
        if len(cell.sites) in range(K_MAX_TOY_DUMMY_SITES + 1):
            # Type tuple is immuatable; create a copy.
            if tuple(cell.sites) == tuple(starting_sites):
                return True
        else:
            assert False, "No possible case to return True."
        return False

    def perform_fn(cell):
        # TODO: Quite naive, need to update site update times to avoid
        #       performing expired processes at a later point.
        # Type list is mutable, but this creates a copy for us... maybe too much
        cell.sites = list(ending_sites)

    sim_time = 10  # Whatever for now.
    return Process(sim_time, toy_cell, is_enabled_still_fn, perform_fn)


def _populate_dummy_lattice(num_sites):
    lattice = Lattice(length=2, width=2, num_sites=num_sites)
    if num_sites == 1:
        lattice.cells[0][0].sites = ["A"]
    elif num_sites == 2:
        lattice.cells[0][0].sites = ["O2", "CO"]
        lattice.cells[0][1].sites = ["*_0", "CO"]
        lattice.cells[1][0].sites = ["O2", "*_1"]
    elif num_sites == 3:
        lattice.cells[0][0].sites = ["X_bridge", "Y_bridge", "*_2"]
        lattice.cells[0][1].sites = ["*_0", "*_1", "Z_hollow"]
        lattice.cells[1][0].sites = ["X_bridge", "*_1", "Z_hollow"]
        lattice.cells[1][1].sites = ["*_0", "Y_bridge", "Z_hollow"]
    elif num_sites == 5:
        lattice.cells[0][0].sites = ["*_0", "*_1", "*_2", "*_3", "*_4"]
        lattice.cells[0][1].sites = ["*_0", "*_1", "CO2", "CO2", "*_4"]
        lattice.cells[1][0].sites = ["CO", "CO", "*_2", "*_3", "O2"]
        lattice.cells[1][1].sites = ["CO", "CO", "*_2", "*_3", "O2"]

    else:
        # Exists a dist of "allowed" occupants, dependpent on cell's state.
        example_sites = ["<draw_allowable(cell, site_%d)>" % index
            for index in range(num_sites)]
        lattice.cells[0][1].sites = example_sites
        lattice.cells[1][1].sites = example_sites
    return lattice
