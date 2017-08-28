

class Process(object):

    def __init__(self, est_perform_time, cell, is_enabled_still_fn, perform_fn):
        # From what I can tell a simple model might use 4 inputs:
        # est_perform_time : estimated time(step) of occurence
        # cell : lattice cell in question
        # is_enabled_still_fn : method to know if process still "allowed" after
        #                       considering lattice changes since entry into
        #                       EnabledCollection, i.e. a "null event" check
        # perform_fn : method for performing what process would do if enacted
        self._est_perform_time = est_perform_time
        # TODO: Only cell indices
        self.cell = cell
        # TODO: Only 2-tuple, e.g. index of function template, cell indices
        # TODO: This must invalidate processes involving sites updated since
        #       process est_perform_time to avoid oversampling expired processes
        #       that otherwise meet enablement criteria.
        self._is_enabled_still_fn = is_enabled_still_fn
        # TODO: Only 2-tuple, e.g. index of function template, cell indices
        self._perform_fn = perform_fn
        self._is_performed = False

    def time_value(self):
        return int(self._est_perform_time)

    def perform(self):
        if not self.is_still_performable():
            raise LatticeProcessException("Not performable")
        self._perform_fn(self.cell)
        self._is_performed = True

    def is_still_performable(self):
        # Assumes that references to cell sites updated elsewhere. Eventually,
        # may need to reference neighbors using cell.row or cell.col.
        return not self._is_performed and self._is_enabled_still_fn(self.cell)

    def is_performed(self):
        return bool(self._is_performed)

    def __repr__(self):
        return "%r" % [
            self._est_perform_time,
            (self.cell.row, self.cell.col),
            ("is_performed", self.is_performed()),
            ("_is_enabled_still_fn", self._is_enabled_still_fn),
            ("_perform_fn", self._perform_fn)]


class LatticeProcessException(Exception):
    pass
