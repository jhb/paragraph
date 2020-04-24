class Traverser:

    def __init__(self, graph):
        self.g = graph
        self.results = [] # pro Step können auch mehrere Elemente abgelegt werden, die dann später extended werden
        self.aliases = {}
        self.current = None


class Foo:
    bar = 3

class Foo2(Foo):

    def __init__(self, x):
        self.bar = x

a = Foo2(1)
b = Foo2(2)

print(a.bar)
print(b.bar)