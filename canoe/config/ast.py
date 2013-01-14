from importlib import import_module

from canoe.canoe import Canoe
from canoe.routes import EchoRoute
from canoe.filters import PassThroughFilter

# TODO: need to import stuff in here I'm sure!

class Node(object):

    def evalute(self, env):
        raise NotImplementedError("Override me please")


class ConfigNode(Node):
    
    def __init__(self, top_assignments=None, watches=None):
        self.top_assignments = top_assignments
        self.watches = watches

    def evaluate(self, env):
        from config import Config
        if self.top_assignments:
            for x in self.top_assignments:
                x.evaluate(env)

        watches = [w.evaluate(env) for w in self.watches]
        return Config(watches)


class AssNode(Node):
    
    def __init__(self, identifier=None, value=None):
        self.identifier = identifier
        self.value = value

    def evaluate(self, env):
        if self.value:
            env[self.identifier] = self.value.evaluate(env)
        else:
            raise ValueError("Can't evaluated assignment without an rvalue")


class DeclNode(Node):
                   
    def __init__(self, typ, path=None, assignments=None):
        self.decl_type = typ
        self.path = path
        self.assignments = assignments

    def evaluate(self, env):
        kwargs = {}

        if self.assignments:
            for a in self.assignments:
                a.evaluate(kwargs)

        if self.decl_type == 'filter':
            klass = find_filter(self.path)
        elif self.decl_type == 'route':
            klass = find_route(self.path)
        else:
            raise ValueError("Don't know what to do with '%s'" % \
                                 self.decl_type)
        return klass(**kwargs)


class WatchNode(Node):

    def __init__(self, f, filters=None, route=None):
        self.file = f
        self.filters = filters
        self.route = route

    def evaluate(self, env):
        eroute = None
        efilters = None
        if self.route:
            eroute = self.route.evaluate(env)
        else:
            eroute = EchoRoute()

        if self.filters:
            efilters = [c.evaluate(env) for c in self.filters]
        else:
            efilters = [PassThroughChisel()]
            
        canoe = Canoe(efilters, eroute)

        # Let someone else deal with the fact that there can be
        # multiple canoes per file
        return (self.file, [canoe])


class ValueNode(Node):
    
    def __init__(self, value):
        print "Creating value node: ", value
        self.value = value

    def evaluate(self, env):
        if isinstance(self.value, DerefNode):
            return self.value.evaluate(env)
        return self.value


class DerefNode(Node):
    
    def __init__(self, identifier):
        self.identifier = identifier

    def evaluate(self, env):
        if self.identifier in env:
            return env[self.identifier]
        raise NameError("can't dereference '%s'. Not defined." % \
                            self.identifier)


# TODO: this is crap, and should definitely be smarter, allow for
# better pluginy infrastructure, etc
def find_filter(p):
    if '.' not in p:
        p = 'canoe.filters.' + p
    return _import_class(p)

def find_route(p):
    if '.' not in p:
        p = 'canoe.routes.' + p
    return _import_class(p)

def _import_class(p):
    bits = p.split('.')
    mod = '.'.join(bits[0:-1])
    cls = bits[-1]

    imod = import_module(mod)
    return getattr(imod, cls)
