import csv
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

#User Functions
def clear_users(tx):
    return tx.run("MATCH (n:User) DETACH DELETE n").data()

def create_user_node(tx, userid, firstname, lastname):
    return tx.run("CREATE (a:User {first_name: $firstname, last_name:$lastname, user_id:$userid}) RETURN id(a)", firstname=firstname, lastname=lastname, userid=userid).data()

def print_users(tx):
    return tx.run("MATCH (a:User) RETURN a").data()

def parse_user_csv():
    with open('Data/user.csv', 'rb') as usercsv:
        userreader = csv.reader(usercsv, delimiter=',', quotechar='|')
        for row in userreader:
            if row[0] != 'User_id':
                print(row)
            print(session.write_transaction(create_user_node,row[0], row[1], row[2]))

#Org Functions
def clear_orgs(tx):
    return tx.run("MATCH (n:Organization) DETACH DELETE n").data()

def create_org_node(tx, orgid, firstname, lastname):
    return tx.run("CREATE (a:Organization {name: $firstname, last_name:$lastname, org_id:$orgid}) RETURN id(a)", firstname=firstname, lastname=lastname, orgid=orgid).data()

def print_orgs(tx):
    return tx.run("MATCH (a:Organization) RETURN a").data()

def parse_org_csv():
    with open('Data/org.csv', 'rb') as orgcsv:
        orgreader = csv.reader(orgcsv, delimiter=',', quotechar='|')
        for row in orgreader:
            if row[0] != 'Organization_id':
                print(row)
            print(session.write_transaction(create_org_node,row[0], row[1], row[2]))

with driver.session() as session:
    print(session.write_transaction(clear_orgs))
    parse_user_csv()
    #print session.write_transaction(create_user_node,'Noam')
    print(session.read_transaction(print_users))
