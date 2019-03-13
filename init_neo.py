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

def parse_user_csv(session):
    with open('Data/user.csv', newline='') as usercsv:
        userreader = csv.reader(usercsv, delimiter=',', quotechar='|')
        for row in userreader:
            if row[0] != 'User_id':
                #print(row)
                print(session.write_transaction(create_user_node,row[0], row[1], row[2]))

#Org Functions
def clear_orgs(tx):
    return tx.run("MATCH (n:Organization) DETACH DELETE n").data()

def create_org_node(tx, name, orgtype):
    curr_org_check = tx.run("MATCH (a:Organization {name: $name, org_type:$orgtype}) RETURN id(a)", name=name, orgtype=orgtype).data()
    if len(curr_org_check) > 0: return curr_org_check
    return tx.run("CREATE (a:Organization {name: $name, org_type:$orgtype})", name=name, orgtype=orgtype).data()

def create_org_user_rel(tx, userid, name, orgtype):
    return tx.run('''MATCH (a:Organization {name: $name, org_type:$orgtype}), (b:User {user_id:$userid})
    CREATE (a)<-[:WORKS_FOR]-(b)
    RETURN id(a), id(b)''', userid=userid, name=name, orgtype=orgtype).data()

def create_dist_rel(tx, org1, org2, dist):
    return tx.run('''MATCH (a:Organization {name: $org1}), (b:Organization {name: $org2})
    CREATE (a)-[:DISTANCE{distance: $dist}]->(b)
    RETURN id(a), id(b)''', org1=org1, org2=org2, dist=float(dist)).data()

def print_orgs(tx):
    return tx.run("MATCH (a:Organization) RETURN a").data()

def parse_org_csv(session):
    with open('Data/organization.csv', newline='') as orgcsv:
        orgreader = csv.reader(orgcsv, delimiter=',', quotechar='|')
        for row in orgreader:
            if row[0] != 'User_id':
                print(row)
                print(session.write_transaction(create_org_node, row[1], row[2]))
                print(session.write_transaction(create_org_user_rel, row[0], row[1], row[2]))

def parse_dist_csv(session):
    with open('Data/distance.csv', newline='') as distcsv:
        orgreader = csv.reader(distcsv, delimiter=',', quotechar='|')
        for row in orgreader:
            if row[2] != 'Distance':
                print(row)
                print(session.write_transaction(create_dist_rel, row[0], row[1], row[2]))

#Proj Functions
def clear_projs(tx):
    return tx.run("MATCH (n:Project) DETACH DELETE n").data()

def create_proj_node(tx,project):
    curr_proj_check = tx.run("MATCH (a:Project {project:$project}) RETURN id(a)", project=project).data()
    if len(curr_proj_check) > 0: return curr_proj_check
    return tx.run("CREATE (a:Project {project:$project})", project=project).data()

def create_proj_user_rel(tx, userid, project):
    return tx.run('''MATCH (a:Project {project: $project}), (b:User {user_id:$userid})
    CREATE (a)<-[:WORKED_ON]-(b)
    RETURN id(a), id(b)''', userid=userid, project=project).data()

def parse_proj_csv(session):
    with open('Data/project.csv', newline='') as projcsv:
        orgreader = csv.reader(projcsv, delimiter=',', quotechar='|')
        for row in orgreader:
            if row[1] != 'Project':
                print(row)
                print(session.write_transaction(create_proj_node, row[1]))
                print(session.write_transaction(create_proj_user_rel, row[0], row[1]))

def init_neo():
    with driver.session() as session:
        cleared = session.write_transaction(clear_users)
        #print(cleared)
        wrote = session.write_transaction(clear_orgs)
        #print(wrote)
        parse_user_csv(session)
        parse_org_csv(session)
        parse_dist_csv(session)
        parse_proj_csv(session)
        #print session.write_transaction(create_user_node,'Noam')
        #print(session.read_transaction(print_users))
        #print(session.read_transaction(print_orgs))

'''
Find:
- Users
- University Users
- Organizations
- Projects
'''

def match_users(session):
    pass

def match_uni_users(session):
    pass

def match_orgs(session):
    pass

def match_projs(session):
    pass

def match_uni_connect_users(tx, originid):
    return tx.run('''MATCH
    p=(a:User{user_id: $userid})-[:WORKS_FOR]->(b:Organization{org_type:'U'})-[:DISTANCE*]->(c)<-[:WORKS_FOR]-(d)
    WITH *,relationships(p) AS f
    WITH *,[n in f WHERE n.distance IS NOT NULL] as noNull
    WITH *, reduce(totalDist = 0, n in noNull|totalDist + n.distance) as totalDist
    RETURN a,b,totalDist,c,d ORDER BY totalDist''', userid=originid).data()

def find_uni_connect_users(originid):
    with driver.session() as session:
        return session.write_transaction(match_uni_connect_users, originid)
