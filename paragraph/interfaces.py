import json
from pprint import pprint


class ObjectDictEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return sorted(list(obj))
        else:
            return json.JSONEncoder.default(self, obj)


class Traversal:

    def iN(self, *reltypes, minhops=None, maxhops=None, ids=False, **filters):
        pass

    def oN(self, *reltypes, minhops=None, maxhops=None, ids=False, **filters):
        pass

    def iE(self, *reltypes, minhops=None, maxhops=None, ids=False, **filters):
        pass

    def oE(self, *reltypes, minhops=None, maxhops=None, ids=False, **filters):
        pass

    def bN(self, *reltypes, minhops=None, maxhops=None, ids=False, **filters):
        pass

    def bE(self, *reltypes, minhops=None, maxhops=None, ids=False, **filters):
        pass

    def values(self, **keys):
        pass

    def paths(self):
        pass

    def alias(self, name):
        pass


def similar_dict(this, other, ellipsis='...'):
    """Compare nodes to another dictonary, leaving out the ellipsis"""

    errors = {}

    if not isinstance(other, dict):
        errors['_not suitable type'] = (type(this), type(other))
        return False

    if len(this) != len(other):
        errors['_different len'] = (len(this), len(other))

    for k, v in this.items():
        if ellipsis and v == ellipsis or other[k] == ellipsis:
            continue
        if v != other[k]:
            errors[k] = (v, other[k])

    if errors:
        return False  # 00_todo
    else:
        return True


class ObjectDict(dict):

    def _similar_to(self, other, ellipsis='...'):
        """Compare nodes to another dictonary, leaving out the ellipsis"""
        return similar_dict(self, other, ellipsis=ellipsis)

    def __eq__(self, other):
        return self._similar_to(other) == True

    def __ne__(self, other):
        return self._similar_to(other) != True


    def _set(self,k,v):
        self[k]=v

    def _del(self,k):
        del(self[k])

    def __hash__(self):
        return int(self.id, 16)
    
    id = property(lambda self: self['_id'],
                  lambda self, v: self._set('_id',v),
                  lambda self: self._del('_id'))


class Node(ObjectDict, Traversal):

    def __init__(self, *labels, **props):
        super().__init__(**props)
        self.setdefault('_id', None)
        self.labels = set(labels)
        #self.__dict__['labels']=self['_labels'] # 00_label_usage

    def to_json(self, indent=None):
        data = dict(self)
        data['_labels']=list(self.labels)
        return json.dumps(data, cls=ObjectDictEncoder, indent=indent)

    def from_json(self, jsondata):
        data = json.loads(jsondata)
        if '_labels' in data:
            self.labels.update(data['_labels'])
            del data['_labels']
        self.update(data)

class Edge(ObjectDict, Traversal):
    def __init__(self, source=None, reltype=None, target=None, **props):
        super().__init__(**props)
        self.setdefault('_id', None)
        self.source = source
        self.reltype = reltype
        self.target = target

    def to_json(self, indent=None):
        data = dict(self)
        data['_source'] = self.source.id
        data['_target'] = self.target.id
        data['_reltype'] = self.reltype
        return json.dumps(data, cls=ObjectDictEncoder, indent=indent)

    def from_json(self, jsondata):
        raise Exception('needs implementation, getting nodes from db')
        data = json.loads(jsondata)
        if '_labels' in data:
            self.labels.update(data['_labels'])
            del data['_labels']
        self.update(data)
    
    
    def __repr__(self):
        data = dict(self.items())
        data['_source'] = self.source.id
        data['_target'] = self.target.id
        return str(data)


class GraphDB:

    def __init__(self, **kwargs):
        pass

    def add_node(self, *labels, **properties):
        pass

    def update_node(self, node:Node):
        pass

    def del_node(self, nodeid):
        pass

    def add_edge(self, _source, _reltype, _target, **properties):
        pass

    def update_edge(self, edge:Edge):
        pass

    def del_edge(self, edgeid):
        pass
    
    def add_node_index(self, name, index):
        pass
    
    def del_node_index(self, name):
        pass

    def query_nodes(self, **filters):
        pass

    def add_edge_index(self, name, index):
        pass

    def del_edge_index(self, name):
        pass

    def query_edges(self, *reltypes, **filters):
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
    pass
