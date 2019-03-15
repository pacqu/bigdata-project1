import csv
import pprint
from pymongo import MongoClient
client = MongoClient()


db = client.test_database
client.drop_database(db)

def initUser():
    users = db.users
    with open('Data/user.csv') as usercsv:
        usercsv.readline()
        user_reader = csv.reader(usercsv, delimiter=',', quotechar='|')
        for row in user_reader:
            user = {"user_id": int(row[0]),
                    "first_name": row[1],
                    "last_name": row[2]
                    }
            users_id = users.insert_one(user).inserted_id

def initSkill():
    users = db.users
    users_skills = {}
    with open('Data/skill.csv') as skillcsv:
        skillcsv.readline() # skip first row
        skill_reader = csv.reader(skillcsv, delimiter=',', quotechar='|')
        for row in skill_reader:
            if row[0] in users_skills: #row[0] is user_id
                users_skills[row[0]].append({row[1]:int(row[2])})
            else:
                users_skills[row[0]]=[{row[1]:int(row[2])}]
        # Adds the skills from the dict to MongoDB
        for user_id in users_skills:
            users.update_one({'user_id':int(user_id)},
                         {'$set':{'skills':users_skills[user_id]}})

def initProject():
    projects = db.projects
    with open('Data/project.csv') as projectcsv:
        projectcsv.readline() # skip first row
        project_reader = csv.reader(projectcsv, delimiter=',', quotechar='|')
        for row in project_reader:
            project = {"user_id":int(row[0]),
                    "project": row[1],
                    }
            project_id = projects.insert_one(project).inserted_id

def initOrganization():
    organizations = db.organizations
    with open('Data/organization.csv') as organizationcsv:
        organizationcsv.readline() # skip first row
        organization_reader = csv.reader(organizationcsv, delimiter=',', quotechar='|')
        for row in organization_reader:
            organization = {"user_id":int(row[0]),
                            "organization":row[1],
                            "organization_type": row[2]}
            organization_id = organizations.insert_one(organization).inserted_id

def initInterest():
    users = db.users
    users_interests = {}
    interests = db.interests
    with open('Data/interest.csv') as interestcsv:
        interestcsv.readline() # skip first row
        interest_reader = csv.reader(interestcsv, delimiter=',', quotechar='|')
        for row in interest_reader:
            if row[0] in users_interests: #row[0] is user_id
                users_interests[row[0]].append({row[1]:int(row[2])})
            else:
                users_interests[row[0]]=[{row[1]:int(row[2])}]
        # Adds the skills from the dict to MongoDB
        for user_id in users_interests:
            users.update_one({'user_id':int(user_id)},
                         {'$set':{'interests':users_interests[user_id]}})

def initDistance():
    distances = db.distances
    with open('Data/distance.csv') as distancecsv:
        distancecsv.readline()
        distance_reader = csv.reader(distancecsv, delimiter=',', quotechar='|')
        for row in distance_reader:
            distance = {"organization_1":row[0],
                        "organization_2":row[1],
                        "distance": row[2]}
            distance_id = distances.insert_one(distance).inserted_id

# I dont think I need origin_id
def find_trusted_collaborators_skills(origin_id, userids, desired_skill):
    #trusted_collaborators = []
    users = db.users
    pp = users.find({"user_id": {"$in" : userids }, "skills." + desired_skill : { "$exists" : True }})
    '''
    for userid in userids:
        pp = users.find_one({"user_id":userid, "skills." + desired_skill : { "$exists" : True }})
        print(pp)
        for skills in pp['skills']:
            if desired_skill in skills:
                trusted_collaborators.append(userid)'''
    #print(list(pp))
    #print(trusted_collaborators)
    #return trusted_collaborators
    return list(pp)

def find_common_uni_skill_interest(origin_id, userids):
    users = db.users
    users_skills_interests = users.find_one({"user_id":origin_id})
    print(users_skills_interests)
    origin_skills = users_skills_interests['skills']
    origin_skills_list = {k for d in origin_skills for k in d.keys()}

    origin_interests = users_skills_interests['interests']
    origin_interests_list = {k for d in origin_interests for k in d.keys()}

    find_skills_interests_fields = {"user_id": {"$in" : userids }, "$or":[]}
    origin_skills_zero = []
    origin_interests_zero = []
    project_fields = {
    'user_id': 1, 'first_name': 1, 'last_name': 1
    }
    for skill in origin_skills_list:
        find_skills_interests_fields["$or"].append({"skills." + skill : { "$exists" : True }})
        origin_skills_zero.append({ "$ifNull" : [{'$arrayElemAt' : ["$skills." + skill , 0 ]}, 0]})
        project_fields['skills.' + skill] = 1

    for interest in origin_interests_list:
        find_skills_interests_fields["$or"].append({"interests." + interest : { "$exists" : True }})
        origin_interests_zero.append({ "$ifNull" : [{'$arrayElemAt' : ["$interests." + interest , 0 ]}, 0]})
        project_fields['interests.' + interest] = 1

    project_fields['totalSkillMatch'] = {'$add' : origin_skills_zero }
    project_fields['totalInterestMatch'] = {'$add' : origin_interests_zero }

    ppm=users.aggregate([
    {'$match': find_skills_interests_fields},
    {'$project': project_fields},
    {'$addFields': {'totalMatch' : {'$add': ['$totalSkillMatch', '$totalInterestMatch']}} },
    {'$sort': {'totalMatch':-1}}
    ])
    return list(ppm)



def init_mongo():
    initUser()
    initSkill()
    initInterest()
    initOrganization()
    initProject()
    initDistance()

def run_mongo():
    #print(find_trusted_collaborators_skills(1,[4,5,6],'drinking')) #should return [5]
    a = find_common_uni_skill_interest(1, [4,2,3,6])
    for i in a:
        print(i)

init_mongo()
run_mongo()