
# Protocol Buffers (proto or pb) are for the display server. Here we define what
# will be sent from server to client in regards to the data model.

import base64
# import data.cell
# import data.elementary_reaction
# import data.enabled_collection
import data.lattice
import data.simulation
import data.site
# import proto.cell_pb2
# import proto.elementary_reaction_pb2
# import proto.enabled_collection_pb2
import proto.lattice_pb2
import proto.simulation_pb2
import proto.site_pb2


class BaseProto(object):
    # An instance of this class should define these functions, examples below.

    def to_proto(data_model_object):
        raise NotImplementedError()

    def from_proto(pb):
        raise NotImplementedError()

    # TODO: Remove nearly duplicated code?
    def to_proto_b64str(data_model_object):
        raise NotImplementedError()

    # TODO: Remove nearly duplicated code?
    def from_proto_b64str(proto_b64str):
        raise NotImplementedError()


class Cell(BaseProto):
    pass


class ElementaryReaction(BaseProto):
    pass


class EnabledCollection(BaseProto):
    pass


class Lattice(BaseProto):
    def to_proto(lattice):
        pb = proto.lattice_pb2.Lattice()
        pb.axis_lengths.extend(list(lattice.coordinate_cardinalities[:-1]))
        pb.sites_per_cell = lattice.sites_per_cell
        pb.sites.extend([data.proto_convert.Site.to_proto(site)
            for site in lattice.iter_sites()
        ])
        return pb

    def from_proto(pb):
        lattice = data.lattice.Lattice(axis_lengths=list(pb.axis_lengths),
            sites_per_cell=pb.sites_per_cell)
        sites = []
        for site_pb in pb.sites:
            sites.append(data.proto_convert.Site.from_proto(site_pb))
        lattice.set_sites(sites)
        lattice.set_cells()
        return lattice

    def to_proto_b64str(lattice):
        # Serialized bytes as a utf-8 encoded str.
        pb = data.proto_convert.Lattice.to_proto(lattice)
        return base64.b64encode(pb.SerializeToString())

    def from_proto_b64str(proto_b64str):
        try:
            import binascii
            proto_str = base64.b64decode(proto_b64str)
        except binascii.Error as e:
            raise Exception("Not a valid base64-encoded protobuf.")
        try:
            pb = proto.lattice_pb2.Lattice.FromString(proto_str)
        except TypeError as e:
            raise Exception("Not a valid base64-encoded protobuf.")
        return data.proto_convert.Lattice.from_proto(pb)


class Process(BaseProto):
    pass


class Simulation(BaseProto):

    def to_proto(simulation):
        lattice_pb = data.proto_convert.Lattice.to_proto(simulation.lattice)
        pb = proto.simulation_pb2.Simulation(lattice=lattice_pb)
        pb.stop_time = simulation.STOP_TIME
        pb.stop_step = simulation.STOP_STEP
        pb.time_usec = simulation.time_usec
        pb.step = simulation.step
        # TODO: This would allow data.simulation.update_process_queue to be
        #       called without from_scrath=True.
        # pb.enabled_collection = (
        #     data.enabled_collection.to_proto(simulation.process_queue))
        # pg.elementary_reaction = (
        #     data.elementary_reaction.to_proto(simulation.ELEM_RXNS))
        return pb

    def from_proto(pb):
        simulation = data.simulation.Simulation(stop_step=pb.stop_step,
            lattice=pb.lattice)
        simulation.STOP_TIME = pb.stop_time
        simulation.STOP_STEP = pb.stop_step
        simulation.time_usec = pb.time_usec
        simulation.step = pb.step
        simulation.lattice = data.proto_convert.Lattice.from_proto(pb.lattice)
        # TODO: No huge rush here b/c can start from scratch.
        # simulation.enabled_collection = pb.process_queue
        # simulation.ELEM_RXNS = pb.elem_rxns
        return simulation

    def to_proto_b64str(simulation):
        # Serialized bytes as a utf-8 encoded str.
        pb = data.proto_convert.Simulation.to_proto(simulation)
        return base64.b64encode(pb.SerializeToString())

    def from_proto_b64str(proto_b64str):
        try:
            import binascii
            proto_str = base64.b64decode(proto_b64str)
        except binascii.Error as e:
            raise Exception("Not a valid base64-encoded protobuf.")
        try:
            pb = proto.simulation_pb2.Simulation.FromString(proto_str)
        except TypeError as e:
            raise Exception("Not a valid base64-encoded protobuf.")
        return data.proto_convert.Simulation.from_proto(pb)


class Site(BaseProto):

    def to_proto(site):
        pb = proto.site_pb2.Site()
        pb.coordinates.extend(list(site.coordinates))
        pb.state = site.state
        pb.last_update_step = site.last_update_step
        return pb

    def from_proto(pb):
        site = data.site.Site(coordinates=list(pb.coordinates), state=pb.state,
            last_update_step=pb.last_update_step)
        return site

    def to_proto_b64str(site):
        # Serialized bytes as a utf-8 encoded str.
        pb = data.proto_convert.Site.to_proto(site)
        return base64.b64encode(pb.SerializeToString())

    def from_proto_b64str(proto_b64str):
        try:
            import binascii
            # Serialized bytes as a utf-8 encoded str.
            proto_str = base64.b64decode(proto_b64str)
        except binascii.Error as e:
            raise Exception("Not a valid base64-encoded protobuf.")
        try:
            pb = proto.site_pb2.Site.FromString(proto_str)
        except TypeError as e:
            raise Exception("Not a valid base64-encoded protobuf.")
        return data.proto_convert.Site.from_proto(pb)
