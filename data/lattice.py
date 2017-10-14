import base64
import data.cell
import data.site
import itertools
import proto.lattice_pb2 as proto_lattice


class Lattice(object):

    def __init__(self, *, axis_lengths=None, sites_per_cell=None):
        axis_lengths = tuple(axis_lengths) if axis_lengths else (10, 10)
        sites_per_cell = sites_per_cell or 1

        self.sites_per_cell = sites_per_cell
        self.coordinate_cardinalities = axis_lengths + (sites_per_cell,)
        coord_sets = [list(range(cc)) for cc in self.coordinate_cardinalities]
        # Default to (x, y, s) here. But (r, theta, z) is equally chill.
        coord_points = list(itertools.product(*coord_sets))

        empty_sites = [
            data.site.Site(coordinates=coords, state="*_%d" % coords[-1])
            for coords in coord_points
        ]
        self._sites = self.set_sites(empty_sites)

        # Ends up storing all the site bookkeeping twice... here and on cells.
        self._cells = self.set_cells()

    def set_sites(self, sites):
        self._sites = {site.coordinates: site for site in sites}
        return self._sites

    def iter_sites(self):
        # Example of a generator-iterator as described by PEP 255.
        # Intro to generators as "lazy evaluation" or "calculation on demand":
        #   http://intermediatepythonista.com/python-generators
        if self._sites:
            for site_coordinates in sorted(self._sites):
                yield self._sites[site_coordinates]

    # Ends up storing all the site bookkeeping twice.
    def set_cells(self):
        cells_coordinates = set()
        for site in self.iter_sites():
            cells_coordinates.add(site.coordinates[:-1])
        cells = [data.cell.Cell(self, cell_coordinates)
            for cell_coordinates in cells_coordinates]
        self._cells = {cell.coordinates: cell for cell in cells}
        return self._cells

    def iter_cells(self):
        if self._cells:
            for cell_coordinates in sorted(self._cells):
                yield self._cells[cell_coordinates]

    def __getitem__(self, key):
        if not isinstance(key, tuple):
            raise TypeError
        site_coordinate_length = len(self.coordinate_cardinalities)
        cell_coordinate_length = site_coordinate_length - 1
        if (len(key) != site_coordinate_length and
                len(key) != cell_coordinate_length):
            raise IndexError(key)
        normalized_key = self._normalize_coordinates(key)
        if self._sites and len(normalized_key) == site_coordinate_length:
            return self._sites[normalized_key]
        elif self._cells and len(normalized_key) == cell_coordinate_length:
            return self._cells[normalized_key]
        else:
            raise IndexError(key)

    def _normalize_coordinates(self, coordinates):
        # TODO make sure we're following periodic boundary condition rules
        normalized_coordinates = []
        for index, coordinate in enumerate(coordinates):
            cardinality = self.coordinate_cardinalities[index]
            # No 'wrap-around' for site indices, raise IndexError instead.
            is_site_index = bool(index == len(coordinates) - 1)
            # Never reach yourself(?)
            if abs(coordinate) >= cardinality * 1.5:
                raise IndexError(coordinates)
            if coordinate < 0:
                if is_site_index:
                    raise IndexError(coordinates)
                normalized = cardinality - abs(coordinate)
            elif coordinate > (cardinality - 1):
                if is_site_index:
                    raise IndexError(coordinates)
                normalized = coordinate - cardinality
            else:
                normalized = coordinate
            normalized_coordinates.append(normalized)
        return tuple(normalized_coordinates)

    def __repr__(self):
        species_counts = {}
        for site in self.iter_sites():
            species_counts[site.state] = species_counts.get(site.state, 0) + 1
        # TODO: Okay to assume empty sites are occupied by a hole of some kind?
        total_count = sum([count for species, count in species_counts.items()])
        dist = {}
        for species, count in species_counts.items():
            dist[species] = count / total_count
        sorted_distribution = [(s, "%.2f" % p) for s, p in sorted(
            dist.items(), key=lambda item: item[1], reverse=True)]
        return "(%r){%r unique species: %r}" % (
            "x".join([str(c) for c in self.coordinate_cardinalities]),
            len(species_counts), sorted_distribution)


# Protocol Buffers (proto or pb) are for the display server.
def to_proto(lattice):
    pb = proto_lattice.Lattice()
    pb.axis_lengths.extend(list(lattice.coordinate_cardinalities[:-1]))
    pb.sites_per_cell = lattice.sites_per_cell
    pb.sites.extend([data.site.to_proto(site) for site in lattice.iter_sites()])
    return pb


# Protocol Buffers (proto or pb) are for the display server.
def from_proto(pb):
    lattice = Lattice(axis_lengths=list(pb.axis_lengths),
        sites_per_cell=pb.sites_per_cell)
    sites = []
    for site_pb in pb.sites:
        sites.append(data.site.from_proto(site_pb))
    lattice.set_sites(sites)
    lattice.set_cells()
    return lattice


# Protocol Buffers (proto or pb) are for the display server.
def to_proto_b64str(lattice):
    # Serialized bytes as a utf-8 encoded str.
    return base64.b64encode(to_proto(lattice).SerializeToString())


# Protocol Buffers (proto or pb) are for the display server.
def from_proto_b64str(proto_b64str):
    try:
        import binascii
        proto_str = base64.b64decode(proto_b64str)
    except binascii.Error as e:
        raise Exception("Not a valid base64-encoded protobuf.")
    try:
        pb = proto_lattice.Lattice.FromString(proto_str)
    except TypeError as e:
        raise Exception("Not a valid base64-encoded protobuf.")
    return from_proto(pb)
