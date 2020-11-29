import py2neo
from py2neo import Graph, Node, Relationship, NodeMatcher, Relationship
import xml.etree.ElementTree as ET

graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")

mytree = ET.parse('SAV1431425.xml')
myroot = mytree.getroot()

# função que retorna os itens relacionados à busca e seus scores.
def index_itens(busca, item):
  #busca = isbn do item
  #transformar isbn do item no titulo dele
  item_titulo = graph.run('''MATCH (n:Item {isbn:"''' + item + '''"}) RETURN n.titulo''').data()[0]
  print(item_titulo['n.titulo'])
  item_titulo = item_titulo['n.titulo']
  titulo = graph.run('''MATCH (n:Item {isbn:"''' + busca + '''"}) RETURN n.titulo''').data()[0]
  print(titulo['n.titulo'])
  titulo = titulo['n.titulo']
  nodes = graph.run('''CALL db.index.fulltext.queryNodes("itens", "''' + titulo + '''") YIELD node, score
  RETURN node.isbn, node.titulo, score''').data()
  print(nodes)
  score = 0
  for node in nodes:
    print(node['node.titulo'])
    print(item_titulo)
    if node['node.titulo'] == item_titulo:
      score = int(node['score'])
      print(score)
  return score

def index_itens_nota(busca, item):
  #busca = isbn do item
  #transformar isbn do item no titulo dele
  item_nota = graph.run('''MATCH (n:Item {isbn:"''' + item + '''"}) RETURN n.nota''').data()[0]
  print(item_nota['n.nota'])
  item_nota = item_nota['n.nota']
  nota = graph.run('''MATCH (n:Item {isbn:"''' + busca + '''"}) RETURN n.nota''').data()[0]
  print(nota['n.nota'])
  nota = nota['n.nota']
  nodes = graph.run('''CALL db.index.fulltext.queryNodes("itens_nota", "''' + nota + '''") YIELD node, score
  RETURN node.isbn, node.nota, score''').data()
  print(nodes)
  score = 0
  for node in nodes:
    #print(node['node.titulo'])
    if node['node.nota'] == item_nota:
      score = int(node['score'])
  return score

score_titulo = index_itens("20140408134700.0", "20191119103535.0")
print("score_titulo = ", score_titulo)
score_nota = index_itens_nota("20140408134700.0", "20191119103535.0")
print("score_nota = ", score_nota)