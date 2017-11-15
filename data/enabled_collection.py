import data.process
import sortedcontainers


class EnabledCollection(object):

    def __init__(self, sorting_fn=None):
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
        assert callable(sorting_fn), "Need callable for sorted process queue."
        self._queue = sortedcontainers.SortedListWithKey(key=sorting_fn)

    def add(self, process):
        # Assumes occurence time used as key.
        assert isinstance(process, data.process.Process)
        self._queue.add(process)

    def pop(self, peek_only=False):
        try:
            return self._queue.pop(0)
        except IndexError as e:
            if peek_only:
                return None
            raise EnabledCollectionError(e)

    def clear(self):
        self._queue.clear()

    def peek(self):
        process = None
        process = self.pop(peek_only=True)
        if process:
            self.add(process)
        return "%r" % process

    def __len__(self):
        return len(self._queue)

    def __repr__(self):
        return "%d process%s,peek:%r" % (
            len(self._queue), "es" if len(self._queue) != 1 else "",
            self.peek()
        )


class EnabledCollectionError(IndexError):
    pass
