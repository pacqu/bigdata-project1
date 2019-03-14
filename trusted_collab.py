def match_trusted_collaborators(tx, originid):
    return tx.run('''MATCH
    (a:User{user_id:$userid})-[:WORKED_ON]->(p:Project)<-[:WORKED_ON]-(b:User)-[:WORKED_ON]->(p2:Project)<-[:WORKED_ON]-(c)
    RETURN a,b,c ''', userid=originid).data()
def find_trusted_collaborators(originid):
    with driver.session() as session:
        trusted = session.write_transaction(match_trusted_collaborators, originid)
        print(trusted)

def find_trusted_collaborators_skills(userids):
    for userid in userids:
        pprint.pprint(skills.find_one({user_id:$userid}))
