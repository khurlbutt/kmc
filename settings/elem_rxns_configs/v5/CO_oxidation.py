import proto.elementary_reaction_pb2


# Needs rate constants, everything is (last I checked) uniformly distributed.
def build_rxns_list():

    oxygen_adsorption = proto.elementary_reaction_pb2.ElementaryReaction()
    oxygen_adsorption.transitions.extend([
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="*_0", product="O", cell_coordinates=[0, 0], site_index=0),
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="*_0", product="O", cell_coordinates=[1, 1], site_index=0)
    ])

    oxygen_desorption = proto.elementary_reaction_pb2.ElementaryReaction()
    oxygen_desorption.transitions.extend([
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="O", product="*_0", cell_coordinates=[0, 0], site_index=0),
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="O", product="*_0", cell_coordinates=[1, 1], site_index=0)
    ])

    carbon_monoxide_adsorption = \
        proto.elementary_reaction_pb2.ElementaryReaction()
    carbon_monoxide_adsorption.transitions.extend([
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="*_1", product="CO", cell_coordinates=[0, 0],
            site_index=1),
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="*_2", product="CO", cell_coordinates=[0, 0], site_index=2)
    ])

    carbon_monoxide_desorption = \
        proto.elementary_reaction_pb2.ElementaryReaction()
    carbon_monoxide_desorption.transitions.extend([
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="CO", product="*_1", cell_coordinates=[0, 0],
            site_index=1),
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="CO", product="*_2", cell_coordinates=[0, 0], site_index=2)
    ])

    carbon_dioxide_adsorption_a = \
        proto.elementary_reaction_pb2.ElementaryReaction()
    carbon_dioxide_adsorption_a.transitions.extend([
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="*_0", product="O", cell_coordinates=[0, 0],
            site_index=0),
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="*_1", product="CO", cell_coordinates=[1, 1],
            site_index=1),
    ])

    carbon_dioxide_adsorption_b = \
        proto.elementary_reaction_pb2.ElementaryReaction()
    carbon_dioxide_adsorption_b.transitions.extend([
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="*_0", product="O", cell_coordinates=[0, 0],
            site_index=0),
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="*_2", product="CO", cell_coordinates=[1, 1],
            site_index=2),
    ])

    carbon_dioxide_formation_a = \
        proto.elementary_reaction_pb2.ElementaryReaction()
    carbon_dioxide_formation_a.transitions.extend([
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="O", product="*_0", cell_coordinates=[0, 0], site_index=0),
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="CO", product="*_1", cell_coordinates=[1, 1], site_index=1)
    ])

    carbon_dioxide_formation_b = \
        proto.elementary_reaction_pb2.ElementaryReaction()
    carbon_dioxide_formation_b.transitions.extend([
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="O", product="*_0", cell_coordinates=[0, 0], site_index=0),
        proto.elementary_reaction_pb2.ElementaryReaction.Transition(
            reactant="CO", product="*_2", cell_coordinates=[1, 1], site_index=2)
    ])

    return [

        # O
        oxygen_adsorption,
        oxygen_desorption,

        # CO
        carbon_monoxide_adsorption,
        carbon_monoxide_adsorption,

        # CO2
        carbon_dioxide_adsorption_a,
        carbon_dioxide_adsorption_b,
        carbon_dioxide_formation_a,
        carbon_dioxide_formation_b,
    ]
