

class Process(object):

    def __init__(self, enabled_step, transition_by_site,
            occurence_usec=None, rate_constant=None):
        assert isinstance(enabled_step, int)
        assert isinstance(transition_by_site, dict) and transition_by_site

        self.enabled_step = enabled_step or 0
        self.occurence_usec = occurence_usec or None
        self.rate_constant = rate_constant or None

        self._sites_coordinates = frozenset(transition_by_site.keys())
        # Should treat as immutable!
        # Map of 3-tuple (row, col, site_index) to 2-tuple (before, after)
        self._transition_by_site = transition_by_site

    def enabled_collection_sorting_fn(self):
        # Used by data.enabled_collection.EnabledCollection for sorting.
        if self.occurence_usec is None:
            raise SimProcessException("Occurence time never initialized.")
        return self.occurence_usec

    def sites_coordinates(self):
        return sorted(self._sites_coordinates)

    def generate_occurence_usec(self, current_usec, rate_constant=None):
        import random
        if rate_constant is not None:
            print("Would use %r as rate constant." % rate_constant)
            import math
            self.occurence_usec = (
                1 / 1 + math.exp(random.random() ** rate_constant))
        else:
            self.occurence_usec = current_usec + int((random.random() * 1e6))

    def perform(self, step, lattice):
        if not self.is_still_performable(lattice):
            raise SimProcessException("Not performable")
        for site_coordinates, transition in self._transition_by_site.items():
            after_adsorbate = transition[1]
            lattice[site_coordinates].transition(step, after_adsorbate)

    def is_still_performable(self, lattice):
        for site_coordinates, transition in self._transition_by_site.items():
            site = lattice[site_coordinates]
            before_adsorbate = transition[0]
            if self.enabled_step < site.last_update_step:
                return False
            if before_adsorbate != site.state:
                return False
        return True

    def __hash__(self):
        # Helps to more efficiently compute data.simulation.update_process_queue
        return hash(tuple(sorted(self._sites_coordinates)))

    def __repr__(self):
        return (
            "enabled_step=%s,occurence_time=%s,%r" % (self.enabled_step,
                self.occurence_usec,
                # TODO nit: rate_constant
                sorted(["@%r%s -> %s" % (s_coords, transition[0], transition[1])
                for s_coords, transition in self._transition_by_site.items()])))


class SimProcessException(Exception):
    pass
