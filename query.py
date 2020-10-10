import py2neo
from py2neo import Graph, Node, Relationship

graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")

# return the first result
# my_node = graph.evaluate('match (x:Assunto) return x')
# print(my_node)

nodes = graph.run("MATCH (a:Assunto) RETURN a.nome").data()
print(nodes)

# MATCH (n)
# DETACH DELETE n