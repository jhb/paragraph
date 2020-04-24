from collections import UserDict

class GraphDatabase:

    def add_node(self, *labels, **properties):
        pass

    def get_node(self, **searchparams):
        pass

    def del_node(self, nodeid):
        pass

    def add_edge(self, source, type, target, **properties):
        pass

    def get_edge(self, **searchparams):
        pass

    def del_edge(self, edgeid):
        pass

    def query(self, query):
        pass



class PropertyObject(UserDict):
    pass

class Node(PropertyObject):

    def __init__(self,*args, **kwargs):
        super().__init__(**kwargs)
        self.labels = list(args)

class Edge(PropertyObject):

    def __init__(self, source, reltype, target, **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.reltype = reltype
        self.target = target


n1 = Node('foo','bar',_id=17, bla='blub')
print(n1)
print(n1.labels)