import init_neo

init_neo.init_neo()
u = init_neo.find_uni_connect_users('1')
for node in u:
    print(node)
