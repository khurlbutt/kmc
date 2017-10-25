"""
File: elementary_reaction.py
----------------------------
This class defines an elementary step for a chemical reaction catalyzed on a
metal surface.
"""


class ElementaryStep():
    """docstring for ElementaryStep"""
    def __init__(self, name=None, k=1.0, E=None, definition=None):
        self.name = name or "elem rxn"
        self.k = k
        self.E = E
        self.definition = definition

    def justify_definition(self):
        min_x = float("inf")
        min_y = float("inf")
        for key in self.definition:
            x = key[0]
            if x < min_x:
                min_x = x
            y = key[1]
            if y < min_y:
                min_y = y
        justified_def = {}
        for key in spec:
            x = key[0]
            y = key[1]
            justified_def[(x - min_x, y - min_y, s)] = spec[key]
        self.definition = justified_def

    def create_rotated_elem_rxns(self):
        rot_90 = {}
        rot_180 = {}
        rot_270 = {}
        for key in spec:
            x = key[0]
            y = key[1]
            rot_90[(y, -x)] = spec[key]
            rot_180[(-y, -x)] = spec[key]
            rot_270[(-y, x)] = spec[key]
        return [
            ElementaryStep(self.name, self.k, self.E, rot_90),
            ElementaryStep(self.name, self.k, self.E, rot_180),
            ElementaryStep(self.name, self.k, self.E, rot_270)
        ]

    def arrhenius(self, dE, prefactor=1e13):
        pass


# Protocol Buffers (proto or pb) are for the display server.
def to_proto(elem_rxn):
    raise NotImplementedError()


# Protocol Buffers (proto or pb) are for the display server.
def from_proto(pb):
    raise NotImplementedError()


# Protocol Buffers (proto or pb) are for the display server.
def to_proto_b64str(elem_rxn):
    raise NotImplementedError()


# Protocol Buffers (proto or pb) are for the display server.
def from_proto_b64str(proto_b64str):
    raise NotImplementedError()
