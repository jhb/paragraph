from neo4j import GraphDatabase
from uuid import uuid4
from paragraph.interfaces import GraphDB, Node, Edge


class NeoGraphDB(GraphDB):

    def __init__(self, uri='bolt://localhost:7687', username='', password='', encrypted=False):
        self.driver = GraphDatabase.driver(uri,auth=(username,password),encrypted=encrypted)
        self.session = self.driver.session()
        self.tx = None

    def begin(self):
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

    def add_node(self, *labels, **properties):
        if '_id' not in properties:
            properties['_id']=self._new_uid()
        labelstring = ':'.join([str(l) for l in labels])
        if labelstring:
            labelstring = ':'+labelstring
        result = self._run(f'create (n{labelstring}) set n = $props return n', props=properties)
        return self._neo2node(result.single()['n'])

    def update_node(self, node: Node):
        pass

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