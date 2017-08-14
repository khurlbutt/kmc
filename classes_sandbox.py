import itertools


class Lattice(object):

    def __init__(self, width=2, length=2):
        self.width = width
        self.length = length
        self.cells = [[Cell(i, j) for i in range(self.width)]
            for j in range(self.length)]

class Cell(object):

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return "(%d,%d)" % (self.row, self.col)


class Process(object):

    def __init__(self):
        pass




class EnabledCollection(object):

    def __init__(self):
        pass

def main():
    lattice = Lattice(width=2, length=2)
    print("Lattice: length=%s, width=%s" % (lattice.length, lattice.width))
    print("first cell: %r" % lattice.cells[0][0])


if __name__ == '__main__':
    main()