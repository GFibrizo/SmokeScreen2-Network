import pyorient

USER = "root"
PASS = "root"
SERVER = "localhost"
PORT = 2424

class SemanticNetwork(object):

    def __init__ (self,networkFile):
        self.db_name = ""
        self.client = pyorient.OrientDB(SERVER, PORT)
        self.client.connect(USER,PASS)

        with open(networkFile) as file:
            self.db_name = file.readline().rstrip();
            self.client.db_create(self.db_name, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY)

            self.client.command('create class Concepts extends V')

            for line in file:
                concept1,concept2,relationship = line.split(",")

                self.add_relationship(concept1,concept2,relationship)

    def destroy_network(self):
        self.client.db_drop(self.db_name)


    def add_concept(self,concept):
        matches = self.client.command("select from Concepts where name = '"+concept+"'")
        if matches:
            return
        self.client.command("insert into Concepts set name = '"+concept+"'")

    def add_relationship(self,concept1,concept2,relationship):
        relationship = "_".join(relationship.split())

        self.add_concept(concept1)
        self.add_concept(concept2)

        try:
            self.client.command("create class "+relationship+" extends E")
        except Exception as e:
            pass

        self.client.command("create edge "+relationship+" from ( select from Concepts where name = '"+concept1+"') to (select from Concepts where name = '"+concept2+"')")

    def search_related_concepts(self,relationship,concept):
        relationship = "_".join(relationship.split())
        concepts = [ concept.name for concept in self.client.command("select expand( in( "+relationship+" )) from Concepts where name='"+concept+"'")
        return concepts
