

class Process(object):

    def __init__(self, enabled_step, occurence_time, transition_by_site):
        assert isinstance(enabled_step, int)
        assert isinstance(transition_by_site, dict)

        self.enabled_step = enabled_step
        self.occurence_time = occurence_time
        # Map of 3-tuple (row, col, site_index) to 2-tuple (before, after)
        self.transition_by_site = transition_by_site

    def key_fn(self):
        # Used by data.enabled_collection.EnabledCollection for sorting.
        return self.occurence_time

    def perform(self, lattice):
        if not self.is_still_performable(lattice):
            raise LatticeProcessException("Not performable")
        for global_site, transition in self.transition_by_site.items():
            cell_row = global_site[0]
            cell_col = global_site[1]
            local_site_index = global_site[2]
            after_adsorbate = transition[1]

            lattice.cells[cell_row][cell_col].sites[local_site_index] = (
                after_adsorbate)

    def is_still_performable(self, lattice):
        for global_site, transition in self.transition_by_site.items():
            cell_row = global_site[0]
            cell_col = global_site[1]
            local_site_index = global_site[2]
            before_adsorbate = transition[0]

            curr = lattice.cells[cell_row][cell_col].sites[local_site_index]
            if before_adsorbate != curr:
                return False
            # TODO: Blocked by sites not yet storing last updated step.
            # if site.last_updated_step > self.enabled_step:
            #     return False

        return True

    def __repr__(self):
        return "%r" % [
            self.enabled_step,
            self.occurence_time,
            "transition_by_site: %r" % sorted([
                "@(%d,%d,%d)%s -> %s" % (
                    site[0], site[1], site[2], transition[0], transition[1])
                for site, transition in self.transition_by_site.items()]),
        ]


class LatticeProcessException(Exception):
    pass
