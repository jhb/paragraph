from paragraph import signals

class Schemahandler:

    def __init__(self,db):
        self.db = db
        self.default_values = dict(string='',int=0)

    @property
    def propertynodes(self):
        return sorted(self.db.query_nodes('_Property').nodes, key=lambda x: x.get('_propname',''))

    @property
    def schemanodes(self):
        return sorted(self.db.query_nodes('_Schema').nodes, key=lambda x: x.get('_schemaname', ''))



    @property
    def schemanames(self):
        return [n.get('_schemaname') for n in self.schemanodes]

    def apply_to_node(self,schemaname,node):
        candidates = self.db.query_nodes(_schemaname=schemaname).nodes
        if len(candidates) != 1:
            raise Exception('Wrong schema selection')
        schema = candidates[0]
        node.labels.add(schema['_schemaname'])
        for propertynode in schema.oN('_PROP', _arity='1').nodes:
            fieldtype = propertynode['_fieldtype']
            name = propertynode['_propname']
            if name not in node:
                node[name]=self.default_values.get(fieldtype,'')

    def find_schemata(self,node):
        schemata = set()
        nodeprops = set(node.keys())
        for schemanode in self.schemanodes:
            schemaprops = set([pn['_propname'] for pn in schemanode.oN('_PROP', _arity='1').nodes])
            if schemaprops and schemaprops.issubset(nodeprops):
                schemata.add(schemanode)
        return schemata

    def property_description(self, propertyname):
        pn = self.propertynodes
        for p in pn:
            if p['_propname'] == propertyname:
                return p['description']
        return ''

    def filter_labels(self, labels :set, properties: dict):
        schemanames = set(self.schemanames)
        to_remove = schemanames & labels
        for label in to_remove:
            labels.remove(label)
        labels.update([s['_schemaname'] for s in self.find_schemata(properties)])
        return labels

@signals.before_label_store.connect
def filter_schema_labels(db,labels :set, properties : dict):
    sh = Schemahandler(db)
    sh.filter_labels(labels, properties)

# node.labels[] = set(node.userlabels) | set(node.schemata) Sekunde, batterie alle
# schema definieren namensraum für labels, der nicht durch Nutzer vergeben werden kann.