# THIS FILE WAS MEANT FOR TESTING



# from neo4jrestclient.client import GraphDatabase
# 
# gdb = GraphDatabase("https://10.0.1.234-44688/", username="neo4j", password="outline-tunnel-operators")
# # Create some nodes with labels
# user = gdb.labels.create("User")
# student = gdb.labels.create("Student")
# teacher = gdb.labels.create("Teacher")
# u1 = gdb.nodes.create(name="Dolby")
# u2 = gdb.nodes.create(name="Prachi")
# user.add(u1)
# user.add(u2)
# student.add(u1)
# teacher.add(u2)
# u2.relationships.create("Teaches", u1, since=1998, introduced_at="Thakur College of Dankology")
# 
# 
# query = '''MATCH (n) -[:Teaches]->()
#  RETURN n'''
# results = gdb.query(query, data_contents=True)
# print(results.rows)


# ------------------------------------------------------------------------------------------------------


from neo4j import GraphDatabase, basic_auth
driver = GraphDatabase.driver(
    "bolt://52.3.253.48:44687",
    auth=basic_auth("neo4j", "outline-tunnel-operators"))
session = driver.session()
# cypher_query = '''
# CREATE(:User{username:'banjy',email:'aa@aa.com'})
# '''
#
# results = session.run(cypher_query,
#   parameters={})
#
# for record in results:
#   print(record['id'])

cypher_query = '''
MATCH (n)
RETURN id(n) AS id
LIMIT 10
'''
results = session.run(cypher_query,
  parameters={})

print(results.value())


# ------------------------------------------------------------------------------------------------------
# from neo4j import GraphDatabase, basic_auth
# driver = GraphDatabase.driver(
#     "bolt://hobby-gfahodcaabamgbkegkdpbbel.dbs.graphenedb.com:24787",
#     auth=basic_auth("developer", "b.rEb0aDuWDSh6.MJh3xAHL51pltkfC"))
# session = driver.session()
# # cypher_query = '''
# # CREATE(:User{username:'banjy',email:'aa@aa.com'})
# # '''
# #
# # results = session.run(cypher_query,
# #   parameters={})
# #
# # for record in results:
# #   print(record['id'])
#
# cypher_query = '''
# MATCH (n:Movie) RETURN n
# LIMIT 10
# '''
# results = session.run(cypher_query,
#   parameters={})
#
# print(results.value())
# print(results.value())
