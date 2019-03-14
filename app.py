import init_neo

def command_line():
    while True:
        command = input("Please input a command: ")
        command.lower()

        if command == "quit" or command == "q":
            break



def run():
    init_neo.init_neo()
    command_line()

run()

# init_neo.find_trusted_collaborators('1')
# init_neo.find_uni_connect_users('1')
