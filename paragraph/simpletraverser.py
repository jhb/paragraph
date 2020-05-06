from _collections import OrderedDict
from copy import copy

from paragraph.interfaces import Traverser


class SimpleTraverser(Traverser):

    def oN(self, *reltypes, minhops=0, maxhops=1, ids=False, **filters):
        resultnodes = OrderedDict()
        resultedges = OrderedDict()
        thisround = copy(self.nodes)
        nextround = []
        for hop in range(minhops, maxhops):
            for node in thisround:
                edges = self.g.query_edges(*reltypes, _source=node)
                for edge in edges:
                    resultedges[edge._id] = edge
                    target = edge._target
                    if target._id not in resultnodes:
                        resultnodes[target._id] = target
                        nextround.append(target)
            thisround = nextround
            nextround = []
        return SimpleTraverser(self.g, list(resultnodes.values()))
        # return (list(resultnodes.values()), list(resultedges.values()))
