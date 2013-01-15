_filter = filter

def filter(func):
    func.filter = True
    return func

@filter
def filter_factory(func):
    func.factory = True
    return func
