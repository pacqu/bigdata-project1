from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

def match_user(tx, originid):
    user = tx.run('''MATCH (o_user:User{user_id: $userid})-[:WORKS_FOR]->(o_org:Organization)
    RETURN o_user,o_org''',userid=originid).data()
    #print(user)
    if len(user) > 0:
        return user
    else:
        return []

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
