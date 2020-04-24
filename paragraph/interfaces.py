from collections import UserDict


class Traversal:

    def iN(self, *reltypes, minhops=None, maxhops=None, idsonly=False, **filters):
        pass

    def oN(self, *reltypes, minhops=None, maxhops=None, idsonly=False, **filters):
        pass

    def iE(self, *reltypes, minhops=None, maxhops=None, idsonly=False, **filters):
        pass

    def oE(self, *reltypes, minhops=None, maxhops=None, idsonly=False, **filters):
        pass

    def bN(self, *reltypes, minhops=None, maxhops=None, idsonly=False, **filters):
        pass

    def bE(self, *reltypes, minhops=None, maxhops=None, idsonly=False, **filters):
        pass

    def values(self, **keys):
        pass

    def paths(self):
        pass

    def alias(self, name):
        pass

class Node(UserDict,Traversal):
    """Node dict(_id=1,_labels=[],prop1='val1')
    """
    def __init__(self, *labels, **props):
        super().__init__(**props)
        self.labels = set(labels)

    labels = set()

class Edge(UserDict,Traversal):
    """Edge ["""
    source = None
    reltype = None
    target = None

class GraphDB:

    def __init__(self, **kwargs):
        pass

    def add_node(self, *labels, **properties):
        pass

    def update_node(self, node:Node):
        pass

    def del_node(self, nodeid):
        pass

    def add_edge(self, source, reltype, target,  **properties):
        pass

    def update_edge(self, edge:Edge):
        pass

    def del_edge(self, edgeid):
        pass
    
    def add_node_index(self, name, index):
        pass
    
    def del_node_index(self, name):
        pass
    
    def query_node(self, **filters):
        pass

    def add_edge_index(self, name, index):
        pass

    def del_edge_index(self, name):
        pass

    def query_edge(self, **filters):
        pass

    def begin(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def query(self, query):
        pass


class Traverser(Traversal):

    g:GraphDB = None

    def __init__(self, graph:GraphDB):
        pass



