"""Database driver for neo4j"""
from typing import Any, Union, Sequence
from uuid import uuid4

from neo4j import GraphDatabase, Result
import neo4j
import neo4j.graph

from paragraph.basic import GraphDB, Node, Edge, ResultWrapper
from paragraph.schemahandler import Schemahandler
from paragraph.simpletraverser import SimpleTraverser
from paragraph import signals
import logging


# noinspection PyCallingNonCallable
class NeoGraphDB:

    def __init__(self,
                 uri: str = 'bolt://localhost:7687',
                 username: str = '',
                 password: str = '',
                 encrypted: bool = False,
                 debug: int = 0) -> None:

        self.driver = GraphDatabase.driver(uri, auth=(username, password), encrypted=encrypted)
        self.session = self.driver.session()
        self.tx = None
        self.debug = debug

        # some form of caching
        self._nodecache = {}
        self._edgecache = {}
        self.propdict = {}

        # populate the propdict
        self._update_propdict()

    def __call__(self, *args, **kwargs):
        return self.query_nodes(*args, **kwargs)

    def begin(self) -> neo4j.Transaction:
        """Begin a transaction"""

        if not self.tx:
            self.tx = self.session.begin_transaction()
        return self.tx

    def _run(self, statement: str, **kwargs: Any) -> neo4j.Result:
        """running the actual cypher statement"""
        tx = self.begin()
        logging.debug(f'{statement} --- {kwargs}')
        if self.debug == 2:
            self.debug = 0
        result = tx.run(statement, **kwargs)
        return result

    def _neo2node(self, neonode: neo4j.graph.Node) -> Node:
        """convert a node from a neo4j result into a paragraph.basic.Node"""
        nodeid = neonode['_id']
        if nodeid not in self._nodecache:
            node = Node(self)
            node.update(neonode)
            node.labels.update(neonode.labels)
            self._nodecache[nodeid] = node
        return self._nodecache[nodeid]

    def _neo2edge(self, relation: neo4j.graph.Relationship) -> Edge:
        """convert a relationship from a neo4j result into a paragraph.basic.Edge"""
        edgeid = relation['_id']
        if edgeid not in self._edgecache:
            edge = Edge(db=self,
                        source=self._neo2node(relation.start_node),
                        reltype=relation.type,
                        target=self._neo2node(relation.end_node))
            edge.update(relation.items())
            self._edgecache[edgeid] = edge
        return self._edgecache[edgeid]

    def _nodeid(self, nodeid: Union[str, Node]):
        """Helper to return the id of a node if nodeid is an actual Node"""
        if type(nodeid) is Node:
            return nodeid.id
        else:
            return nodeid

    def _edgeid(self, edgeid: Union[str, Edge]):
        """Helper to return the id of an edge if edgeid is an actual Edge"""
        if type(edgeid) is Edge:
            return edgeid.id
        else:
            return edgeid


    def _new_uid(self) -> str:
        """Create a new uid"""
        return uuid4().hex

    def _labels2string(self, labels: Sequence) -> str:
        """Returns the labels as a string formatted for use in a cypher statement"""
        labelstring = ':'.join([str(l) for l in labels])
        if labelstring:
            labelstring = ':' + labelstring
        return labelstring

    def add_node(self, *labels: str, **properties: Any) -> Node:
        """Creates and adds a node"""
        if '_id' not in properties:
            properties['_id'] = self._new_uid()
        if type(labels) != set:
            labels = set(labels)
        signals.before_label_store.send(self, labels=labels, properties=properties)
        labelstring = self._labels2string(labels)
        result = self._run(f'create (n{labelstring}) set n = $props return n', props=properties)
        return self._neo2node(result.single()['n'])

    def update_node(self, node: Node) -> Node:
        """Updates the node in the database, and returns the updated node"""
        signals.before_label_store.send(self, labels=node.labels, properties=node)
        labelstring = self._labels2string(node.labels)
        if labelstring:
            labelstring = 'set n' + labelstring
        result = self._run(f'match (n) where n._id=$_id {labelstring} set n=$props return n',
                           labelstring=labelstring,
                           _id=node['_id'],
                           props=dict(node))
        return self._neo2node(result.single()['n'])

    def del_node(self, _id: Union[str, Node], detach: bool = False) -> None:
        """Deletes the node from the db. Detach will also delte attached edges"""

        _id = self._nodeid(_id)
        if detach:
            result = self._run("match (n) where n._id=$_id detach delete n", _id=_id)
        else:
            result = self._run("match (n) where n._id=$_id delete n", _id=_id)

    def query_nodes(self, *labels: str, **filters: Any) -> ResultWrapper:
        """Query nodes by the given labels and filters"""
        labelstring = self._labels2string(labels)
        result = self._run('''WITH $filters as filters 
                              MATCH (n%s) WHERE ALL(k in keys(filters) WHERE filters[k] = n[k])
                              return n''' % labelstring,
                           filters=filters)
        # return Neo4jWrapper([self._neo2node(r['n']) for r in result],self)
        return Neo4jWrapper(result, self)

    def add_edge(self, source: Union[str, Edge], reltype: str, target: Union[str, Edge], **properties: Any) -> Edge:
        """Add and return an edge"""
        if '_id' not in properties:
            properties['_id'] = self._new_uid()
        props = dict(properties)
        s_id = self._nodeid(source)
        t_id = self._nodeid(target)
        r = self._run('''match (s) where s._id=$s_id
                         match (t) where t._id=$t_id
                         create (s)-[r:%s]->(t) set r = $props return s,r,t
        ''' % reltype, s_id=s_id, t_id=t_id, props=props)

        return self._neo2edge(r.single()['r'])

    def update_edge(self, edge: Edge) -> Edge:
        """Update the edge in the database and return the updated edge"""
        r = self._run('''match (s)-[r]->(t) where r._id=$r_id set r = $props return s,r,t''', r_id=edge.id,
                      props=dict(edge))
        return self._neo2edge(r.single()['r'])

    def query_edges(self,
                    *reltypes: str,
                    source: Union[str, Edge] = None,
                    target:  Union[str, Edge] = None,
                    **filters) -> ResultWrapper:
        """Query edge, filter by the given reltypes, source, target and filters"""
        # 00_todo filter by node types/labels
        relstring = ''
        if reltypes:
            if type(reltypes) not in [list, tuple]:
                reltypes = [reltypes]
            relstring = ':' + '|'.join(reltypes)
        # for k, v in filters.items():
        #    filters[k] = self._nodeid(v)
        wheres = []
        params = dict(filters=filters)
        if source:
            wheres.append('s._id=$_s_id')
            params['_s_id'] = self._nodeid(source)
        if target:
            wheres.append('t._id=$_t_id')
            params['_t_id'] = self._nodeid(target)
        if wheres:
            wheres.insert(0, '')

        result = self._run('''with $filters as filters
                              match (s)-[r%s]->(t)
                              WHERE ALL(k in keys(filters) WHERE filters[k] = r[k])
                              %s
                              return s,r,t
                              ''' % (relstring, ' AND '.join(wheres)),
                           **params
                           )
        return Neo4jWrapper(result, self)

    #        return [self._neo2edge(r['r']) for r in result]

    def del_edge(self, edgeid: Union[str, Edge]) -> None:
        """Remove an edge"""
        edgeid = self._edgeid(edgeid)
        result = self._run('''match (s)-[r]->(t) where r._id=$_id delete r''', _id=edgeid)

    def add_node_index(self, name, index):
        pass

    def del_node_index(self, name):
        pass

    def add_edge_index(self, name, index):
        pass

    def del_edge_index(self, name):
        pass

    def commit(self) -> None:
        """Commit the transaction"""
        self.tx.commit()
        self.tx = None

    def rollback(self):
        """Abort the transaction"""
        self.tx.rollback()
        self.tx = None

    def query(self, statement: str, **params: Any) -> ResultWrapper:
        """Direct access to the underlying query language, e.g. cypher"""
        result = self._run(statement, **params)
        return Neo4jWrapper(result, self)

    def traverse(self,
                 labels: Union[Sequence,str] = None,
                 nodes: Union[Sequence,Node] = None,
                 **filters: Any) -> SimpleTraverser:
        """Query for nodes and return a traverser"""
        if labels is None:
            labels = []
        elif type(labels) is str:
            labels = [labels]
        if nodes:
            if type(nodes) != list:
                nodes = [nodes]
        else:
            nodes = self.query_nodes(*labels, **filters).nodes

        return SimpleTraverser(self, nodes)

    def _recursive_replace(self, object: Any) -> Any:
        """Replace neo4j.graph.* by matching Node/Edge"""
        objecttype = type(object)
        if objecttype is neo4j.graph.Node:
            return self._neo2node(object)
        elif objecttype in [list, tuple, neo4j.graph.Path]:
            return [self._recursive_replace(o) for o in object]
        elif objecttype is neo4j.graph.Relationship or hasattr(object, 'start_node'):  # neo4j, I love you:
            return self._neo2edge(object)
        elif hasattr(object, 'keys'):
            return {k: self._recursive_replace(object[k]) for k in object.keys()}
        else:
            return object

    def _fix_ids(self):
        pass

    @property
    def schemahandler(self) -> Schemahandler:
        """Return a Schemahandler with self"""
        return Schemahandler(self)

    def _update_propdict(self):  # 00_caching maybe better db.propdict? How do we proper cache this?
        """Updates the dict of available propertynodes"""
        self.propdict = {p['_propname']: p for p in self.schemahandler.propertynodes}


class Neo4jWrapper(ResultWrapper):
    """A ResultWrapper for neo4j results"""

    def _prepare(self) -> None:
        """Replaces neo4j.graph.* by the respective Node/Edge in the result"""
        for r in self.result:
            self.rows.append(self.db._recursive_replace(r))
        graph = self.result.graph()
        self.nodes = [self.db._recursive_replace(n) for n in graph.nodes]
        self.edges = [self.db._recursive_replace(e) for e in graph.relationships]


if __name__ == "__main__":
    db = NeoGraphDB()
    n = db.add_node('Test', foo='bar')
    print(n)
    print(n.labels)
