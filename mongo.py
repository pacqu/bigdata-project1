from pymongo import MongoClient
client = MongoClient()
db = client.test_database

def find_trusted_collaborators_interests(origin_id, userids, desired_interests):
    final_results = {}
    users = db.users
    o_user = users.find_one({"user_id":origin_id})
    final_results['o_user'] = o_user
    find_interests_fields = {"user_id": {"$in" : userids }}
    if len(desired_interests) > 0:
        find_interests_fields["$or"] = []
    for interest in desired_interests:
        find_interests_fields["$or"].append({"interests." + interest : { "$exists" : True }})
    pp = users.find(find_interests_fields)
    final_results['trusted'] = list(pp)
    return final_results

def find_common_uni_skill_interest(origin_id, userids):
    final_results = {}
    #Retrieving from User Collection
    users = db.users

    #Finding Origin User So we Can Retrieve their skills and interests
    users_skills_interests = users.find_one({"user_id":origin_id})

    #Extrating Skills/Interests Data from User results
    origin_skills = users_skills_interests['skills']
    origin_interests = users_skills_interests['interests']

    #Appending Skills/Interest and weights to final results
    final_results['origin_skills'] = origin_skills
    final_results['origin_interests'] = origin_interests

    #Processing Skills/Interests Data from Mongo to create flat lists of skills/interests
    origin_skills_list = {k for d in origin_skills for k in d.keys()}
    origin_interests_list = {k for d in origin_interests for k in d.keys()}

    #Initiailizing arrays/objects that will be used for ultimately getting appropriate users_skills
    #Match query object for getting initial list of users in provide ids that share origin's interests/skills
    find_skills_interests_fields = {"user_id": {"$in" : userids }}
    #Lists that will ultimately enable addition of the weights of skills/interests in common
    origin_skills_zero = []
    origin_interests_zero = []
    #Object that will indicate which user fields to include in final results
    project_fields = {
    'user_id': 1, 'first_name': 1, 'last_name': 1
    }

    if (len(origin_skills_list) > 0) or (len(origin_interests_list) > 0):
        find_skills_interests_fields["$or"] = []

    for skill in origin_skills_list:
        #If a user has this skill in common with origin, it will be included in results
        find_skills_interests_fields["$or"].append({"skills." + skill : { "$exists" : True }})
        #If this skill in common with origin exists, it's value will be added to Skill Match Score
        #If skill doesn't exist for user, it will be represented as 0
        origin_skills_zero.append({ "$ifNull" : [{'$arrayElemAt' : ["$skills." + skill , 0 ]}, 0]})
        #If this skill in common with origin exists, it will be included in final results
        project_fields['skills.' + skill] = 1

    #Repeat actions acted on skills list with interest lists
    for interest in origin_interests_list:
        find_skills_interests_fields["$or"].append({"interests." + interest : { "$exists" : True }})
        origin_interests_zero.append({ "$ifNull" : [{'$arrayElemAt' : ["$interests." + interest , 0 ]}, 0]})
        project_fields['interests.' + interest] = 1

    #Skill/Interest Match Scores now to be included in final results
    project_fields['totalSkillMatch'] = {'$add' : origin_skills_zero }
    project_fields['totalInterestMatch'] = {'$add' : origin_interests_zero }

    #Users that have common skills/interests with origin is now queried for
    #Along with Skill/Interest/Total Matching Scores with Origin for each user
    ppm=users.aggregate([
    {'$match': find_skills_interests_fields},
    {'$project': project_fields},
    {'$addFields': {'totalMatch' : {'$add': ['$totalSkillMatch', '$totalInterestMatch']}} },
    {'$sort': {'totalMatch':-1}}
    ])
    final_results['common_users'] = list(ppm)
    return final_results

def find_user(user_id):
    users = db.users
    return users.find_one({"user_id":user_id})
def find_org(org_name):
    orgs = db.organizations
    return orgs.find_one({"organization":org_name})
