import proto.elementary_reaction_pb2


# Needs rate constants, everything is (last I checked) uniformly distributed.
def build_rxns_list():

    X_adsorption = proto.elementary_reaction_pb2.ElementaryReaction()
    X_adsorption.transitions.extend([
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="*_0", product="X", cell_coordinates=[0, 0], site_index=0)
    ])

    X_desorption = proto.elementary_reaction_pb2.ElementaryReaction()
    X_desorption.transitions.extend([
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="X", product="*_0", cell_coordinates=[0, 0], site_index=0)
    ])

    Y_adsorption = \
        proto.elementary_reaction_pb2.ElementaryReaction()
    Y_adsorption.transitions.extend([
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="*_1", product="Y", cell_coordinates=[0, 0], site_index=1)
    ])

    Y_desorption = \
        proto.elementary_reaction_pb2.ElementaryReaction()
    Y_desorption.transitions.extend([
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="Y", product="*_1", cell_coordinates=[0, 0], site_index=1)
    ])

    return [

        # O
        X_adsorption,
        X_desorption,

        # CO
        Y_adsorption,
        Y_desorption,
    ]
