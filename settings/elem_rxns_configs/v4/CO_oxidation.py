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

oxygen_adsorption = {
    "name": "oxygen adsorption",
    "rate_constant": 1e10,
    "changes": {
        (0, 0): {(0, ): ("*", "O")},
        (1, 1): {(0, ): ("*", "O")}
    }
}

oxygen_desorption = {
    "name": "oxygen desorption",
    "rate_constant": 1e5,
    "changes": {
        (0, 0): {(0, ): ("O", "*")},
        (1, 1): {(0, ): ("O", "*")}
    }
}

carbon_monoxide_adsorption = {
    "name": "carbon monoxide adsorption",
    "rate_constant": 1e9,
    "changes": {
        (0, 0): {(1, 2): ("*", "CO")}
    }
}

carbon_monoxide_desorption = {
    "name": "carbon monoxide desorption",
    "rate_constant": 1e8,
    "changes": {
        (0, 0): {(1, 2): ("CO", "*")}
    }
}

carbon_dioxide_formation = {
    "name": "carbon dioxide formation",
    "rate_constant": 1e3,
    "changes": {
        (0, 0): {(0, ): ("O", "*")},
        (1, 1): {(1, 2): ("CO", "*")}
    }
}

carbon_dioxide_adsorption = {
    "name": "carbon dioxide adsorption",
    "rate_constant": 1e-2,
    "changes": {
        (0, 0): {(0, ): ("*", "O")},
        (1, 1): {(1, 2): ("*", "CO")}
    }
}

ELEMENTARY_RXNS = [
    oxygen_adsorption,
    oxygen_desorption,
    carbon_monoxide_adsorption,
    carbon_monoxide_desorption,
    carbon_dioxide_formation,
    carbon_dioxide_adsorption
]
