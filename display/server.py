import data.lattice
import data.proto_convert
import print_toys
import tornado.ioloop
import tornado.web
import os.path

from urllib.parse import urljoin  # Py3 version of urlparse from Python 2.x
from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")


class BaseDisplayHandler(tornado.web.RequestHandler):
    def reverse_full_url(self, name, *args, **kwargs):
        host_url = "{protocol}://{host}".format(**vars(self.request))
        return urljoin(host_url, self.reverse_url(name, *args, **kwargs))


class HomeDisplayHandler(BaseDisplayHandler):
    def get(self):
        self.render("home.html",
            num_dummy_examples=print_toys.K_MAX_TOY_DUMMY_SITES)


class PrintToyDisplayHandler(BaseDisplayHandler):
    def get(self, num_dummy_sites):
        raise NotImplementedError()

    def post(self, num_dummy_sites):
        raise NotImplementedError()


class PrintToySimulation(PrintToyDisplayHandler):
    def get(self, num_dummy_sites):
        num_dummy_sites = int(num_dummy_sites)
        axis_lengths = (2, 2)
        if num_dummy_sites > 2:
            axis_lengths = (4, 4)
        try:
            lattice = print_toys.get_dummy_lattice(
                axis_lengths, num_dummy_sites)
            stop_step = int(self.get_query_argument("stop_step", 0))
            if stop_step:
                lattice = print_toys.simulate_lattice(
                    lattice=lattice, stop_step=stop_step)

            simulation = data.simulation.Simulation(
                stop_step=stop_step, lattice=lattice)
            serialized_sim = self.serialize_simulation(simulation)

            self.render("print_toys/toy_simulation.html",
                sim=simulation,
                serialized_sim=serialized_sim,
                bgcolor_for_cell=print_toys.bgcolor_for_cell)
        except print_toys.PrintToysError as e:
            self.write("Could not print toy with %d dummy sites: %s" % (
                num_dummy_sites, e))

    def post(self, num_dummy_sites):
        num_dummy_sites = int(num_dummy_sites)

        # From empty.
        stop_step = int(self.get_body_argument("stop_step", 0))
        # From serialized.
        additional_steps = int(self.get_body_argument("additional_steps", 0))

        if stop_step:
            simulation = print_toys.simulation_from_scratch(
                num_dummy_sites, stop_step)
        elif additional_steps:
            old_serialized_sim = self.get_body_argument("serialized")
            simulation = data.proto_convert.Simulation.from_proto_b64str(
                old_serialized_sim)
            # TODO: Fix gross hack regarding default for 2x2 toy lattice.
            if tuple(simulation.lattice.coordinate_cardinalities[:2]) == (2, 2):
                simulation = print_toys.simulation_from_scratch(
                    num_dummy_sites, additional_steps)
            else:
                simulation.STOP_STEP = simulation.step + additional_steps
                # TODO: Once storing process queue (enabled_collection) on the
                # client proto, consider preserving -- not naively from scratch.
                simulation.update_process_queue(None, from_scratch=True)
        else:
            raise NotImplementedError("Need input.")

        simulation.run()
        new_serialized_sim = self.serialize_simulation(simulation)
        self.render("print_toys/toy_simulation.html",
            sim=simulation,
            serialized_sim=new_serialized_sim,
            bgcolor_for_cell=print_toys.bgcolor_for_cell)

    def serialize_simulation(self, simulation):
        assert isinstance(simulation, data.simulation.Simulation)
        serialized = data.proto_convert.Simulation.to_proto_b64str(simulation)
        return serialized


class PrintToyLattice(PrintToyDisplayHandler):
    def get(self, num_dummy_sites):
        num_dummy_sites = int(num_dummy_sites)
        axis_lengths = (2, 2)
        if num_dummy_sites > 2:
            axis_lengths = (4, 4)
        try:
            lattice = print_toys.get_dummy_lattice(
                axis_lengths, num_dummy_sites)
            stop_step = int(self.get_query_argument("stop_step", 0))
            if stop_step:
                lattice = print_toys.simulate_lattice(
                    lattice=lattice, stop_step=stop_step)

            serialized_lattice = self.serialize_lattice(lattice)

            self.render("print_toys/toy_lattice.html",
                lattice=lattice,
                serialized_lattice=serialized_lattice,
                bgcolor_for_cell=print_toys.bgcolor_for_cell)
        except print_toys.PrintToysError as e:
            self.write("Could not print toy with %d dummy sites: %s" % (
                num_dummy_sites, e))

    def post(self, num_dummy_sites):
        lattice = None
        simulation_steps = None

        # From empty.
        stop_step = int(self.get_body_argument("stop_step", 0))
        # From serialized.
        simulation_steps = int(self.get_body_argument("additional_steps", 0))

        if stop_step:
            simulation_steps = stop_step
            num_dummy_sites = int(num_dummy_sites)
            axis_lengths = (10, 10)
            lattice = print_toys.get_dummy_lattice(
                axis_lengths, num_dummy_sites, empty=True)
            lattice = print_toys.simulate_lattice(
                lattice=lattice, stop_step=stop_step)
        elif simulation_steps:
            serialized_lattice = self.get_body_argument("serialized")
            lattice = data.proto_convert.Lattice.from_proto_b64str(
                serialized_lattice)
            lattice = print_toys.simulate_lattice(
                lattice=lattice, stop_step=simulation_steps)

        new_serialized_lattice = self.serialize_lattice(lattice)
        self.render("print_toys/toy_lattice.html",
            lattice=lattice,
            serialized_lattice=new_serialized_lattice,
            bgcolor_for_cell=print_toys.bgcolor_for_cell)

    def serialize_lattice(self, lattice):
        assert isinstance(lattice, data.lattice.Lattice)
        return data.proto_convert.Lattice.to_proto_b64str(lattice)


def main():
    parse_command_line()

    app = tornado.web.Application(
        [
            (r"/", HomeDisplayHandler),
            (r"/toy-lattice/(?P<num_dummy_sites>\d+)", PrintToyLattice),
            (r"/toy-simulation/(?P<num_dummy_sites>\d+)", PrintToySimulation),
        ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=options.debug,
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
