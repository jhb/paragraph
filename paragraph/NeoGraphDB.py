"""
Database connector for Neo4j

>>> db = NeoGraphDB()

Create a node
>>> n = db.add_node('Testlabel', foo='bar')
>>> pprint(n) # doctest: +ELLIPSIS
{'foo': 'bar', '_id': '...'}
>>> n.labels
{'Testlabel'}

Upate the node
>>> n['foo2']='bar2'
>>> n.labels.add('Testlabel2')
>>> pprint(db.update_node(n))  # doctest: +ELLIPSIS
{'foo2': 'bar2', 'foo': 'bar', '_id': '...'}
"""

from pprint import pprint
from neo4j import GraphDatabase
from uuid import uuid4
from paragraph.interfaces import GraphDB, Node, Edge


class NeoGraphDB(GraphDB):

    def __init__(self, uri='bolt://localhost:7687', username='', password='', encrypted=False):
        """
        Initialize the database connection

        :param uri:
        :param username:
        :param password:
        :param encrypted:
        """
        self.driver = GraphDatabase.driver(uri,auth=(username,password),encrypted=encrypted)
        self.session = self.driver.session()
        self.tx = None

    def begin(self):
        """Begin a transaction

        :return transaction
        """
        if not self.tx:
            self.tx = self.session.begin_transaction()
        return self.tx

    def _run(self,statement,**kwargs):
        tx = self.begin()
        return tx.run(statement,**kwargs)

    def _neo2node(self,neonode):
        node = Node()
        node.update(neonode)
        node.labels = set(neonode.labels)
        return node

    def _new_uid(self):
        return uuid4().hex

    def _labels2string(self,labels):
        labelstring = ':'.join([str(l) for l in labels])
        if labelstring:
            labelstring = ':' + labelstring
        return labelstring

    def add_node(self, *labels, **properties):
        if '_id' not in properties:
            properties['_id']=self._new_uid()
        labelstring = self._labels2string(labels)
        result = self._run(f'create (n{labelstring}) set n = $props return n', props=properties)
        return self._neo2node(result.single()['n'])

    def update_node(self, node: Node):
        labelstring = self._labels2string(node.labels)
        if labelstring:
            labelstring = 'set n'+labelstring
        result = self._run(f'match (n) where n._id=$_id {labelstring} set n=$props return n',
                           labelstring=labelstring,
                           _id=node['_id'],
                           props=dict(node.items()))
        return self._neo2node(result.single()['n'])


    def del_node(self, _id):
        pass

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

    def query_node(self, **filters):
        pass

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
    n = db.add_node('Test',foo='bar')
    print(n)
    print(n.labels)