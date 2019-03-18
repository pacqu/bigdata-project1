import csv
from neo4j import GraphDatabase
from itertools import islice

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

#User Functions
def clear_users(tx):
    return tx.run("MATCH (n:User) DETACH DELETE n").data()

def create_user_node(tx, userid, firstname, lastname):
    return tx.run("CREATE (a:User {first_name: $firstname, last_name:$lastname, user_id:$userid}) RETURN id(a)", firstname=firstname, lastname=lastname, userid=userid).data()

def print_users(tx):
    return tx.run("MATCH (a:User) RETURN a").data()

def parse_user_csv(session, user_input_csv):
    with open(user_input_csv, newline='') as usercsv:
        userreader = csv.reader(usercsv, delimiter=',', quotechar='|')
        for row in userreader:
            if row[0] != 'User_id':
                # print(row)
                user = session.write_transaction(create_user_node,int(row[0]), row[1], row[2])
                #print(user)

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

def parse_org_csv(session, org_input_csv):
    with open(org_input_csv, newline='') as orgcsv:
        orgreader = csv.reader(orgcsv, delimiter=',', quotechar='|')
        for row in orgreader:
            if row[0] != 'User_id':
                # print(row)
                org = session.write_transaction(create_org_node, row[1], row[2])
                # print(org)
                rel = session.write_transaction(create_org_user_rel, int(row[0]), row[1], row[2])
                # print(rel)

def parse_dist_csv(session, dist_input_csv):
    with open(dist_input_csv, newline='') as distcsv:
        orgreader = csv.reader(distcsv, delimiter=',', quotechar='|')
        for row in orgreader:
            if row[2] != 'Distance':
                #print(row)
                dist = session.write_transaction(create_dist_rel, row[0], row[1], row[2])
                #print dist

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

def parse_proj_csv(session, proj_input_csv):
    with open(proj_input_csv, newline='') as projcsv:
        orgreader = csv.reader(projcsv, delimiter=',', quotechar='|')
        for row in orgreader:
            if row[1] != 'Project':
                # print(row)
                proj = session.write_transaction(create_proj_node, row[1])
                #print(proj)
                rel = session.write_transaction(create_proj_user_rel, int(row[0]), row[1])
                #print(rel)

def clear_neo():
    with driver.session() as session:
        cleared = session.write_transaction(clear_users)

def init_neo(*arg):
    # print('neo', arg)
    # arg order: user, org, dist, proj
    with driver.session() as session:
        cleared = session.write_transaction(clear_users)
        #print(cleared)
        wrote = session.write_transaction(clear_orgs)
        #print(wrote)
        parse_user_csv(session, arg[0])
        parse_org_csv(session, arg[1])
        parse_dist_csv(session, arg[2])
        parse_proj_csv(session, arg[3])
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

def match_user(tx, originid):
    user = tx.run('''MATCH (o_user:User{user_id: $userid})-[:WORKS_FOR]->(o_org:Organization)
    RETURN o_user,o_org''',userid=originid).data()
    #print(user)
    if len(user) > 0:
        return user
    else:
        return []

def match_users(tx):
    pass

def match_uni_users(tx):
    pass

def match_orgs(tx):
    pass

def match_projs(tx):
    pass

def match_uni_connect_users(tx, originid):
    return tx.run('''MATCH
    p=(o_user:User{user_id: $userid})-[:WORKS_FOR]->(o_org:Organization{org_type:'U'})-[:DISTANCE*]-(d_org)<-[:WORKS_FOR]-(d_user)
    WITH *,relationships(p) AS f
    WITH *,[n in f WHERE n.distance IS NOT NULL] as noNull
    WITH *, reduce(totalDist = 0, n in noNull|totalDist + n.distance) as totalDist
    WHERE totalDist <= 10
    RETURN DISTINCT o_user,o_org,
    CASE
    WHEN o_org.name = d_org.name
    THEN 0
    ELSE totalDist
    END AS totalDist,
    d_org,d_user ORDER BY totalDist''',userid=originid).data()

#MIGHT NOT BE NECESSARY, WORKS FOR READABILITY OF OUTPUT
def find_uni_connect_users(originid):
    results = {}
    connected_users = {}
    connected_ids = []
    with driver.session() as session:
        connections = session.write_transaction(match_uni_connect_users, originid)
        if len(connections) > 0:
            connection = connections[0]
            results['o_user'] = {
            'first_name': connection['o_user']['first_name'],
            'last_name': connection['o_user']['last_name'],
            'org': {
            'name': connection['o_org']['name'],
            'org_type': connection['o_org']['org_type']
            }
            }
        else:
            origin = session.write_transaction(match_user, originid)
            if len(origin) > 0:
                origin = origin[0]
                results['o_user'] = {
                'first_name': origin['o_user']['first_name'],
                'last_name': origin['o_user']['last_name'],
                'org': {
                'name': origin['o_org']['name'],
                'org_type': origin['o_org']['org_type'],
                }
                }
        for connection in connections:
            if connection['d_user']['user_id'] in connected_users:
                continue
            connected_users[connection['d_user']['user_id']] = {
            'first_name': connection['d_user']['first_name'],
            'last_name': connection['d_user']['last_name'],
            'org': {
            'name': connection['d_org']['name'],
            'org_type': connection['d_org']['org_type']
            },
            'total_dist': connection['totalDist']
            }
            connected_ids.append(connection['d_user']['user_id'])
    results['connected_users'] = connected_users
    results['connected_ids'] = connected_ids
    return results


# u = find_uni_connect_users('1')
# for i in u:
#     if i == 'connections':
#         print('Connections:')
#         for j in u[i]:
#             print(j + ': ' +str(u[i][j]))
#     else:
#         print(i + ': '+ str(u[i]))

# (a:User{user_id:$userid})-[:WORKED_ON]->(proj1)<-[:WORKED_ON]-(b:User)-[:WORKED_ON]->(proj2)<-[:WORKED_ON]-(c)
def match_trusted_collaborators(tx, originid):
    return tx.run('''MATCH
    (a:User{user_id:$userid})-[:WORKED_ON]->(p:Project)<-[:WORKED_ON]-(b:User)-[:WORKED_ON]->(p2:Project)<-[:WORKED_ON]-(c)
    RETURN a,b,c''', userid=originid).data()

def find_trusted_collaborators(originid):
    final_results = {}
    with driver.session() as session:
        trusted = session.write_transaction(match_trusted_collaborators, originid)
        final_results['results'] = trusted
        userids = []
        common_trust = {}
        for trust in trusted:
            userids.append(trust['c']['user_id'])
            if trust['c']['user_id'] not in common_trust:
                common_trust[trust['c']['user_id']] = []
            common_trust[trust['c']['user_id']].append(trust['b']['first_name'] + ' ' + trust['b']['last_name'])
        final_results['ids'] = list(set(userids))
        final_results['common_trust'] = common_trust
        return final_results
