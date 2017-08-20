from classes_sandbox import Lattice as Lattice
from classes_sandbox import Process as Process


def lattice_examples():
    for num_sites in range(1, 5):
        print("\n\n%d site(s) per cell:" %
            num_sites)
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
        else:
            # Exists a dist of "allowed" occupants, dependpent on cell's state.
            example_sites = ["<draw_allowable(cell, site_%d)>" % index
                for index in range(num_sites)]
            lattice.cells[0][0].sites = example_sites

        print("Lattice: %r" % lattice)
        for cell in lattice.enumerate_cells():
            print(cell)


def process_examples():
    for num_sites in range(1, 6):
        lattice = Lattice(length=2, width=2, num_sites=num_sites)
        process = None
        if num_sites == 1:
            def _still_allowed_fn(cell):
                return cell.get_adsorbates() == ["A"]

            def _perform_fn(cell):
                cell.sites = ["*_0"]
            cell = lattice.cells[0][0]
            cell.sites = ["A"]
            sim_time = 10  # Whatever
            remove = Process(sim_time, cell, _still_allowed_fn, _perform_fn)
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
            cell = lattice.cells[0][0]
            cell.sites = ["*_0", "*_1", "CO2", "CO2", "*_4"]
            sim_time = 10  # Whatever
            breakdown = Process(sim_time, cell, _still_allowed_fn, _perform_fn)
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
