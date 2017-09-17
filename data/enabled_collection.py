import sortedcontainers


class EnabledCollection(object):

    def __init__(self, key_fn=None):
        # Requirements:
        # Add element, log n
        # Pop lowest value by occurence time, log n
        #
        # Nice to have:
        # Evict expired processes eg prune values < x, min(# pruned, log n)
        #
        # Current top ideas:
        # SortedListWithKey
        # http://www.grantjenks.com/docs/sortedcontainers/sortedlistwithkey.html
        # IMHO this will do for early iterating; we could build our own, but
        # honestly this is likely more performant. As a plus, it's pythonic AF.
        assert callable(key_fn), "Need callable for sorted process queue."
        self._queue = sortedcontainers.SortedListWithKey(key=key_fn)

    def add(self, process):
        # Assumes occurence time used as key.
        self._queue.add(process)

    def pop(self, raise_if_empty=False):
        try:
            return self._queue.pop(0)
        except IndexError as e:
            if raise_if_empty:
                raise e
            return None

    def clear(self):
        self._queue.clear()

    def peek(self):
        process = self.pop()
        if process:
            self.add(process)
        return process

    def __len__(self):
        return len(self._queue)

    def __repr__(self):
        return "%d process%s,peek:%r" % (
            len(self._queue), "es" if len(self._queue) != 1 else "",
            self.peek()
        )
