import py2neo
from py2neo import Graph, Node, Relationship, NodeMatcher, Relationship
import xml.etree.ElementTree as ET
import time

graph = Graph("http://localhost:11009/db/data/", user="neo4j", password="senha")

inicio = time.time()

def recomendacao(item):
    nodes = graph.run('''MATCH p=(n:Item {isbn:"''' + item + '''"})-[r:SE_ASSEMELHA_A]-(m:Item) 
    RETURN m.titulo, r.score ORDER BY r.score LIMIT 1''').data()
    #print(nodes)
    return nodes

def allItens():
  #retorna todos os itens do grafo
  itens = graph.run('''MATCH (n:Item) RETURN n''').data()
  return itens

def assuntos_comum(usuario1, usuario2):
    node = graph.run('''MATCH (a:Usuário {usuario:"''' + usuario1 + '''"}), (b:Usuário {usuario:"''' + usuario2 + '''"}), 
    (a)-[r:TEM_PREFERÊNCIA_POR]-(c:Assunto), (b)-[s:TEM_PREFERÊNCIA_POR]-(c:Assunto) 
    return a.usuario, b.usuario, c.assunto''').data()
    #print(node)
    if node != []:
        createRelUsuarios(usuario1, usuario2)

def mesmo_idioma(isbn1, isbn2):
  node = graph.run('''MATCH (a:Item {isbn:"''' + isbn1 + '''", idioma:"por"}), (b:Item {isbn:"''' + isbn2 + '''", idioma:"por"}) 
  RETURN a.titulo, b.titulo, a.idioma''').data()
  if node != []:
    return 1
  else:
    return 0

def autores_iguais(isbn1, isbn2):
  node = graph.run('''MATCH (a:Item {isbn:"''' + isbn1 + '''"}), (b:Item {isbn:"''' + isbn2 + '''"}), 
  (c:Autor)-[r:É_AUTOR_DE]-(a), (c:Autor)-[s:É_AUTOR_DE]-(b) 
  return a.titulo, b.titulo, c.nome''').data()
  if node != []:
    return 1
  else:
    return 0

def autores2_iguais(isbn1, isbn2):
  node = graph.run('''MATCH (a:Item {isbn:"''' + isbn1 + '''"}), (b:Item {isbn:"''' + isbn2 + '''"}), 
  (c:`Autor Secundário`)-[r:É_AUTOR_SECUNDÁRIO_DE]-(a), (c:`Autor Secundário`)-[s:É_AUTOR_SECUNDÁRIO_DE]-(b) 
  return a.titulo, b.titulo, c.nome''').data()
  if node != []:
    return 1
  else:
    return 0

def assuntos_comum_usuarios(usuario1, usuario2):
    node = graph.run('''MATCH (a:Usuário {usuario:"''' + usuario1 + '''"}), (b:Usuário {usuario:"''' + usuario2 + '''"}), 
    (a)-[r:TEM_PREFERÊNCIA_POR]-(c:Assunto), (b)-[s:TEM_PREFERÊNCIA_POR]-(c:Assunto) 
    return a.usuario, b.usuario, c.assunto''').data()
    if node != []:
        createRelUsuarios(usuario1, usuario2)

def assuntos_comum_itens(properties, item2):
  node = graph.run('''MATCH (a:Item {isbn:"''' + properties + '''"}), (b:Item {isbn:"''' + item2 + '''"}), 
  (a)-[r:PERTENCE_AO_ASSUNTO]-(c:Assunto), (b)-[s:PERTENCE_AO_ASSUNTO]-(c:Assunto) 
  return a.titulo, b.titulo, c.assunto''').data()
  count1 = graph.run('''MATCH (a:Item {isbn:"''' + properties + '''"}), (a)-[r:PERTENCE_AO_ASSUNTO]-(c:Assunto)
  return count(c) as count''').data()
  count2 = graph.run('''MATCH (a:Item {isbn:"''' + item2 + '''"}), (a)-[r:PERTENCE_AO_ASSUNTO]-(c:Assunto)
  return count(c) as count''').data()
  union = int(str(count1[0].values()).replace('dict_values([', '').replace('])', '')) + \
    int(str(count2[0].values()).replace('dict_values([', '').replace('])', ''))
  #print(union)
  if node != []:
    return union
  else:
    return 0

def material_comum_itens(properties, item2):
  node = graph.run('''MATCH (a:Item {isbn:"''' + properties + '''"}), (b:Item {isbn:"''' + item2 + '''"}), 
  (a)-[r:É_DO_TIPO_DE_MATERIAL]-(c:`Tipo de Material`), (b)-[s:É_DO_TIPO_DE_MATERIAL]-(c:`Tipo de Material`) 
  return a.titulo, b.titulo, c.material''').data()
  #print(node)
  count1 = graph.run('''MATCH (a:Item {isbn:"''' + properties + '''"}), (a)-[r:É_DO_TIPO_DE_MATERIAL]-(c:`Tipo de Material`)
  return count(c) as count''').data()
  count2 = graph.run('''MATCH (a:Item {isbn:"''' + item2 + '''"}), (a)-[r:É_DO_TIPO_DE_MATERIAL]-(c:`Tipo de Material`)
  return count(c) as count''').data()
  union = int(str(count1[0].values()).replace('dict_values([', '').replace('])', '')) + \
    int(str(count2[0].values()).replace('dict_values([', '').replace('])', ''))
  if node != []:
    return 1
  else:
    return 0
  
def biblioteca_comum_itens(properties, item2):
  node = graph.run('''MATCH (a:Item {isbn:"''' + properties + '''"}), (b:Item {isbn:"''' + item2 + '''"}), 
  (a)-[r:ESTÁ_ALOCADO_EM]-(c:Biblioteca), (b)-[s:ESTÁ_ALOCADO_EM]-(c:Biblioteca) 
  return a.titulo, b.titulo, c.biblioteca''').data()
  #print(node)
  count1 = graph.run('''MATCH (a:Item {isbn:"''' + properties + '''"}), (a)-[r:ESTÁ_ALOCADO_EM]-(c:Biblioteca)
  return count(c) as count''').data()
  count2 = graph.run('''MATCH (a:Item {isbn:"''' + item2 + '''"}), (a)-[r:ESTÁ_ALOCADO_EM]-(c:Biblioteca)
  return count(c) as count''').data()
  union = int(str(count1[0].values()).replace('dict_values([', '').replace('])', '')) + \
    int(str(count2[0].values()).replace('dict_values([', '').replace('])', ''))
  if node != []:
    return 1
  else:
    return 0    

def createRelItens(properties, item2, score):
  graph = Graph("http://localhost:11009/db/data/", user="neo4j", password="senha")
  matcher = NodeMatcher(graph)
  m = matcher.match("Item", isbn=properties).first()
  n = matcher.match("Item", isbn=item2).first()
  rel = Relationship(n, "SE_ASSEMELHA_A", m, score=score)
  graph.create(rel)

# função que retorna os itens relacionados à busca e seus scores.
def index_itens(busca, item):
  #busca = isbn do item
  #transformar isbn do item no titulo dele
  item_titulo = graph.run('''MATCH (n:Item {isbn:"''' + item + '''"}) RETURN n.titulo''').data()[0]
  #print(item_titulo['n.titulo'])
  item_titulo = item_titulo['n.titulo']
  titulo = graph.run('''MATCH (n:Item {isbn:"''' + busca + '''"}) RETURN n.titulo''').data()[0]
  #print(titulo['n.titulo'])
  titulo = titulo['n.titulo']
  nodes = graph.run('''CALL db.index.fulltext.queryNodes("itens", "''' + titulo + '''") YIELD node, score
  RETURN node.isbn, node.titulo, score''').data()
  #print(nodes)
  score = 0
  for node in nodes:
    #print(node['node.titulo'])
    #print(item_titulo)
    if node['node.titulo'] == item_titulo:
      score = int(node['score'])
      #print(score)
  return score

def index_itens_nota(busca, item):
  #busca = isbn do item
  #transformar isbn do item no titulo dele
  item_nota = graph.run('''MATCH (n:Item {isbn:"''' + item + '''"}) RETURN n.nota''').data()[0]
  #print(item_nota['n.nota'])
  item_nota = item_nota['n.nota']
  nota = graph.run('''MATCH (n:Item {isbn:"''' + busca + '''"}) RETURN n.nota''').data()[0]
  #print(nota['n.nota'])
  nota = nota['n.nota']
  nodes = graph.run('''CALL db.index.fulltext.queryNodes("itens_nota", "''' + nota + '''") YIELD node, score
  RETURN node.isbn, node.nota, score''').data()
  #print(nodes)
  score = 0
  for node in nodes:
    #print(node['node.titulo'])
    #print(item_nota)
    if node['node.nota'] == item_nota:
      score = int(node['score'])
  return score

item = "8508072732"
# itens = allItens()
# nodes = graph.run('''MATCH (n:Item {isbn:"''' + item + '''"}) RETURN n.isbn''').data()
# isbn1 = nodes[0]['n.isbn']
# # criação do relacionamento com os outros itens da base
# for item2 in itens:
#   item2 = dict(item2['n'])
#   if item2['isbn'] != isbn1:
#     #print(item2['isbn'])
#     print("RELACIONAMENTO COM ITEM ",item2['titulo'])
#     score_autores = autores_iguais(isbn1, item2['isbn'])
#     #print("score_autores = ", score_autores)
#     score_autores2 = autores2_iguais(isbn1, item2['isbn'])
#     #print("score_autores = ", score_autores)
#     score_assuntos = assuntos_comum_itens(isbn1, item2['isbn'])
#     #print("score_assuntos = ", score_assuntos)
#     score_material = material_comum_itens(isbn1, item2['isbn'])
#     #print("score_material = ", score_material)
#     score_biblioteca = biblioteca_comum_itens(isbn1, item2['isbn'])
#     #print("score_biblioteca = ", score_biblioteca)
#     score_titulo = index_itens(isbn1, item2['isbn'])
#     #print("score_titulo = ", score_titulo)
#     score_nota = index_itens(isbn1, item2['isbn'])
#     #print("score_nota = ", score_nota)
#     score = (8*score_autores + 3*score_autores2 + 3*score_assuntos + 1*score_material + 1*score_biblioteca + 5*score_titulo + 1*score_nota)/22
#     if score > 0.0:
#       createRelItens(isbn1, item2['isbn'], score)

result = recomendacao(item)
print("Itens relacionados:")
for item2 in result:
      print(item2)

#graph.run('''MATCH p=()-[r:SE_ASSEMELHA_A]->() DELETE r''')

fim = time.time()
print(fim - inicio)