# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET
import py2neo
import time
from py2neo import Graph, Node, NodeMatcher, Relationship

inicio = time.time()

#arquivo = open('SAV1425925.xml', 'r', encoding = 'utf8')

mytree = ET.parse('itens_1312_v3.xml')
myroot = mytree.getroot()

# myroot é o collection

biblioteca = input("Insira o nome da biblioteca:")

# MATCH (n) DETACH DELETE n

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

def allItens():
  #retorna todos os itens do grafo
  itens = graph.run('''MATCH (n:Item) RETURN n''').data()
  return itens

def assuntos_comum(usuario1, usuario2):
    node = graph.run('''MATCH (a:Usuário {usuario:"''' + usuario1 + '''"}), (b:Usuário {usuario:"''' + usuario2 + '''"}), 
    (a)-[r:TEM_PREFERÊNCIA_POR]-(c:Assunto), (b)-[s:TEM_PREFERÊNCIA_POR]-(c:Assunto) 
    return a.usuario, b.usuario, c.assunto''').data()
    print(node)
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
  if node != []:
    return 1
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
  graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
  matcher = NodeMatcher(graph)
  m = matcher.match("Item", isbn=properties).first()
  n = matcher.match("Item", isbn=item2).first()
  rel = Relationship(n, "ITENS_SEMELHANTES", m, score=score)
  graph.create(rel)

graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")

# CRIAÇÃO DOS INDEX
graph.run('''CALL db.index.fulltext.createNodeIndex('itens_nota', ['Item'], ['nota'], {analyzer: "brazilian"})''')
graph.run('''CALL db.index.fulltext.createNodeIndex('itens', ['Item'], ['titulo'], {analyzer: "brazilian"})''')

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
  return score

def itens(busca, item):
    nodes = graph.run('''CALL db.index.fulltext.queryNodes("entreItens", "''' + busca + '''") YIELD node, score
    RETURN node.isbn, node.titulo, score''').data()
    print(nodes)

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

# records são os filhos do myroot
for child in myroot:
  try:
    # retorna todos os itens
    itens = allItens()
    properties = dict()
    autor_text = ''
    assunto_list = []
    material = ''
    autor_sec_list = []
    local = ''
    for data in child.iter("{http://www.loc.gov/MARC21/slim}datafield"):
        if data.attrib.get('tag') == '041':
          # idioma
          idioma = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='a']").text
          properties["idioma"] = idioma

        if data.attrib.get('tag') == '044':
          # pais
          pais = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='a']").text
          properties["pais"] = pais

        if data.attrib.get('tag') == '020':
          # isbn
          isbn = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='a']")
          if isbn != None:
            properties["isbn"] = isbn.text
          #print(properties["isbn"])

        if data.attrib.get('tag') == '100':
          # autor
          autor = data.findall("./{http://www.loc.gov/MARC21/slim}subfield")
          autor_text = ''
          for i in range(0, len(autor)):
            autor_text += autor[i].text + " "
          autor_text = autor_text[:-1]
          matcher = NodeMatcher(graph)
          m = matcher.match("Autor", nome=autor_text).first()
          if m is None:
            createAutor(autor_text)

        if data.attrib.get('tag') == '700':
          # autor secundário
          autor2 = data.findall("./{http://www.loc.gov/MARC21/slim}subfield")
          autor2_text = ''
          for i in range(0, len(autor2)):
            autor2_text += autor2[i].text + " "
          autor2_text = autor2_text[:-1]
          autor_sec_list.append(autor2_text)
          m = matcher.match("Autor Secundário", nome=autor2_text).first()
          if m is None:
            createAutorSec(autor2_text)

        if data.attrib.get('tag') == '650':
          # assunto
          assunto = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='a']").text
          matcher = NodeMatcher(graph)
          assunto_list.append(assunto)
          m = matcher.match("Assunto", assunto=assunto).first()
          if m is None:
            createAssunto(assunto)

        if data.attrib.get('tag') == '245':
          # titulo
          titulo = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='a']").text
          titulo2 = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='b']")
          if titulo2 != None:
            titulo2 = titulo2.text
            properties["titulo"] = titulo + " " + titulo2
          else:
            properties["titulo"] = titulo
          print(properties["titulo"])

        if data.attrib.get('tag') == '945':
          # tipo de material
          material = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='b']").text
          matcher = NodeMatcher(graph)
          m = matcher.match("Tipo de Material", tipo=material).first()
          if m is None:
            createMaterial(material)

        if data.attrib.get('tag') == '260':
          # imprenta
          imprenta = data.findall("./{http://www.loc.gov/MARC21/slim}subfield")
          imprenta_text = ''
          for i in range(0, len(imprenta)):
            imprenta_text += imprenta[i].text + " "
          imprenta_text = imprenta_text[:-1]
          properties["imprenta"] = imprenta_text

        if data.attrib.get('tag') == '300':
          # descrição física
          desc = data.findall("./{http://www.loc.gov/MARC21/slim}subfield")
          desc_text = ''
          for i in range(0, len(desc)):
            desc_text += desc[i].text + " "
          desc_text = desc_text[:-1]
          properties["desc_fisica"] = desc_text

        if data.attrib.get('tag') == '500':
          # nota
          nota = data.findall("./{http://www.loc.gov/MARC21/slim}subfield")
          nota_text = ''
          for i in range(0, len(nota)):
            nota_text += nota[i].text + " "
          properties["nota"] = nota_text

        if data.attrib.get('tag') == '946':
          # biblioteca
          local1 = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='e']").text
          local2 = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='f']").text
          local = local1 + ' ' + local2
          matcher = NodeMatcher(graph)
          m = matcher.match("Biblioteca", biblioteca=local).first()
          if m is None:
            createBiblioteca(local)
    print(properties)
    if 'isbn' in properties:
      matcher = NodeMatcher(graph)
      m = matcher.match("Item", isbn=properties['isbn']).first()
      if m == None:
        createItem(properties)
    else:
      continue

    # criação de relacionamentos
    if autor_text != '':
      createRelAutor(properties, autor_text)
    if assunto_list != []:
      for element in assunto_list:
        createRelAssunto(properties, element)
    if autor_sec_list != []:
      for element in autor_sec_list:
        createRelAutorSec(properties, element)
    if material != '':
      createRelMaterial(properties, material)
    matcher = NodeMatcher(graph)
    m = matcher.match("Biblioteca", biblioteca=biblioteca).first()
    if m is None:
      createBiblioteca(biblioteca)
    createRelBiblioteca(properties, biblioteca)
    print("ITEM ",properties['titulo']," INSERIDO")

    # criação do relacionamento com os outros itens da base
    # for item2 in itens:
    #   item2 = dict(item2['n'])
    #   #print(item2['isbn'])
    #   #print("RELACIONAMENTO COM ITEM ",item2['titulo'])
    #   score_autores = autores_iguais(properties['isbn'], item2['isbn'])
    #   #print("score_autores = ", score_autores)
    #   score_autores2 = autores2_iguais(properties['isbn'], item2['isbn'])
    #   #print("score_autores = ", score_autores)
    #   score_assuntos = assuntos_comum_itens(properties['isbn'], item2['isbn'])
    #   #print("score_assuntos = ", score_assuntos)
    #   score_material = material_comum_itens(properties['isbn'], item2['isbn'])
    #   #print("score_material = ", score_material)
    #   score_biblioteca = biblioteca_comum_itens(properties['isbn'], item2['isbn'])
    #   #print("score_biblioteca = ", score_biblioteca)
    #   score_titulo = index_itens(properties['isbn'], item2['isbn'])
    #   #print("score_titulo = ", score_titulo)
    #   score_nota = index_itens(properties['isbn'], item2['isbn'])
    #   #print("score_nota = ", score_nota)
    #   score = (8*score_autores + 3*score_autores2 + 3*score_assuntos + 1*score_material + 5*score_titulo + 1*score_nota)/22
    #   if score >= 1.0:
    #     createRelItens(properties['isbn'], item2['isbn'], score)
  except:
    print("An exception occurred")

fim = time.time()
print(fim - inicio)

# how to access http://localhost:7474/browser/