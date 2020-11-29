import py2neo
from py2neo import Graph, Node, Relationship, NodeMatcher, Relationship
import xml.etree.ElementTree as ET

graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")

mytree = ET.parse('SAV1431425.xml')
myroot = mytree.getroot()

def recomendacao(item):
    nodes = graph.run('''MATCH p=(n:Item {isbn:"''' + item + '''"})-[r:ITENS_SEMELHANTES]-(m:Item), 
    (g:Autor)-[:É_AUTOR_DE]->(n), (h:Autor)-[:É_AUTOR_DE]->(m), (n)-[:PERTENCE_AO_ASSUNTO]->(t:Assunto), 
    (m)-[:PERTENCE_AO_ASSUNTO]->(l:Assunto) RETURN m.titulo, t.assunto, l.assunto, g.nome, h.nome, 
    r.score ORDER BY r.score DESC LIMIT 10''').data()
    #print(nodes)
    return nodes

def allItens():
  #retorna todos os itens do grafo
  itens = graph.run('''MATCH (n:Item) RETURN n''').data()
  return itens

itens = allItens()
for item in itens:
    item = dict(item['n'])
    result = recomendacao(item['isbn'])
    print("Itens relacionados ao item ", item['titulo'])
    for item2 in result:
        print(item2)

# OS RELACIONAMENTOS DE ITENS_SEMELHANTES TÊM QUE SER IDA E VOLTA - OK