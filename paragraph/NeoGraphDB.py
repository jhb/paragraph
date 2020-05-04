"""Database driver for neo4j"""
import logging
from uuid import uuid4

from neo4j import GraphDatabase

from paragraph.interfaces import GraphDB, Node, Edge


class NeoGraphDB(GraphDB):

    def __init__(self, uri='bolt://localhost:7687', username='', password='', encrypted=False, debug=0):
        """
        Initialize the database connection

        :param uri:
        :param username:
        :param password:
        :param encrypted:
        """
        self.driver = GraphDatabase.driver(uri, auth=(username, password), encrypted=encrypted)
        self.session = self.driver.session()
        self.tx = None
        self.debug = debug

    def begin(self):
        """Begin a transaction

        :return transaction
        """
        if not self.tx:
            self.tx = self.session.begin_transaction()
        return self.tx

    def _run(self, statement, **kwargs):
        tx = self.begin()
        if self.debug:  #
            logging.debug(f'{statement} {kwargs}')  # @@_todo
        return tx.run(statement, **kwargs)

    def _neo2node(self, neonode):
        node = Node()
        node.update(neonode)
        node._labels.update(neonode.labels)
        return node

    def _new_uid(self):
        return uuid4().hex

    def _labels2string(self, labels):
        labelstring = ':'.join([str(l) for l in labels])
        if labelstring:
            labelstring = ':' + labelstring
        return labelstring

    def add_node(self, *labels, **properties):
        if '_id' not in properties:
            properties['_id'] = self._new_uid()
        labelstring = self._labels2string(labels)
        result = self._run(f'create (n{labelstring}) set n = $props return n', props=properties)
        return self._neo2node(result.single()['n'])

    def update_node(self, node: Node):
        labelstring = self._labels2string(node._labels)
        if labelstring:
            labelstring = 'set n' + labelstring
        props = {k: v for k, v in node.items() if k not in ['_labels']}
        result = self._run(f'match (n) where n._id=$_id {labelstring} set n=$props return n',
                           labelstring=labelstring,
                           _id=node['_id'],
                           props=props)
        return self._neo2node(result.single()['n'])

    def del_node(self, _id, detach=False):
        if detach:
            result = self._run("match (n) where n._id=$_id detach delete n", _id=_id)
        else:
            result = self._run("match (n) where n._id=$_id delete n", _id=_id)

    def add_edge(self, source, reltype, target, **properties):
        pass

    def update_edge(self, edge: Edge):
        pass

    def del_edge(self, edgeid):
        pass

    def add_node_index(self, name, index):
        pass

    def del_node_index(self, name):
        pass

    def query_nodes(self, **filters):
        result = self._run('''WITH $filters as filters 
                              MATCH (n) WHERE ALL(k in keys(filters) WHERE filters[k] = n[k])
                              return n''',
                           filters=filters)
        return [self._neo2node(r['n']) for r in result]

    def add_edge_index(self, name, index):
        pass

    def del_edge_index(self, name):
        pass

    def query_edge(self, **filters):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def query(self, query):
        pass


if __name__ == "__main__":
    db = NeoGraphDB()
    n = db.add_node('Test', foo='bar')
    print(n)
    print(n.labels)
