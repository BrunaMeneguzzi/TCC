import py2neo
from py2neo import Graph, Node, Relationship, NodeMatcher, Relationship
import xml.etree.ElementTree as ET

graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")

def allUsers():
    #retorna todos os usuarios do grafo
    users = graph.run('''MATCH (n:Usuário) RETURN n''').data()
    return users

users = allUsers()
for user in users:
    print(user)
    user = dict(user['n'])
    itens = []
    usuario = str(user['usuario'])
    assuntos = graph.run('''MATCH p=(n:`Usuário` {usuario:''' + usuario + '''})-[r:`TEM_PREFERÊNCIA_POR`]->(m:Assunto) RETURN m.assunto''').data()
    #print(assuntos)
    for assunto in assuntos:
        assunto = assunto['m.assunto']
        itens1 = graph.run('''MATCH p=(n:Item)-[r:PERTENCE_AO_ASSUNTO]->(m:Assunto {assunto:"''' + assunto + '''"}), (u:`Usuário`)-[s:PEGOU_EMPRESTADO]->(n) RETURN DISTINCT n.titulo''').data()
    for item1 in itens1:
        itens.append(item1['n.titulo'])
    print(itens)

# COMO PRIORIZAR ITENS QUE JÁ FORAM PEGOS
# MATCH p=(n:Item)-[r:PERTENCE_AO_ASSUNTO]->(m:Assunto {assunto:"CONTO"}), q=(u:`Usuário`)-[s]->(n) WHERE s IS NOT "PEGOU_EMPRESTADO" RETURN DISTINCT n.titulo
# COMO RETIRAR AQUELES QUE O USUARIO JA PEGOU EMPRESTADO
# MATCH (j:Usuário {usuario:8493}), (n:Item)-[r:PERTENCE_AO_ASSUNTO]->(m:Assunto {assunto:"LITERATURA"}), (j)-[s:PEGOU_EMPRESTADO]->(n) WHERE NOT EXISTS s RETURN n.titulo