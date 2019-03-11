from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

'''def add_person(driver, name):
    with driver.session() as session:
        # Caller for transactional unit of work
        return session.write_transaction(create_person_node, name)'''

def clear_db(tx):
    return tx.run("MATCH (n:Person) DETACH DELETE n").data()

def create_person_node(tx, name):
    return tx.run("CREATE (a:Person {name: $name}) RETURN id(a)", name=name).data()

def print_persons(tx):
    return tx.run("MATCH (a:Person) RETURN a").data()


with driver.session() as session:
    print session.write_transaction(clear_db)
    print session.write_transaction(create_person_node,'Noam')
    print session.read_transaction(print_persons)
