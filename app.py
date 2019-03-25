import queries
import init_mongo
import init_neo
import sys

def command_line():
    queries.print_commands()
    while True:
        command = input("Please input a command: ")
        command = command.lower()
        if command == "quit" or command == "q":
            break
        elif command == "nearby":
            queries.find_nearby_users()
        elif command == "user":
            queries.find_user()
        elif command == 'org':
            queries.find_org()
        elif command == 'proj':
            queries.find_proj()
        elif command == "trusted":
            queries.find_trusted()
        elif command == "help":
            queries.print_commands()

# python app.py Data/user.csv Data/organization.csv Data/distance.csv Data/project.csv Data/skill.csv Data/interest.csv
def load_csv():
    user_csv = 'Data/user.csv'
    org_csv = 'Data/organization.csv'
    dist_csv = 'Data/distance.csv'
    proj_csv = 'Data/project.csv'
    skill_csv = 'Data/skill.csv'
    interest_csv = 'Data/interest.csv'

    if len(sys.argv) != 7:
        print('Using default values')
    else:
        user_csv = sys.argv[1]
        org_csv = sys.argv[2]
        dist_csv = sys.argv[3]
        proj_csv = sys.argv[4]
        skill_csv = sys.argv[5]
        interest_csv = sys.argv[6]
    init_neo.init(user_csv,org_csv,dist_csv,proj_csv)
    init_mongo.init(user_csv,skill_csv,interest_csv,org_csv, proj_csv, dist_csv)


def run():
    load_csv()
    command_line()

run()
