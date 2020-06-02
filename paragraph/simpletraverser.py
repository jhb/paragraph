from _collections import OrderedDict

from paragraph.basic import Traversal, GraphDB, ResultWrapper


class SimpleTraverser(ResultWrapper):

    def __init__(self, graphdb: GraphDB, nodes, prev=None):
        self.rows = []
        self.g = graphdb
        if type(nodes) != set and type(nodes) != list:
            nodes = {nodes}
        self.nodes = nodes
        self.prev = prev

        self.nodes_seen = set()
        self.edges_seen = set()
        self.edges = self.edges_seen

        if prev:
            self.nodes_seen.update(self.prev.nodes_seen)
            self.edges_seen.update(self.prev.edges_seen)

    def oN(self, *reltypes, minhops=1, maxhops=1, ids=False, **filters):
        return self._traverseN('target',*reltypes, minhops=minhops, maxhops=maxhops, ids=ids, **filters)

    def iN(self, *reltypes, minhops=1, maxhops=1, ids=False, **filters):
        return self._traverseN('source', *reltypes, minhops=minhops, maxhops=maxhops, ids=ids, **filters)

    def _traverseN(self, otherattribute, *reltypes, minhops=1, maxhops=1, ids=False, **filters):
        thisround = set(self.nodes)
        nextround = set()
        found = set()
        for i in range(1,maxhops+1):
            for node in thisround:
                if node in self.nodes_seen:
                    continue
                else:
                    self.nodes_seen.add(node)
                if otherattribute=='target':
                    edges = self.g.query_edges(*reltypes, source=node).edges
                else:
                    edges = self.g.query_edges(*reltypes, target=node).edges
                for edge in edges:
                    if edge in self.edges_seen:
                        continue
                    self.edges_seen.add(edge)
                    other = getattr(edge,otherattribute)
                    #nextround
                    if other not in self.nodes_seen:
                        nextround.add(other)
                    #found
                    if i>=minhops and other not in found:
                        found.add(other)

            thisround=nextround
            nextround=set()

        return SimpleTraverser(self.g, nodes=found, prev=self)

    def allnodes(self):
        return SimpleTraverser(self.g, set(self.nodes) | set(self.nodes_seen),prev=self)




