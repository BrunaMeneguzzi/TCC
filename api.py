# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET
import re
import py2neo
from py2neo import Graph, Node, NodeMatcher, Relationship
pattern = re.compile("^([a-z]+)$")

arquivo = open('SAV1430674.xml', 'r', encoding = 'utf8')
#novo_arquivo = open('novo-arquivo.xml', 'w', encoding = 'utf8')
#linhas = arquivo.readlines()

#for i in range(0,len(linhas)):
#  linhas[i] = linhas[i].replace("marc:", "")
#  novo_arquivo.write(linhas[i])

#arquivo.close()
#novo_arquivo.close()

#ET.register_namespace('marc', 'http://www.loc.gov/MARC21/slim')
#ET._namespace_map['http://www.loc.gov/MARC21/slim'] = 'marc'

#mytree = ET.parse('novo-arquivo.xml')
mytree = ET.parse('SAV1421269.xml')
myroot = mytree.getroot()


# myroot é o collection
items = []

# # outra forma de printar o isbn
# for x in myroot:
#   var = x.find("./{http://www.loc.gov/MARC21/slim}controlfield[@tag='005']").text
#   print(var)

def createItem(properties_dict):
    graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
    nodename = Node('Item', **properties_dict)
    graph.create(nodename)

def createAutor(name):
    graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
    nodename = Node('Autor', nome=name)
    graph.create(nodename)

def createAssunto(name):
    graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
    nodename = Node('Assunto', nome=name)
    graph.create(nodename)

def createRelAutor(properties_dict, autor_text):
  graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
  item_titulo = properties_dict["titulo"]
  matcher = NodeMatcher(graph)
  m = matcher.match("Autor", nome=autor_text).first()
  n = matcher.match("Item", titulo=item_titulo).first()
  #print(n)
  #print(m)
  rel = Relationship(m, "É_AUTOR_DE", n)
  graph.create(rel)

def createRelAssunto(properties_dict, assunto):
  graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
  item_titulo = properties_dict["titulo"]
  matcher = NodeMatcher(graph)
  m = matcher.match("Assunto", nome=assunto).first()
  n = matcher.match("Item", titulo=item_titulo).first()
  #print(n)
  #print(m)
  rel = Relationship(m, "ASSUNTO", n)
  graph.create(rel)

graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")

# records são os filhos do myroot
for child in myroot:
  properties = dict()
  autor_text = ''
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
        if "autor_sec" in properties:
          properties["autor_sec"].append(autor2_text)
        else:
          properties["autor_sec"] = [autor2_text]
      if data.attrib.get('tag') == '650':
        assunto = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='a']").text
        properties["assunto"] = assunto
        matcher = NodeMatcher(graph)
        m = matcher.match("Assunto", nome=assunto).first()
        if m is None:
          #print(autor_text)
          createAssunto(assunto)
      if data.attrib.get('tag') == '245':
        titulo = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='a']").text
        properties["titulo"] = titulo
      if data.attrib.get('tag') == '945':
        material = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='b']").text
        properties["material"] = material
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
  for data in child.iter("{http://www.loc.gov/MARC21/slim}controlfield"):
    if data.attrib.get('tag') == '005':
      isbn = data.text
      #print(isbn)
      properties["isbn"] = isbn
  #items.append(properties)
  #createItem(properties)
  #if autor_text != '':
    #print(autor_text)
    #createRelAutor(properties, autor_text)
  if autor_text != '':
    #print(autor_text)
    createRelAutor(properties, assunto)
  #print(properties)
#print(items)

# ctrl + ; para comentar linhas

# problemas:
# 1. acentuação OK
# 2. quero pegar apenas os subfields de a-z e não números

# how to access http://localhost:7474/browser/