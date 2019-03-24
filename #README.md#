Big Data by Justin Pacquing and Noam Sohn

# Expected Data in CSV:
## User:
* User_id, First_name, Last_name, Phone_number, Email
## Project:
* User_id, Project_name
## Interests:
* User_id, Interest, Interest_level
## Skills:
* User_id, Skill, Skill Level
## Organizations
* User_id, Organization, Organization_type
## Distance:
* Organization 1, Organization 2, Distance

## Explanation and Diagrams:

# Options Queries:
##

# All queries
* ***'trusted'***: Given an origin_id, number of interests to query for, and the list of queries, trusted returns the list of trusted colleagues of colleagues. It searches through the origin_id's colleagues and then finds their colleagues, afterwards it searches through that list and determines if they have the any of the interests that the origin_id requested, if so it is returned.
* ***'user'***: Given a user_id, returns the user information from MongoDB. If teh user does not exists, returns error message.
* ***'nearby'***: Given a user_id, nearby returns the list of users within LAKSJF:LASKFJASL:FKJSAL:FKJASFL:KJ
* ***'org'***: Given the name of the organization, returns the details of the organization. If no organization exists, returns an error message.
* ***'help'***: Prints a list of the available queries and a brief description.
* ***'quit' or 'q'***: Exits the program




# Potential improvements
Our databases are expecting the information to be provided in a reasonable format, however, big data does not always function in that way; we could enhance the system by allowing for 'incomplete' data to be stored in Mongo/Neo4j. Furthermore, when searching for an item, if one searched for "Hunter" instead of "Hunter College" the system will return that it does not have any nodes with "Hunter" an update we could implement would be to allow for incomplete searches to return information and clarify if that was the result the user was expecting when they searched for the shortcut term.