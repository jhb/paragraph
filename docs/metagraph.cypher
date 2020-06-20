
CREATE
(_schema:_Schema {description:'the meta schema to label schemas',_id:'def1',_schemaname:'_Schema',_techname:'_Schema', graph:'metagraph'}),
(_description:_Property {description:'longer description',_field:'StringField',_id:'def2',_techname:'description', graph:'metagraph'}),
(_techname:_Property {description:'internal scalar representation',_field:'StringField',_id:'def3',_techname:'_techname', graph:'metagraph'}),
(_prop:_Relation {description:'_Schema --_PROP-> _Property',_targetarity:'*',_id:'def5',_sourcearity:'*',_techname:'_PROP', graph:'metagraph'}),
(_arity:_Property {description:'How often can there be the element',_field:'StringField',_id:'def7',_techname:'_arity', graph:'metagraph'}),
(_relation:_Schema {description:'used to define a type of relation',_id:'def8',_schemaname:'_Relation',_techname:'_Relation', graph:'metagraph'}),
(_property:_Schema {description:'A description of  property of semantic meta object',_id:'def9',_schemaname:'_Property',_techname:'_Property', graph:'metagraph'}),
(_field:_Property {description:'Von welchem Typ ist der Wert',_field:'StringField',_id:'def10',_techname:'_field', graph:'metagraph'}),
(_name:_Property {description:'full name of  thing',_field:'StringField',_id:'def11',_techname:'name', graph:'metagraph'}),
(_person:_Schema {description:'a human',_id:'def12',_schemaname:'Person',_techname:'Person', graph:'metagraph'}),
(_firstname:_Property {description:'first name of a person',_field:'StringField',_id:'def13',_techname:'firstname', graph:'metagraph'}),
(_lastname:_Property {description:'last name of a person',_field:'StringField',_id:'def14',_techname:'lastname', graph:'metagraph'}),
(_likes:_Relation {description:'xoxoxo',_targetarity:'1',_id:'def15',_sourcearity:'?',_techname:'LIKES', graph:'metagraph'}),
(_bob:Person {name:'Bob',firstname:'',_id:'def16',lastname:'', graph:'metagraph'}),
(_alice:Person {name:'Alice Alison',firstname:'Alice',_id:'def17',lastname:'Alison', graph:'metagraph'}),
(_schemaname:_Property {description:'the name of a schema',_field:'StringField',_id:'def18',_techname:'_schemaname', graph:'metagraph'}),
(_sourcearity:_Property {description:'_arity of start',_field:'StringField',_id:'def19',_techname:'_sourcearity', graph:'metagraph'}),
(_targetarity:_Property {description:'_arity of target',_field:'StringField',_id:'def20',_techname:'_targetarity', graph:'metagraph'}),
(_source:_Relation {description:'schema for the start of relation',_targetarity:'*',_id:'def21',_sourcearity:'*',_techname:'_SOURCE', graph:'metagraph'}),
(_target:_Relation {description:'schema for the start of relation',_targetarity:'*',_id:'def22',_sourcearity:'*',_techname:'_TARGET', graph:'metagraph'}),
(_schema)-[:_PROP {_id:'def22',_arity:'1', graph:'metagraph'}]->(_description),
(_schema)-[:_PROP {_id:'def23',_arity:'1', graph:'metagraph'}]->(_techname),
(_schema)-[:_SOURCE {_id:'def24', graph:'metagraph'}]->(_prop),
(_schema)-[:_PROP {_id:'def25',_arity:'1', graph:'metagraph'}]->(_schemaname),
(_prop)-[:_PROP {_id:'def26',_arity:'1', graph:'metagraph'}]->(_arity),
(_relation)-[:_PROP {_id:'def27',_arity:'1', graph:'metagraph'}]->(_techname),
(_relation)-[:_PROP {_id:'def28',_arity:'1', graph:'metagraph'}]->(_description),
(_relation)-[:_PROP {_id:'def30',_arity:'*', graph:'metagraph'}]->(_sourcearity),
(_relation)-[:_PROP {_id:'def31',_arity:'*', graph:'metagraph'}]->(_targetarity),
(_property)-[:_PROP {_id:'def32',_arity:'1', graph:'metagraph'}]->(_field),
(_property)-[:_PROP {_id:'def33',_arity:'1', graph:'metagraph'}]->(_description),
(_property)-[:_PROP {_id:'def34',_arity:'1', graph:'metagraph'}]->(_techname),
(_prop)-[:_TARGET {_id:'def35', graph:'metagraph'}]->(_property),
(_person)-[:_PROP {_id:'def36',_arity:'?', graph:'metagraph'}]->(_lastname),
(_person)-[:_PROP {_id:'def37',_arity:'?', graph:'metagraph'}]->(_firstname),
(_person)-[:_PROP {_id:'def38',_arity:'1', graph:'metagraph'}]->(_name),
(_person)-[:_SOURCE {_id:'def39', graph:'metagraph'}]->(_likes),
(_likes)-[:_TARGET {_id:'def40', graph:'metagraph'}]->(_person),
(_relation)-[:_SOURCE {_id:'def41', graph:'metagraph'}]->(_source),
(_source)-[:_TARGET {_id:'def42', graph:'metagraph'}]->(_schema),
(_relation)-[:_SOURCE {_id:'def43', graph:'metagraph'}]->(_target),
(_target)-[:_TARGET {_id:'def44', graph:'metagraph'}]->(_schema),
(_alice)-[:LIKES {_id:'def45', graph:'metagraph'}]->(_bob),
(_bob)-[:LIKES {_id:'def46', graph:'metagraph'}]->(_alice);