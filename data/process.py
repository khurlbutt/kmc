

class Process(object):

    def __init__(self, enabled_step, occurence_time, transition_by_site):
        assert isinstance(enabled_step, int)
        assert isinstance(transition_by_site, dict)

        self.enabled_step = enabled_step
        self.occurence_time = occurence_time
        # Map of 3-tuple (row, col, site_index) to 2-tuple (before, after)
        self.transition_by_site = transition_by_site
        # Convenience, assumes transition_by_site is immutable.
        self.sites_coordinates = list(transition_by_site.keys())

    def key_fn(self):
        # Used by data.enabled_collection.EnabledCollection for sorting.
        return self.occurence_time

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
            if before_adsorbate != site.state:
                return False
            # TODO: Blocked by sites not yet storing last updated step.
            # if site.last_updated_step > self.enabled_step:
            #     return False
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
