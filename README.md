# Big Data by Justin Pacquing and Noam Sohn

## Expected Data in CSV:
### User:
* User_id, First_name, Last_name, Phone_number, Email
### Project:
* User_id, Project_name
### Interests:
* User_id, Interest, Interest_level
### Skills:
* User_id, Skill, Skill Level
### Organizations
* User_id, Organization, Organization_type
### Distance:
* Organization 1, Organization 2, Distance

## Diagrams and Explanations:
### Neo4j Database:
![Neo4j Diagram](Data/neo4jdiagram.png)

#### Our Neo4j Database has 3 types of Entities
* Users
  * The registered users of the Application
  * Users have three properties:
    * 'first_name': the user's first name
    * 'last_name': the user's last name
    * 'user_id': the unique identifier of a user from the loaded user csv
   
* Organizations
  * The organizations users work for
  * Organizations have two properties:
    * 'name': the name of the organization
    * 'org_type': the type of organization
      * Possible Value of 'org_type' are:
        * 'U': University
        * 'C': Company
        * 'G': Government
       
* Projects
  * The projects users have worked on
  * Projects have one property:
    * 'name': the name of the project


#### Our Neo4j Database has 3 types of Relationships
* WORKS_FOR
  * Connects User --> Organization
  * Describes what organization a user works for
  * Has one property:
    * 'since': the year the user started working
   
* WORKED_ON
  * Connects User --> Project
  * Describes what project(s) a user worked on
  * Has two properties:
    * 'from': the year the user started working on the project
    * 'to': the year the user last worked on the project
    
* DISTANCE
  * Connects Organization --> Organization
  * Describes how far an organization is from another
  * Has one property:
    * 'distance': the distance between two organizations
   
### MongoDB Database
![MongoDB Diagram](Data/mongodbdiagram.png)

#### Collections
* Users
  * The registered users of the Application
  * Each User document has five fields:
    * 'first_name': the user's first name
    * 'last_name': the user's last name
    * 'user_id': the unique identifier of a user from the loaded user csv
    * 'skills': an array of documents each containg a user skill as a field and the weight of that skill as the value
    * 'interests': an array of documents each containg a user interest as a field and the weight of that interest as the value
   
* Organizations
  * The organizations users work for
  * Each Organization document have two fields:
    * 'name': the name of the organization
    * 'org_type': the type of organization
      * Possible Value of 'org_type' are:
        * 'U': University
        * 'C': Company
        * 'G': Government
       
* Projects
  * The projects users have worked on
  * Each Project document have one field:
    * 'name': the name of the project
  
## Options Queries:
##

## All queries

## Potential improvements
* Add additional information for each entity
* Be able to create/delete/modify entities from the command line
