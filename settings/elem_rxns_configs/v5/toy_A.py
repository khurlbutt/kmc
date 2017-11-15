import proto.elementary_reaction_pb2


def build_rxns_list():
    adsorption = proto.elementary_reaction_pb2.ElementaryReaction()
    adsorption.transitions.extend([
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="*_0", product="A", cell_coordinates=[0, 0], site_index=0),
    ])
    desorption = proto.elementary_reaction_pb2.ElementaryReaction()
    desorption.transitions.extend([
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="A", product="*_0", cell_coordinates=[0, 0], site_index=0)
    ])
    return [
        adsorption,
        desorption
    ]
