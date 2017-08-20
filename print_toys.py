from classes_sandbox import Lattice as Lattice
from classes_sandbox import Process as Process
from classes_sandbox import Simulation as Simulation

K_MAX_TOY_DUMMY_SITES = 6


def lattice_examples():
    for num_sites in range(1, K_MAX_TOY_DUMMY_SITES):
        print("\n\n%d site(s) per cell:" %
            num_sites)
        lattice = _populate_dummy_lattice(num_sites)
        print("Lattice: %r" % lattice)
        for cell in lattice.enumerate_cells():
            print(cell)


def process_examples():
    for num_sites in range(1, K_MAX_TOY_DUMMY_SITES):
        lattice = _populate_dummy_lattice(num_sites)
        process = None
        if num_sites == 1:
            def _still_allowed_fn(cell):
                return cell.get_adsorbates() == ["A"]

            def _perform_fn(cell):
                cell.sites = ["*_0"]
            sim_time = 10  # Whatever
            toy_cell = lattice.cells[0][0]
            remove = Process(sim_time, toy_cell, _still_allowed_fn, _perform_fn)
            process = remove
            print("\n\nREMOVAL: %d site(s) per cell" % num_sites)
        if num_sites == 5:
            def _still_allowed_fn(cell):
                # We could check individual site or use patterns etc.
                # return bool(
                #     cell.sites[0] == "*_0" and
                #     cell.sites[1] == "*_1" and
                #     cell.sites[2] == "CO2" and
                #     cell.sites[3] == "CO2" and
                #     cell.sites[4] == "*_4")
                return cell.sites == ["*_0", "*_1", "CO2", "CO2", "*_4"]

            def _perform_fn(cell):
                cell.sites = ["CO", "CO", "*_2", "*_4", "O2"]
            toy_cell = lattice.cells[0][0]
            toy_cell.sites = ["*_0", "*_1", "CO2", "CO2", "*_4"]
            sim_time = 10  # Whatever
            breakdown = Process(
                sim_time, toy_cell, _still_allowed_fn, _perform_fn)
            process = breakdown
            print("\n\nBREAKDOWN: %d site(s) per cell" % num_sites)
        if process:
            print("before")
            print("Lattice:%r" % lattice)
            print("Process:%r" % process)
            print(process.cell)
            process.perform()
            print("after")
            print("Lattice:%r" % lattice)
            print("Process:%r" % process)
            print(process.cell)


def simulation_examples():
    simulation = Simulation()
    print("\n\n%r" % simulation)


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
        lattice.cells[1][0].sites = ["CO", "CO", "*_2", "*_4", "O2"]
        lattice.cells[1][1].sites = ["CO", "CO", "*_2", "*_4", "O2"]

    else:
        # Exists a dist of "allowed" occupants, dependpent on cell's state.
        example_sites = ["<draw_allowable(cell, site_%d)>" % index
            for index in range(num_sites)]
        lattice.cells[0][0].sites = example_sites
    return lattice
