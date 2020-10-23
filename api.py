# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET
import re
import py2neo
from py2neo import Graph, Node, NodeMatcher, Relationship
pattern = re.compile("^([a-z]+)$")

#arquivo = open('SAV1425925.xml', 'r', encoding = 'utf8')

mytree = ET.parse('SAV1431425.xml')
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
  #print(properties)
#print(items)

# ctrl + ; para comentar linhas

# problemas:
# 1. acentuação OK
# 2. quero pegar apenas os subfields de a-z e não números

# how to access http://localhost:7474/browser/