import neo
import mongo

def get_uni_connected_users(origin_id):
    final_results = []
    neo_results = neo.find_uni_connect_users(origin_id)
    #print(neo_results)
    origin_user = neo_results['o_user']
    mongo_results = mongo.find_common_uni_skill_interest(origin_id, neo_results['connected_ids'])
    origin_user['org'] = origin_user['org']['name']
    origin_user['skills'] = mongo_results['origin_skills']
    origin_user['interests'] = mongo_results['origin_interests']
    final_results.append(origin_user)
    for user_result in mongo_results['common_users']:
        user_result['org'] = neo_results['connected_users'][user_result['user_id']]['org']['name']
        final_results.append(user_result)
    return final_results

def command_line():
    while True:
        command = input("Please input a command: ")
        command = command.lower()
        if command == "quit" or command == "q":
            break
        elif command == "uni":
            origin_id = int(input("Please input an origin id: "))
            command_results = get_uni_connected_users(origin_id)
            for i in range(len(command_results)):
                user = command_results[i]
                if i == 0:
                    print('Origin User:')
                    print('{fname} {lname} - Organization: {orgname}'.format(fname=user['first_name'], lname=user['last_name'], orgname=user['org']))
                    print('\tSkills: {skills}'.format(skills=user['skills']))
                    print('\tInterests: {interests}'.format(interests=user['interests']))
                    print('')
                    print('Connected Users with Common Skills/Interests:')
                else:
                    print('{fname} {lname} - Organization: {orgname}'.format(fname=user['first_name'], lname=user['last_name'], orgname=user['org']))
                    skills = [x for x in user['skills'] if x != {}]
                    interests = [x for x in user['interests'] if x != {}]
                    print('\tSkills: {skills} - In-Common Skill Score: {sscore}'.format(skills=skills, sscore=user['totalSkillMatch']))
                    print('\tInterests: {interests} - In-Common Interest Score: {iscore}'.format(interests=interests, iscore=user['totalInterestMatch']))
                    print('\tTotal In-Common Score: {tscore}'.format(tscore=user['totalMatch']))
                    print('')

def run():
    neo.init_neo()
    command_line()

run()

# init_neo.find_trusted_collaborators('1')
# init_neo.find_uni_connect_users('1')
