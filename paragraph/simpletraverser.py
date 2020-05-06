from _collections import OrderedDict

from paragraph.interfaces import Traverser


class SimpleTraverser(Traverser):

    def oN(self, nodes, *reltypes, minhops=0, maxhops=1, ids=False, **filters):
        if type(nodes) != list:
            nodes = [nodes]
        resultnodes = OrderedDict()
        resultedges = OrderedDict()
        thisround = list(nodes)
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
        return (list(resultnodes.values()), list(resultedges.values()))
