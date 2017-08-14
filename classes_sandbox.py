import itertools


class Lattice(object):

    def __init__(self, length=2, width=2):
        self.length = length
        self.width = width
        self.cells = [[Cell(row, col) for col in range(self.width)]
            for row in range(self.length)]

    def enumerate_cells(self):
        # Example of a generator-iterator as described by PEP 255.
        # Intro to generators as "lazy evaluation" or "calculation on demand":
        #     http://intermediatepythonista.com/python-generators
        for row in range(self.length):
            for col in range(self.width):
                yield self.cells[row][col]

    def num_occupied(self):
        num_occupied = 0
        for cell in self.enumerate_cells():
            if cell.is_occupied():
                num_occupied += 1
        return num_occupied

    def __repr__(self):
        species = set()
        for cell in self.enumerate_cells():
            if cell.adsorbate:
                species.add(cell.adsorbate)
        return "(%d,%d)[%d occupied]{%d species: %r}" % (
            self.length, self.width, self.num_occupied(), len(species), species)

class Cell(object):

    def __init__(self, row, col, adsorbate=None):
        self.row = row
        self.col = col
        self.adsorbate = adsorbate

    def is_occupied(self):
        return bool(self.adsorbate)

    def __repr__(self):
        return "(%d,%d)[%r]" % (self.row, self.col, self.adsorbate)


class Process(object):

    def __init__(self):
        pass




class EnabledCollection(object):

    def __init__(self):
        pass

def main():
    lattice = Lattice(length=2, width=2)
    lattice.cells[0][0].adsorbate = "A"
    print("Lattice: %r" % lattice)
    for cell in lattice.enumerate_cells():
        print(cell)


if __name__ == '__main__':
    main()