# NOTE TO SELF:
#  * skip first row of each file

import csv
import pprint
from pymongo import MongoClient
client = MongoClient()


db = client.test_database
client.drop_database(db)
# client.db.command("dropDatabase")


# userreader = csv.reader(usercsv, delimiter=',', quotechar='|')
#         for row in userreader:
#                 print row
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
            # print(user)
            users_id = users.insert_one(user).inserted_id
            # TEST
            # pprint.pprint(users.find_one({"first_name":"Justin"}))


def initSkill():
    # print('init skill')
    users = db.users
    users_skills = {}
    # {1: [{"yapping": 2},{"emails": 3}]}
    with open('Data/skill.csv') as skillcsv:
        skillcsv.readline()
        skill_reader = csv.reader(skillcsv, delimiter=',', quotechar='|')
        for row in skill_reader:
            if row[0] in users_skills:
                users_skills[row[0]].append({row[1]:row[2]})
            else:
                users_skills[row[0]]=[{row[1]:row[2]}]
        for user_id in users_skills:
            # print(users_skills[user_id])
            users.update({'user_id':int(user_id)},
                         {'$set':{'skills':users_skills[user_id]}})
            # TEST
        # pprint.pprint(users.find_one({"user_id":1}))

def initProject():
    projects = db.projects
    with open('Data/project.csv') as projectcsv:
        projectcsv.readline()
        project_reader = csv.reader(projectcsv, delimiter=',', quotechar='|')
        for row in project_reader:
            project = {"user_id":int(row[0]),
                    "project": row[1],
                    }
            project_id = projects.insert_one(project).inserted_id
             # TEST
            # pprint.pprint(projects.find_one({"user_id":1}))

def initOrganization():
    organizations = db.organizations
    with open('Data/organization.csv') as organizationcsv:
        organizationcsv.readline()
        organization_reader = csv.reader(organizationcsv, delimiter=',', quotechar='|')
        for row in organization_reader:
            organization = {"user_id":int(row[0]),
                            "organization":row[1],
                            "organization_type": row[2]}
            organization_id = organizations.insert_one(organization).inserted_id
            # TEST
           # pprint.pprint(projects.find_one({"user_id":1}))

def initInterest():
    interests = db.interests
    with open('Data/interest.csv') as interestcsv:
        interestcsv.readline()
        interest_reader = csv.reader(interestcsv, delimiter=',', quotechar='|')
        for row in interest_reader:
            interest = {"user_id":int(row[0]),
                        "interest":row[1],
                        "interest_level": row[2]}
            interest_id = interests.insert_one(interest).inserted_id
            # TEST
            # pprint.pprint(interests.find_one({"user_id":'1'}))
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
            # TEST
            # pprint.pprint(distances.find_one({"organization_1":'Hunter'}))

def find_trusted_collaborators_skills(origin_id, userids, skill):
    userids=[1,4,5,6]
    trusted_collaborators = []
    skill ='emailing'
    users = db.users
    for userid in userids:
        print(userid)
        pp = users.find_one({"user_id":userid})
        for skills in pp['skills']:
            if 'emailing' in skills:
                trusted_collaborators.append(userid)
    print(trusted_collaborators)
    return trusted_collaborators



def runAll():
    initUser()
    initSkill()
    find_trusted_collaborators_skills()


runAll()
