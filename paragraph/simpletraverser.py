from _collections import OrderedDict

from paragraph.interfaces import Traverser, GraphDB


class SimpleTraverser(Traverser):

    def __init__(self, graphdb: GraphDB, nodes, prev=None):
        self.g = graphdb
        if type(nodes) != list:
            nodes = [nodes]
        self.nodes = nodes
        self.prev = prev
        self.resultnodes = OrderedDict()
        self.resultedges = OrderedDict()

    def oN(self, *reltypes, minhops=1, maxhops=1, ids=False, **filters):
        self.resultnodes = OrderedDict()
        self.resultedges = OrderedDict()
        thisround = OrderedDict({n._id: n for n in self.nodes})
        nextround = OrderedDict()
        for hop in range(1, maxhops + 1):
            for node in thisround.values():
                edges = self.g.query_edges(*reltypes, _source=node)
                for edge in edges:
                    self.resultedges[edge._id] = edge
                    target = edge._target
                    if hop >= minhops and target._id not in self.resultnodes:
                        self.resultnodes[target._id] = target
                    if target._id not in nextround:
                        nextround[target._id] = target

            thisround = nextround
            nextround = OrderedDict()

        return SimpleTraverser(self.g, list(self.resultnodes.values()), prev=self)
        # return (list(resultnodes.values()), list(resultedges.values()))

    @property
    def goodnodes(self):
        out = OrderedDict()
        t = self
        while 1:
            out.update(t.resultnodes)
            t = t.prev
            if t is None:
                break
        return list(out.values())

    def same_nodes(self, othernodes):
        if type(othernodes) != list:
            othernodes = [list]
        return {n._id for n in self.nodes} == set([n._id for n in othernodes])
