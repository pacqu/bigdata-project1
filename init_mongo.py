import csv
from pymongo import MongoClient
client = MongoClient()


db = client.test_database
client.drop_database(db)

def initUser(user_input_csv):
    users = db.users
    with open(user_input_csv) as usercsv:
        usercsv.readline()
        user_reader = csv.reader(usercsv, delimiter=',', quotechar='|')
        for row in user_reader:
            user = {}
            if len(row) != 5:
                # insert placeholder for phone_number and email
                row.append('')
                row.append('')
            user = {"user_id": int(row[0]),
                    "first_name": row[1],
                    "last_name": row[2],
                    "phone_number":row[3],
                    "email":row[4]
                    }
            users_id = users.insert_one(user).inserted_id

def initSkill(skill_input_csv):
    users = db.users
    users_skills = {}
    with open(skill_input_csv) as skillcsv:
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

def initProject(project_input_csv):
    projects = db.projects
    with open(project_input_csv) as projectcsv:
        projectcsv.readline() # skip first row
        project_reader = csv.reader(projectcsv, delimiter=',', quotechar='|')
        for row in project_reader:
            project = {"user_id":int(row[0]),
                    "project": row[1],
                    }
            project_id = projects.insert_one(project).inserted_id

def initOrganization(org_input_csv):
    organizations = db.organizations
    with open(org_input_csv) as organizationcsv:
        organizationcsv.readline() # skip first row
        organization_reader = csv.reader(organizationcsv, delimiter=',', quotechar='|')
        for row in organization_reader:
            organization = {"user_id":int(row[0]),
                            "organization":row[1],
                            "organization_type": row[2]}
            organization_id = organizations.insert_one(organization).inserted_id

def initInterest(interest_input_csv):
    users = db.users
    users_interests = {}
    interests = db.interests
    with open(interest_input_csv) as interestcsv:
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

def initDistance(dist_input_csv):
    distances = db.distances
    with open(dist_input_csv) as distancecsv:
        distancecsv.readline()
        distance_reader = csv.reader(distancecsv, delimiter=',', quotechar='|')
        for row in distance_reader:
            distance = {"organization_1":row[0],
                        "organization_2":row[1],
                        "distance": row[2]}
            distance_id = distances.insert_one(distance).inserted_id

def init(*arg):
    initUser(arg[0])
    initSkill(arg[1])
    initInterest(arg[2])
    initOrganization(arg[3])
    initProject(arg[4])
    initDistance(arg[5])
