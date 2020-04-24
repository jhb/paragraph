DB backends
===========
* Neo4j
* ZODB
* SQLite

DB Abstraction
==============
* add/update/delete node
* add/update/delete edge
* traverse - multiple hops
    * gremlin like interface
* create/remove indexes
* interface to networkx (import/export)


Schema and behaviour
====================
* Properties
* ComputedProperties? Adapters?
* Schema composed out of properties
  * Assigned to node
  * Observed on node
* Interactions with sets/lists of nodes

Events
======
* Eventsystem

Structure and permissions
=========================
* Tree structures (e.g. for location, permission etc.)
  * Edgetypes
  * Root node
  * child_of relations
* Content is related to nodes within those trees
* Security inherited down the tree


UI Interactions
===============
* Inspecting nodes
* Arranging nodes
  * Multiple perspective nodes
* Inspecting edges
* Adding nodes and edges
* Connecting two nodes
* Adding a connected node
* Removing a node or edge
* Multi-selecting nodes
  * arranging nodes

* Mapping of structured data into the graph (wikipedia, musicbrainz,...)
* Display of collections

