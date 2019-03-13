def match_trusted_collaborators(tx, originid):
    return tx.run('''MATCH
    p=(a:User{user_id:$userid})-[:WORKED_ON]->(proj1)<-[:WORKED_ON]-(b:User)-[:WORKED_ON]->(proj2)<-[:WORKED_ON]-(c)
    RETURN a,b,c ''', user_id=originid).data()
def find_trusted_collaborators(originid):
    with driver.session() as session:
        return session.write_transaction(match_trusted_collaborators, originid)
