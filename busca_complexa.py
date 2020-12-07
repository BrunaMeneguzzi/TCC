import py2neo
from py2neo import Graph, Node, Relationship, NodeMatcher, Relationship
import xml.etree.ElementTree as ET

graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")

def allItens():
  #retorna todos os itens do grafo
  itens = graph.run('''MATCH (n:Item) RETURN n''').data()
  return itens

def allUsers():
    #retorna todos os itens do grafo
    users = graph.run('''MATCH (n:Usuário) RETURN n''').data()
    return users

def createRelUsuarioItem(user, item):
    #verifica se o usuario já pegou o item
    pegou_item = graph.run('''RETURN EXISTS( (:Usuário {usuario:''' + user + '''})-[:PEGOU_EMPRESTADO]->(:Item {isbn:''' + item + '''}))''').data()
    if list(pegou_item[0].values())[0] == False:
        score_item = 0
    else:
        score_item = 1
    #verifica se o item tem assuntos em comum com o usuárioassuntos_comum = MATCH (v:Usuário {usuario:3025})-[:TEM_PREFERÊNCIA_POR]->(m:Assunto) RETURN m.assunto
    assuntos_comum = graph.run('''MATCH (v:Usuário {usuario:''' + user + '''})-[:TEM_PREFERÊNCIA_POR]->(m:Assunto) RETURN m.assunto''').data()
    if assuntos_comum == []:
        score_assunto = 0
    else:
        score_assunto = 1
    #verifica se o usuário ja pegou algum item com os assuntos do item
    #verifica se o usuario ja pegou algum item com os autores do item
    #verifica se o usuario ja pegou algum item da biblioteca que está o item
    if score_item == 0:
        score = 

createRelUsuarioItem("3025","20110814003400.0")

# itens = allItens()
# for user in allUsers():
#     for item in itens:
#     item = dict(item['n'])
#     result = recomendacao(item['isbn'])
#     print("Itens relacionados ao item ", item['titulo'])
#     for item2 in result:
#         print(item2)

# OS RELACIONAMENTOS DE ITENS_SEMELHANTES TÊM QUE SER IDA E VOLTA - OK