# elem_rxns_config V3

# A version of the elementary reactions'
# config, as inputted by the user.

# V3 fields
# name: string
# rate_constant: numerical, int for now... maybe float
# changes: dict, mapping of cell to sites changes on that cell
#    note: holes are explicitly indexed by "sites"
#    eg  {cell: {sites: (before, after)}
#        {(0, 0): {(0,): ("*", "A")}}
#    note: sites is a tuple, since potentially more than one site can do change
#    eg  {(0, 0): {(0, 1): ("CO", "*")}}

adsorption = {
    "name": "toy adsorption",
    "rate_constant": 1e10,
    "changes": {
        (0, 0): ("*", "A"),
    }
}

desorption = {
    "name": "toy desorption",
    "rate_constant": 1e10,
    "changes": {
        (0, 0): ("A", "*"),
    }
}

ELEMENTARY_RXNS = [
    adsorption,
    desorption
]

def justify_elem_rxn_spec(spec):
    min_x = float("inf")
    min_y = float("inf")
    for key in spec:
        x = key[0]
        if x<min_x:
            min_x = x
        y = key[1]
        if y<min_y:
            min_y = y
    adjusted_spec = {}
    for key in spec:
        x = key[0]
        y = key[1]
        adjusted_spec[(x-min_x, y-min_y)] = spec[key]
    return adjusted_spec

def generate_rotated_specs(spec):
    rot_90 = {}
    rot_180 = {}
    rot_270 = {}
    for key in spec:
        x = key[0]
        y = key[1]
        rot_90[(y, -x)] = spec[key]
        rot_180[(-y, -x)] = spec[key]
        rot_270[(-y, x)] = spec[key]
    return [rot_90, rot_180, rot_270]

def build_rxns_list():
    result = []
    for rxn in ELEMENTARY_RXNS:
        justified = {}
        for key in rxn:
            justified[key] = rxn[key]
        justified["changes"] = justify_elem_rxn_spec(justified["changes"])
        result.append(justified)
        rot_90=rot_180=rot_270 = {}
        for key in justified:
            rot_90[key]=rot_180[key]=rot_270[key] = justified[key]
        rotated = generate_rotated_specs(justified["changes"])
        rot_90 = rotated[0]
        result.append(rot_90)
        rot_180 = rotated[1]
        result.append(rot_180)
        rot_270 = rotated[2]
        result.append(rot_270)
    return result

