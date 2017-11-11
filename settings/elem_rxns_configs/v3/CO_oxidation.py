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
#    note: sites is a tuple, since potentially more than one site can do change.
#          what's meant below is XOR, a case of AND should be distinct entries.
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

# SEE BELOW COMMENT
carbon_monoxide_adsorption = {
    "name": "carbon monoxide adsorption",
    "rate_constant": 1e9,
    "changes": {
        (0, 0): {(1, 2): ("*", "CO")}
    }
}

# SEE BELOW COMMENT
carbon_monoxide_desorption = {
    "name": "carbon monoxide desorption",
    "rate_constant": 1e8,
    "changes": {
        (0, 0): {(1, 2): ("CO", "*")}
    }
}

# SEE BELOW COMMENT
carbon_dioxide_formation = {
    "name": "carbon dioxide formation",
    "rate_constant": 1e3,
    "changes": {
        (0, 0): {(0, ): ("O", "*")},
        (1, 1): {(1, 2): ("CO", "*")}
    }
}

# At (1, 1) what we mean is XOR.
# There could be a case where AND is required,
# but arguably such a case should be two distinct entries in "sites".
carbon_dioxide_adsorption = {
    "name": "carbon dioxide adsorption",
    "rate_constant": 1e-2,
    "changes": {
        (0, 0): {(0, ): ("*", "O")},
        (1, 1): {(1, 2): ("*", "CO")}
    }
}

carbon_dioxide_adsorption = {
    "name": "carbon dioxide adsorption",
    "rate_constant": 1e-2,
    "transitions": {
        [str R1, str P1, int h1, int j1, int s1],
        [str R2, str P2, int h2, int j2, int s2],
        eg
        ["*", "CO", 0, 0, 0]
    }
}

"*_br + *_hol -> CO*_br + O*_hol"

carbon_dioxide_adsorption = {
    "name": "carbon dioxide adsorption",
    "rate_constant": 1e-2,
    "transitions": {
        ["*", "O", 0, 0, 0],
        ["*", "CO", 1, 1, 1]
    }
}

carbon_dioxide_adsorption = {
    "name": "carbon dioxide adsorption",
    "rate_constant": 1e-2,
    "transitions": [
        ["*", "O", 0, 0, 0],
        ["*", "CO", 1, 1, 2]
    ]
}


ELEMENTARY_RXNS = []
for thing in thingy:
    ELEMENTARY_RXNS.append(build_elems_for(thing))

def find_processes(self, site):
    adsorbate = site.occupation
    processes_to_add = []
    incident_cell_real_coordinates = site.coordinates #eg (54,93,1)
    #incident_site_def_coordinates = ... (eg (1,1,1))
    for elem_rxn in self.ELEMENTARY_RXNS:
        for possible_launching_point in elem_rxn["transition"]:
            if adsorbate == possible_launching_point[0]:
                incident_cell_coordinates = (possible_launching_point[2], possible_launching_point[3])
                add_flag = True
                for transition in elem_rxn["transitions"]:
                    cell_coordinates = (transition[2], transition[3])
                    
                    magic_cell_coordinates = incident_cell_real_coordinates + (cell_coordinates - incident_coordinates)
                    
                    magic_coordinates = (magic_cell_coordinates[0], magic_cell_coordinates[1], transition[4])
                    if self.lattice[MAGIC_COORDINATES] != transition[0]:
                        add_flag = False
                        break
                    RETAIN SOME INFORMATION ABOUT MAGIC_COORDINATES FOR PROCESS ADDITION
                if add_flag:
                    processes_to_add.append(Process(...))
    for p in processes_to_add:
        self.enabled_process.add(p)


ELEMENTARY_RXNS = [
    oxygen_adsorption,
    oxygen_desorption,
    carbon_monoxide_adsorption,
    carbon_monoxide_desorption,
    carbon_dioxide_formation,
    carbon_dioxide_adsorption
]
