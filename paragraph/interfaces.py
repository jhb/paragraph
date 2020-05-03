import json


class ObjectDictEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return sorted(list(obj))
        else:
            return json.JSONEncoder.default(self, obj)


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

class ObjectDict(dict):

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def _similar_to(self, other, ellipsis='...'):
        """Compare nodes to another dictonary, leaving out the ellipsis"""

        errors = {}

        if len(self) != len(other):
            errors['_different len'] = (len(self),len(other))

        for k,v in self.items():
            if ellipsis and  v==ellipsis or other[k]==ellipsis:
                continue
            if v != other[k]:
                errors[k] = (v,other[k])

        if errors:
            return errors
        else:
            return True

    def __eq__(self, other):
        return self._similar_to(other) == True

    def __ne__(self, other):
        return self._similar_to(other) != True

    def to_json(self):
        return json.dumps(self, cls=ObjectDictEncoder, indent=2)

    def from_json(self, jsondata):
        data = json.loads(jsondata)
        if '_labels' in data:
            data['_labels'] = set(data['_labels'])
        self.update(data)


class Node(ObjectDict, Traversal):

    def __init__(self, *labels, **props):
        super().__init__(**props)
        self.setdefault('_id', None)
        self.setdefault('_labels', set())
        self._labels.update(labels)

class Edge(ObjectDict,Traversal):
    def __init__(self, _source=None,_reltype=None,_target=None, **props):
        super().__init__(**props)
        self.setdefault('_id', None)
        self.setdefault('_source',_source)
        self.setdefault('_reltype', _source)
        self.setdefault('_target', _source)

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



