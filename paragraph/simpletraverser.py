from _collections import OrderedDict

from paragraph.interfaces import Traverser, GraphDB


class SimpleTraverser(Traverser):

    def __init__(self, graphdb: GraphDB, nodes, prev=None):
        self.g = graphdb
        if type(nodes) != set and type(nodes) != list:
            nodes = set([nodes])
        self.nodes = nodes
        self.prev = prev

        self.nodes_seen = set()
        self.edges_seen = set()

        if prev:
            self.nodes_seen.update(self.prev.nodes_seen)
            self.edges_seen.update(self.prev.edges_seen)


    def oN(self, *reltypes, minhops=1, maxhops=1, ids=False,  **filters ):
        thisround = set(self.nodes)
        nextround = set()
        found = set()
        for i in range(1,maxhops+1):
            for node in thisround:
                if node in self.nodes_seen:
                    continue
                else:
                    self.nodes_seen.add(node)
                edges = self.g.query_edges(*reltypes, _source=node)
                for edge in edges:
                    if edge in self.edges_seen:
                        continue
                    self.edges_seen.add(edge)
                    target = edge._target
                    #nextround
                    if target not in self.nodes_seen:
                        nextround.add(target)
                    #found
                    if i>=minhops and target not in found:
                        found.add(target)

            thisround=nextround
            nextround=set()
        return SimpleTraverser(self.g, nodes=found, prev=self)

    def same_nodes(self, othernodes):
        if type(othernodes) != list:
            othernodes = [list]
        return {n._id for n in self.nodes} == set([n._id for n in othernodes])

    def allnodes(self):
        return self.nodes + self.nodes_seen
