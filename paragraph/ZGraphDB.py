from paragraph.basic import GraphDB

class ZGraphDB(GraphDB):

    def __init__(self):
        self.foo='x'


z = ZGraphDB()
print(z.foo)
