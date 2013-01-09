def lift_iter(xs):
    if not xs:
        return []
    if hasattr(xs, '__iter__'):
        return xs
    return [xs]


class Canoe(object):

    def __init__(self, filters=None, route=None):
        self._filters = lift_iter(filters)
        self._route = route

    def send(self, line, buffer):
        for f in self._filters:
            nline, nbuffer = f(line, buffer)

        if nline != None and buffer != None:
            if self._route:
                return self._route(line, buffer)

    def add_filter(self, filter):
        self._filters.append(filters)

    def set_route(self, route):
        self._route = route
