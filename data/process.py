

class Process(object):

    def __init__(self, enabled_step, transition_by_site):
        assert isinstance(enabled_step, int)
        assert isinstance(transition_by_site, dict) and transition_by_site

        self.enabled_step = enabled_step
        self.occurence_time = None
        # Map of 3-tuple (row, col, site_index) to 2-tuple (before, after)
        self.transition_by_site = transition_by_site
        # Convenience, assumes transition_by_site is immutable.
        self.sites_coordinates = list(transition_by_site.keys())

    def key_fn(self):
        # Used by data.enabled_collection.EnabledCollection for sorting.
        if self.occurence_time is None:
            raise LatticeProcessException("Occurence time never initialized.")
        return self.occurence_time

    def generate_occurence_time(self, current_time):
        # TODO...
        self.occurence_time = current_time + 1

    def perform(self, lattice):
        if not self.is_still_performable(lattice):
            raise LatticeProcessException("Not performable")
        for site_coordinates, transition in self.transition_by_site.items():
            after_adsorbate = transition[1]
            lattice.sites[site_coordinates].state = after_adsorbate

    def is_still_performable(self, lattice):
        for site_coordinates, transition in self.transition_by_site.items():
            site = lattice.sites[site_coordinates]
            before_adsorbate = transition[0]
            if self.enabled_step < site.last_update_step:
                return False
            if before_adsorbate != site.state:
                return False
        return True

    def __repr__(self):
        return "%r" % [
            self.enabled_step,
            self.occurence_time,
            sorted(["@%r%s -> %s" % (site, transition[0], transition[1])
                for site, transition in self.transition_by_site.items()]),
        ]


class LatticeProcessException(Exception):
    pass
