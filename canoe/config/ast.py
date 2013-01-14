from importlib import import_module

from canoe import Canoe

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

        print self.assignments
        print kwargs

        if self.decl_type == 'chisel':
            klass = find_chisel(self.path)
            print klass
        elif self.decl_type == 'route':
            klass = find_route(self.path)
        else:
            raise ValueError("Don't know what to do with '%s'" % \
                                 self.decl_type)

        # TODO: find and instantiate path with kwargs!
        return klass(**kwargs)


class WatchNode(Node):

    def __init__(self, f, chisels=None, route=None):
        self.file = f
        self.chisels = chisels
        self.route = route

    def evaluate(self, env):
        eroute = None
        echisels = None
        if self.route:
            eroute = self.route.evaluate(env)

        # TODO: if no chisels, pass everything through.
        # TODO: if no route, use default Print route    
        if self.chisels:
            echisels = [c.evaluate(env) for c in self.chisels]
            
        canoe = Canoe(echisels, eroute)

        # TODO: this isn't quite right, since we can have multiple
        #  canoes per file
        return (self.file, [canoe])


class ValueNode(Node):
    
    def __init__(self, value):
        print "Creating value node: ", value
        self.value = value

    def evaluate(self, env):
        return self.value


# TODO: derefs are never created from the parser
class DerefNode(Node):
    
    def __init__(self, identifier):
        self.identifier = identifier

    def evaluate(self, env):
        if self.identifier in env:
            return env[self.identifier]
        raise NameError("can't dereference '%s'. Not defined." % \
                            self.identifier)


def find_chisel(p):
    if '.' not in p:
        p = 'canoe.chisels.' + p
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
