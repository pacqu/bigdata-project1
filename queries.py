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


def get_trusted_col_of_col(origin_id, interests):
    final_results = {}
    neo_results = neo.find_trusted_collaborators(origin_id)
    #print(neo_results)
    mongo_results = mongo.find_trusted_collaborators_interests(origin_id, neo_results['ids'], interests)
    #print(mongo_results)
    for trust in mongo_results['trusted']:
        trust['common_trusted'] = ", ".join(neo_results['common_trust'][trust['user_id']])
    return mongo_results
def organize_list(input_list):
    return ", ".join(["{k} - {v}".format(k=k,v=str(v)) for d in input_list if d != {} for (k,v) in d.items()])
def find_nearby_users():
    origin_id = int(input("Please input an origin id: "))
    command_results = get_uni_connected_users(origin_id)
    #print(command_results)
    origin_org = ""
    for i in range(len(command_results)):
        user = command_results[i]
        if i == 0:
            print('Origin User:')
            skills = organize_list(user['skills'])
            interests = organize_list(user['interests'])
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
            skills = organize_list(user['skills'])
            interests = organize_list(user['interests'])
            if len(skills):
                print('\tCommon Skills: {skills} (Common Skill Score: {sscore})'.format(skills=skills, sscore=user['totalSkillMatch']))
            if len(interests):
                print('\tCommon Interests: {interests} (Common Interest Score: {iscore})'.format(interests=interests, iscore=user['totalInterestMatch']))
            print('\tTotal Common Score: {tscore}'.format(tscore=user['totalMatch']))
            print('')
def find_user():
    user_id = input("What is the User's ID? ")
    if not user_id.isdigit():
        print('Given ID is not valid')
        return
    user = mongo.find_user(int(user_id))
    if not user:
        print('User does not exist')
        return
    skills = organize_list(user['skills'])
    interests = organize_list(user['interests'])
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

def find_trusted():
    origin_id = int(input("Please input an origin id: "))
    desired_interests = []
    num_interests = int(input("Please input how many interests to be queried: "))
    for i in range(num_interests):
        desired_interests.append(input("Please input desired interest #{num}: ".format(num=i+1)))
    #print(desired_interests)
    command_results = get_trusted_col_of_col(origin_id,desired_interests)
    if command_results['o_user'] == None:
        print('User of given origin id does not exist!')
    else:
        o_user = command_results['o_user']
        print("Origin User: {fname} {lname}".format(fname=o_user['first_name'], lname=o_user['last_name']))
        print("\tDesired Interest(s): " + ", ".join(desired_interests))
        print(" ")
        if command_results['trusted']:
            print("Trusted Colleagues of Colleagues (TCoC):")
            for user in command_results['trusted']:
                print("TCoC: {fname} {lname}".format(fname=user['first_name'], lname=user['last_name']))
                print("\tInterests: " + ", ".join([k for d in user['interests'] for (k,v) in d.items()]))
                print("\tTrusted Colleague(s) in Common with Origin: {cols}".format(cols=user['common_trusted']))
                print(" ")
        else:
            print('No Trusted Colleagues')
def print_commands():
    print('Commands:')
    print('\thelp: Prints list of available commands')
    print('\tuser: Prints user info')
    print('\torg: Prints organization info')
    print('\tnearby: Prints nearby colleagues')
    print('\ttrusted: Prints trusted colleagues of colleagues')
    print('\tquit: Quits out of the program')