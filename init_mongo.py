import csv
import pprint
from pymongo import MongoClient
client = MongoClient()

db = client.test_database

def initUser():
    users = db.users

    user_loc = ("Data/user.xlsx")
    wb = xlrd.open_workbook(user_loc)
    sheet = wb.sheet_by_index(0)

    # Read csv and extract data
    for row in range(1,sheet.nrows):
        arr = sheet.row_values(row)
        user = {"user_id": arr[0],
                "first_name": arr[1],
                "last_name": arr[2]}
        users_id = users.insert_one(user).inserted_id
    # TEST
    # pprint.pprint(users.find_one({"first_name":"Justin"}))


def initSkill():
    skills = db.skills

    skill_loc = ("Data/skill.xlsx")
    wb = xlrd.open_workbook(skill_loc)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(1, 0)

    for row in range(1, sheet.nrows):
        arr = sheet.row_values(row)
        skill = {"user_id":arr[0],
                "skill": arr[1],
                "skill_level": arr[2]
                }
        skill_id = skills.insert_one(skill).inserted_id
    # TEST
    # pprint.pprint(skills.find_one({"user_id":1}))

def initProject():
    projects = db.projects

    project_loc = ("Data/project.xlsx")
