# NOTE TO SELF:
#  * skip first row of each file

import csv
import pprint
from pymongo import MongoClient
client = MongoClient()
# client.drop_database('<DBNAME>')

db = client.test_database
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
            user = {"user_id": row[0],
                    "first_name": row[1],
                    "last_name": row[2]}
            # print(user)
            users_id = users.insert_one(user).inserted_id
            # TEST
            # pprint.pprint(users.find_one({"first_name":"Justin"}))


def initSkill():
    skills = db.skills
    with open('Data/skill.csv') as skillcsv:
        skillcsv.readline()
        skill_reader = csv.reader(skillcsv, delimiter=',', quotechar='|')
        for row in skill_reader:
            skill = {"user_id":row[0],
                    "skill": row[1],
                    "skill_level": row[2]
                    }
            skill_id = skills.insert_one(skill).inserted_id
            # TEST
            # pprint.pprint(skills.find_one({"user_id":1}))

def initProject():
    projects = db.projects
    with open('Data/project.csv') as projectcsv:
        projectcsv.readline()
        project_reader = csv.reader(projectcsv, delimiter=',', quotechar='|')
        for row in project_reader:
            project = {"user_id":row[0],
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
            organization = {"user_id":row[0],
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
            interest = {"user_id":row[0],
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
