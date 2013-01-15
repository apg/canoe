def route(func):
    func.route = True
    return func

@route
def route_factory(func):
    func.factory = True
    return func
