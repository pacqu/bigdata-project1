import neo
import mongo

def get_uni_connected_users(origin_id):
    final_results = []
    neo_results = neo.find_uni_connect_users(origin_id)
    #print(neo_results)
    if 'o_user' not in neo_results:
        print('User of given origin id does not exist!')
    else:
        origin_user = neo_results['o_user']
        #print(origin_user)
        final_results.append(origin_user)
        connected_ids = []
        if 'connected_ids' in neo_results:
            connected_ids = neo_results['connected_ids']
            mongo_results = mongo.find_common_uni_skill_interest(origin_id, connected_ids)
            #print(mongo_results)
            origin_user['skills'] = mongo_results['origin_skills']
            origin_user['interests'] = mongo_results['origin_interests']
            for user_result in mongo_results['common_users']:
                user_result['org'] = neo_results['connected_users'][user_result['user_id']]['org']
                user_result['total_dist'] = neo_results['connected_users'][user_result['user_id']]['total_dist']
                final_results.append(user_result)
    return final_results
def find_nearby_users():
    origin_id = int(input("Please input an origin id: "))
    command_results = get_uni_connected_users(origin_id)
    #print(command_results)
    origin_org = ""
    for i in range(len(command_results)):
        user = command_results[i]
        if i == 0:
            print('Origin User:')
            skills = ", ".join(["{k} - {v}".format(k=k,v=str(v)) for d in user['skills'] if d != {} for (k,v) in d.items()])
            interests = ", ".join(["{k} - {v}".format(k=k,v=str(v)) for d in user['interests'] if d != {} for (k,v) in d.items()])
            origin_org = user['org']['name']
            print('{fname} {lname} - Organization: {orgname}({orgtype})'.format(fname=user['first_name'], lname=user['last_name'], orgname=user['org']['name'],orgtype=user['org']['org_type']))
            print('\tSkills: {skills}'.format(skills=skills))
            print('\tInterests: {interests}'.format(interests=interests))
            print('')
            if len(command_results) > 1:
                print('Connected Users with Common Skills/Interests:')
            else:
                if user['org']['org_type'] == 'U':
                    print('No Connected Users within 10 miles with Common Skills/Interests!')
                else:
                    print('Given User is not a University User!')
        else:
            print('{fname} {lname} - Organization: {orgname}({orgtype}) - Distance from {o_org}: {dist}'.format(fname=user['first_name'], lname=user['last_name'], orgname=user['org']['name'], orgtype=user['org']['org_type'], o_org=origin_org, dist=user['total_dist']))
            skills = ", ".join(["{k} - {v}".format(k=k,v=str(v)) for d in user['skills'] if d != {} for (k,v) in d.items()])
            interests = ", ".join(["{k} - {v}".format(k=k,v=str(v)) for d in user['interests'] if d != {} for (k,v) in d.items()])
            #print()
            if len(skills):
                print('\tCommon Skills: {skills} (Common Skill Score: {sscore})'.format(skills=skills, sscore=user['totalSkillMatch']))
            if len(interests):
                print('\tCommon Interests: {interests} (Common Interest Score: {iscore})'.format(interests=interests, iscore=user['totalInterestMatch']))
            print('\tTotal Common Score: {tscore}'.format(tscore=user['totalMatch']))
            print('')
def find_user():
    user_id = int(input("What is the User's ID? "))
    user = mongo.find_user(user_id)
    print(user)
    if not user:
        print('User does not exist')
        return
    skills = ", ".join(["{k} - {v}".format(k=k,v=str(v)) for d in user['skills'] if d != {} for (k,v) in d.items()])
    interests = ", ".join(["{k} - {v}".format(k=k,v=str(v)) for d in user['interests'] if d != {} for (k,v) in d.items()])
    print('{fname} {lname}'.format(fname=user['first_name'], lname=user['last_name']))
    print('\tSkills: {skills}'.format(skills=skills))
    print('\tInterests: {interests}'.format(interests=interests))
    if user['email'] or user['phone_number']:
        print('\tPhone Number: {phone_number}'.format(phone_number=user['phone_number']))
        print('\tEmail: {email}'.format(email=user['email']))

def find_org():
    org_name = input('What is the organization name? ')
    org = mongo.find_org(org_name.capitalize())
    if not org:
        print('Organization does not exist.')
        return
    print('\tOrganization Name: {org_name}\n\tOrganization Type: {org_type}'.format(org_name=org['organization'], org_type=org['organization_type']))

def print_commands():
    print('Commands:')
    print('\tuser: Prints user info')
    print('\torg: Prints organization info')
    print('\tuni: Prints nearby colleagues')
def command_line():
    print_commands()
    while True:
        command = input("Please input a command: ")
        command = command.lower()
        if command == "quit" or command == "q":
            break
        elif command == "uni":
            find_nearby_users()
        elif command == "user":
            find_user()
        elif command == 'org':
            find_org()

def run():
    neo.init_neo()
    mongo.init_mongo()
    command_line()

run()

# init_neo.find_trusted_collaborators('1')
# init_neo.find_uni_connect_users('1')
