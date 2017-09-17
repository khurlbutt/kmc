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
        (0, 0): {(0, ): ("*", "A")},
    }
}

desorption = {
    "name": "toy desorption",
    "rate_constant": 1e10,
    "changes": {
        (0, 0): {(0, ): ("A", "*")},
    }
}

ELEMENTARY_RXNS = [
    adsorption,
    desorption
]
