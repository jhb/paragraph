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
        if prev:
            self.resultnodes.update(prev.resultnodes)
            self.resultedges.update(prev.resultnodes)

        self.nodes_seen = OrderedDict()
        self.edges_seen = OrderedDict()

        if prev:
            self.nodes_seen.update(self.prev.nodes_seen)
            self.edges_seen.update(self.prev.edges_seen)


    def oN1(self, *reltypes, minhops=1, maxhops=1, ids=False, **filters):
        localnodes = OrderedDict()
        thisround = OrderedDict({n._id: n for n in self.nodes})
        nextround = OrderedDict()
        for hop in range(1, maxhops + 1):
            for node in thisround.values():
                edges = self.g.query_edges(*reltypes, _source=node)
                for edge in edges:
                    self.resultedges[edge._id] = edge
                    target = edge._target
                    if hop >= minhops and target._id not in localnodes:
                        localnodes[target._id] = target
                    if target._id not in nextround:
                        nextround[target._id] = target

            thisround = nextround
            nextround = OrderedDict()
        self.resultnodes.update(localnodes)
        return SimpleTraverser(self.g, list(localnodes.values()), prev=self)
        # return (list(resultnodes.values()), list(resultedges.values()))

    def oN(self, *reltypes, minhops=1, maxhops=1, ids=False, **filters ):
        thisround = OrderedDict({n._id:n for n in self.nodes})
        nextround = OrderedDict()
        found = OrderedDict()
        for i in range(1,maxhops+1):
            for node in thisround.values():
                if node._id in self.nodes_seen:
                    continue
                else:
                    self.nodes_seen[node._id] = node
                edges = self.g.query_edges(*reltypes, _source=node)
                for edge in edges:
                    if edge._id in self.edges_seen:
                        continue
                    self.edges_seen[edge._id] = edge
                    target = edge._target
                    #nextround
                    if target._id not in self.nodes_seen:
                        nextround[target._id]=target
                    #found
                    if i>=minhops and target._id not in found:
                        found[target._id]=target

            thisround=nextround
            nextround=OrderedDict()
        return SimpleTraverser(self.g, nodes=list(found.values()), prev=self)

    def same_nodes(self, othernodes):
        if type(othernodes) != list:
            othernodes = [list]
        return {n._id for n in self.nodes} == set([n._id for n in othernodes])
