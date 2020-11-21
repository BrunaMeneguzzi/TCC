# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET
import re
import py2neo
from py2neo import Graph, Node, NodeMatcher, Relationship
pattern = re.compile("^([a-z]+)$")

#arquivo = open('SAV1425925.xml', 'r', encoding = 'utf8')

mytree = ET.parse('SAV1421269.xml')
myroot = mytree.getroot()

# myroot é o collection

biblioteca = input("Insira o nome da biblioteca:")

# # outra forma de printar o isbn
# for x in myroot:
#   var = x.find("./{http://www.loc.gov/MARC21/slim}controlfield[@tag='005']").text
#   print(var)

# MATCH (n)
# DETACH DELETE n

def createItem(properties_dict):
    graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
    nodename = Node('Item', **properties_dict)
    graph.create(nodename)

def createAssunto(assunto):
    graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
    nodename = Node('Assunto', assunto=assunto)
    graph.create(nodename)

def createRelUsuarios(usuario1, usuario2):
  graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
  matcher = NodeMatcher(graph)
  m = matcher.match("Usuário", usuario=usuario1).first()
  n = matcher.match("Usuário", usuario=usuario2).first()
  rel = Relationship(n, "SIMILARES", m)
  graph.create(rel)

def assuntos_comum(usuario1, usuario2):
    node = graph.run('''MATCH (a:Usuário {usuario:"''' + usuario1 + '''"}), (b:Usuário {usuario:"''' + usuario2 + '''"}), 
    (a)-[r:TEM_PREFERÊNCIA_POR]-(c:Assunto), (b)-[s:TEM_PREFERÊNCIA_POR]-(c:Assunto) 
    return a.usuario, b.usuario, c.assunto''').data()
    print(node)
    if node != []:
        createRelUsuarios(usuario1, usuario2)

# relacionamento entre 2 itens
# assuntos iguais
# autores iguais
# indexação de titulo
# indexação de nota
# mesma lingua (peso baixo)

def mesmo_idioma(isbn1, isbn2):
  node = graph.run('''MATCH (a:Item {isbn:"''' + isbn1 + '''", idioma:"por"}), (b:Item {isbn:"''' + isbn2 + '''", idioma:"por"}) 
  RETURN a.titulo, b.titulo, a.idioma''').data()
  print(node)
  if node != []:
    return 1
  else:
    return 0

def autores_iguais(isbn1, isbn2):
  node = graph.run('''MATCH (a:Item {isbn:"''' + isbn1 + '''"}), (b:Item {isbn:"''' + isbn2 + '''"}), 
  (c:Autor)-[r:É_AUTOR_DE]-(a), (c:Autor)-[s:É_AUTOR_DE]-(b) 
  return a.titulo, b.titulo, c.nome''').data()
  print(node)
  if node != []:
    return 1
  else:
    return 0

def assuntos_comum_usuarios(usuario1, usuario2):
    node = graph.run('''MATCH (a:Usuário {usuario:"''' + usuario1 + '''"}), (b:Usuário {usuario:"''' + usuario2 + '''"}), 
    (a)-[r:TEM_PREFERÊNCIA_POR]-(c:Assunto), (b)-[s:TEM_PREFERÊNCIA_POR]-(c:Assunto) 
    return a.usuario, b.usuario, c.assunto''').data()
    print(node)
    if node != []:
        createRelUsuarios(usuario1, usuario2)

def assuntos_comum_itens(item1, item2):
  node = graph.run('''MATCH (a:Item {isbn:"''' + item1 + '''"}), (b:Item {isbn:"''' + item2 + '''"}), 
  (a)-[r:PERTENCE_AO_ASSUNTO]-(c:Assunto), (b)-[s:PERTENCE_AO_ASSUNTO]-(c:Assunto) 
  return a.titulo, b.titulo, c.assunto''').data()
  #print(node)
  count1 = graph.run('''MATCH (a:Item {isbn:"''' + item1 + '''"}), (a)-[r:PERTENCE_AO_ASSUNTO]-(c:Assunto)
  return count(c) as count''').data()
  count2 = graph.run('''MATCH (a:Item {isbn:"''' + item2 + '''"}), (a)-[r:PERTENCE_AO_ASSUNTO]-(c:Assunto)
  return count(c) as count''').data()
  union = int(str(count1[0].values()).replace('dict_values([', '').replace('])', '')) + \
    int(str(count2[0].values()).replace('dict_values([', '').replace('])', ''))
  print(union)
  if node != []:
    return len(node)/union
    

def createRelItens(item1, item2, score):
  graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
  matcher = NodeMatcher(graph)
  m = matcher.match("Item", isbn=item1).first()
  n = matcher.match("Item", isbn=item2).first()
  rel = Relationship(n, "ITENS_SEMELHANTES", m, score=score)
  graph.create(rel)

graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")

# CRIAÇÃO DOS INDEX
#graph.run('''CALL db.index.fulltext.createNodeIndex('itens_nota', ['Item'], ['nota'], {analyzer: "brazilian"})''')
#graph.run('''CALL db.index.fulltext.createNodeIndex('itens', ['Item'], ['titulo'], {analyzer: "brazilian"})''')

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
    print(item_nota)
    if node['node.nota'] == item_nota:
      score = int(node['score'])
      print(score)
  return score

def itens(busca, item):
    nodes = graph.run('''CALL db.index.fulltext.queryNodes("entreItens", "''' + busca + '''") YIELD node, score
    RETURN node.isbn, node.titulo, score''').data()
    print(nodes)


#itens("folclore")

# Função que criou o NodeIndex entre Assuntos
#nodes = graph.run('''CALL db.index.fulltext.createNodeIndex("entreAssuntos",["Assunto"],["assunto"])''')
#print(nodes)

# CALL db.index.fulltext.createRelationshipIndex("taggedByRelationshipIndex",["TAGGED_AS"],["taggedByUser"], { analyzer: "url_or_email", eventually_consistent: "true" })

# Função que cria RelationshipIndex entre Itens e Assuntos
#nodes = graph.run('''CALL db.index.fulltext.createRelationshipIndex("pertenceAoAssunto", ["Item"],["Assunto"])''')

#index_busca("folclore")

#assuntos_comum("Zeza", "Bubu")

def createItem(properties_dict):
    graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
    nodename = Node('Item', **properties_dict)
    graph.create(nodename)

def createAutor(name):
    graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
    nodename = Node('Autor', nome=name)
    graph.create(nodename)

def createAutorSec(name):
    graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
    nodename = Node('Autor Secundário', nome=name)
    graph.create(nodename)

def createAssunto(assunto):
    graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
    nodename = Node('Assunto', assunto=assunto)
    graph.create(nodename)

def createMaterial(material):
    graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
    nodename = Node('Tipo de Material', tipo=material)
    graph.create(nodename)

def createBiblioteca(local):
    graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
    nodename = Node('Biblioteca', biblioteca=local)
    graph.create(nodename)

def createRelAutor(properties_dict, autor_text):
  graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
  item_titulo = properties_dict["titulo"]
  matcher = NodeMatcher(graph)
  m = matcher.match("Autor", nome=autor_text).first()
  n = matcher.match("Item", titulo=item_titulo).first()
  rel = Relationship(m, "É_AUTOR_DE", n)
  graph.create(rel)

def createRelBiblioteca(properties_dict, local):
  graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
  item_titulo = properties_dict["titulo"]
  matcher = NodeMatcher(graph)
  m = matcher.match("Biblioteca", biblioteca=local).first()
  n = matcher.match("Item", titulo=item_titulo).first()
  rel = Relationship(n, "ESTÁ_ALOCADO_EM", m)
  graph.create(rel)

def createRelAutorSec(properties_dict, autor_sec_text):
  graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
  item_titulo = properties_dict["titulo"]
  matcher = NodeMatcher(graph)
  m = matcher.match("Autor Secundário", nome=autor_sec_text).first()
  n = matcher.match("Item", titulo=item_titulo).first()
  rel = Relationship(m, "É_AUTOR_SECUNDÁRIO_DE", n)
  graph.create(rel)

def createRelAssunto(properties_dict, assunto):
  graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
  item_titulo = properties_dict["titulo"]
  matcher = NodeMatcher(graph)
  #print(assunto)
  m = matcher.match("Assunto", assunto=assunto).first()
  n = matcher.match("Item", titulo=item_titulo).first()
  rel = Relationship(n, "PERTENCE_AO_ASSUNTO", m)
  graph.create(rel)

def createRelMaterial(properties_dict, material):
  graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
  item_titulo = properties_dict["titulo"]
  matcher = NodeMatcher(graph)
  m = matcher.match("Tipo de Material", tipo=material).first()
  n = matcher.match("Item", titulo=item_titulo).first()
  rel = Relationship(n, "É_DO_TIPO_DE_MATERIAL", m)
  graph.create(rel)

graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")

# records são os filhos do myroot
for child in myroot:
  properties = dict()
  autor_text = ''
  assunto_list = []
  material = ''
  autor_sec_list = []
  local = ''
  for data in child.iter("{http://www.loc.gov/MARC21/slim}datafield"):
      if data.attrib.get('tag') == '041':
        idioma = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='a']").text
        properties["idioma"] = idioma
      if data.attrib.get('tag') == '044':
        pais = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='a']").text
        properties["pais"] = pais
      if data.attrib.get('tag') == '100':
        autor = data.findall("./{http://www.loc.gov/MARC21/slim}subfield")
        autor_text = ''
        for i in range(0, len(autor)):
          autor_text += autor[i].text + " "
        autor_text = autor_text[:-1]
        matcher = NodeMatcher(graph)
        m = matcher.match("Autor", nome=autor_text).first()
        if m is None:
          #print(autor_text)
          createAutor(autor_text)
      if data.attrib.get('tag') == '700':
        autor2 = data.findall("./{http://www.loc.gov/MARC21/slim}subfield")
        autor2_text = ''
        for i in range(0, len(autor2)):
          autor2_text += autor2[i].text + " "
        autor2_text = autor2_text[:-1]
        autor_sec_list.append(autor2_text)
        m = matcher.match("Autor Secundário", nome=autor2_text).first()
        if m is None:
          #print(autor_text)
          createAutorSec(autor2_text)
      if data.attrib.get('tag') == '650':
        assunto = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='a']").text
        matcher = NodeMatcher(graph)
        assunto_list.append(assunto)
        m = matcher.match("Assunto", assunto=assunto).first()
        if m is None:
          #print(autor_text)
          createAssunto(assunto)
      if data.attrib.get('tag') == '245':
        titulo = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='a']").text
        properties["titulo"] = titulo
      if data.attrib.get('tag') == '945':
        material = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='b']").text
        matcher = NodeMatcher(graph)
        m = matcher.match("Tipo de Material", tipo=material).first()
        if m is None:
          #print(autor_text)
          createMaterial(material)
      if data.attrib.get('tag') == '260':
        imprenta = data.findall("./{http://www.loc.gov/MARC21/slim}subfield")
        imprenta_text = ''
        for i in range(0, len(imprenta)):
          imprenta_text += imprenta[i].text + " "
        imprenta_text = imprenta_text[:-1]
        properties["imprenta"] = imprenta_text
      if data.attrib.get('tag') == '300':
        desc = data.findall("./{http://www.loc.gov/MARC21/slim}subfield")
        desc_text = ''
        for i in range(0, len(desc)):
          desc_text += desc[i].text + " "
        desc_text = desc_text[:-1]
        properties["desc_fisica"] = desc_text
      if data.attrib.get('tag') == '500':
        nota = data.findall("./{http://www.loc.gov/MARC21/slim}subfield")
        nota_text = ''
        for i in range(0, len(nota)):
          nota_text += nota[i].text + " "
        properties["nota"] = nota_text
      if data.attrib.get('tag') == '946':
        local1 = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='e']").text
        #print(local1)
        local2 = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='f']").text
        local = local1 + ' ' + local2
        matcher = NodeMatcher(graph)
        m = matcher.match("Biblioteca", biblioteca=local).first()
        if m is None:
          #print(autor_text)
          createBiblioteca(local)
  for data in child.iter("{http://www.loc.gov/MARC21/slim}controlfield"):
    if data.attrib.get('tag') == '005':
      isbn = data.text
      #print(isbn)
      properties["isbn"] = isbn
  #items.append(properties)
  createItem(properties)
  if autor_text != '':
    #print(autor_text)
    createRelAutor(properties, autor_text)
  if assunto_list != []:
    #print(assunto_list)
    for element in assunto_list:
      createRelAssunto(properties, element)
  if autor_sec_list != []:
    #print(autor_sec_list)
    for element in autor_sec_list:
      createRelAutorSec(properties, element)
  if material != '':
    #print(assunto)
    createRelMaterial(properties, material)
  if local != '':
    #print(assunto)
    createRelBiblioteca(properties, local)
  else:
    matcher = NodeMatcher(graph)
    m = matcher.match("Biblioteca", biblioteca=biblioteca).first()
    if m is None:
      #print(autor_text)
      createBiblioteca(biblioteca)
    createRelBiblioteca(properties, biblioteca)


# score_autores = autores_iguais("20200918225200.0", "20191119103535.0")
# print("score_autores = ", score_autores)
# score_assuntos = assuntos_comum_itens("20200918225200.0", "20191119103535.0")
# print("score_assuntos = ", score_assuntos)
# score_idioma = mesmo_idioma("20200918225200.0", "20191119103535.0")
# print("score_idioma = ", score_idioma)
# score_titulo = index_itens("20200918225200.0", "20191119103535.0")
# print("score_titulo = ", score_titulo)
# score_nota = index_itens("20200918225200.0", "20191119103535.0")
# print("score_nota = ", score_nota)
# score = (8*score_autores + 1.5*score_assuntos + 0.5*score_idioma)/10
# print("score = ", score)
# createRelItens("20200918225200.0", "20191119103535.0", score)
  #print(properties)
#print(items)

# ctrl + ; para comentar linhas

# problemas:
# 1. acentuação OK
# 2. quero pegar apenas os subfields de a-z e não números

# how to access http://localhost:7474/browser/