import base64
import proto.site_pb2 as proto_site


class Site(object):

    def __init__(self, *, coordinates=None, state=None, last_update_step=None):
        assert coordinates
        assert isinstance(state, str) and state  # "*_0", "A", "CO", "O2", etc.

        # eg (x, y, s) or (r, theta, s) or something else, up to YOU!
        self.coordinates = tuple(coordinates)
        self.state = state
        # TODO gets updated now, but should we show in __repr__?
        self.last_update_step = last_update_step or 0

    def transition(self, step, state):
        self.last_update_step = step
        self.state = state

    def __repr__(self):
        return "@%r%s" % (self.coordinates, self.state)


# Protocol Buffers (proto or pb) are for the display server.
def to_proto(site):
    pb = proto_site.Site()
    pb.coordinates.extend(list(site.coordinates))
    pb.state = site.state
    pb.last_update_step = site.last_update_step
    return pb


# Protocol Buffers (proto or pb) are for the display server.
def from_proto(pb):
    site = Site(coordinates=list(pb.coordinates), state=pb.state,
        last_update_step=pb.last_update_step)
    return site


# Protocol Buffers (proto or pb) are for the display server.
def to_proto_b64str(site):
    # Serialized bytes as a utf-8 encoded str.
    return base64.b64encode(to_proto(site).SerializeToString())


# Protocol Buffers (proto or pb) are for the display server.
def from_proto_b64str(proto_b64str):
    try:
        import binascii
        # Serialized bytes as a utf-8 encoded str.
        proto_str = base64.b64decode(proto_b64str)
    except binascii.Error as e:
        raise Exception("Not a valid base64-encoded protobuf.")
    try:
        pb = proto_site.Site.FromString(proto_str)
    except TypeError as e:
        raise Exception("Not a valid base64-encoded protobuf.")
    return from_proto(pb)
