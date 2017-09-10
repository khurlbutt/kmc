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
        num_dummy_sites = int(num_dummy_sites)
        try:
            lattice = print_toys.get_dummy_lattice(num_dummy_sites)
            self.render("lattice.html", lattice=lattice)
        except print_toys.PrintToysError as e:
            self.write("Could not print toy with %d dummy sites: %s" % (
                num_dummy_sites, e))


def main():
    parse_command_line()

    app = tornado.web.Application(
        [
            (r"/", HomeDisplayHandler),
            (r"/print-toy/(?P<num_dummy_sites>\d+)", PrintToyDisplayHandler),
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
