import py2neo
from py2neo import Graph, Node, Relationship, NodeMatcher, Relationship
import xml.etree.ElementTree as ET

graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")

mytree = ET.parse('SAV1431425.xml')
myroot = mytree.getroot()


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

assuntos_comum("Zeza", "Bubu")

def createRelAssunto(properties_dict, assunto):
  graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
  item_titulo = properties_dict["titulo"]
  matcher = NodeMatcher(graph)
  #print(assunto)
  m = matcher.match("Assunto", assunto=assunto).first()
  n = matcher.match("Item", titulo=item_titulo).first()
  rel = Relationship(n, "PERTENCE_AO_ASSUNTO", m)
  graph.create(rel)

# for child in myroot:
#   properties = dict()
#   autor_text = ''
#   assunto_list = []
#   material = ''
#   autor_sec_list = []
#   local = ''
#   for data in child.iter("{http://www.loc.gov/MARC21/slim}datafield"):
#       if data.attrib.get('tag') == '041':
#         idioma = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='a']").text
#         properties["idioma"] = idioma
#       if data.attrib.get('tag') == '044':
#         pais = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='a']").text
#         properties["pais"] = pais
#       if data.attrib.get('tag') == '650':
#         assunto = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='a']").text
#         matcher = NodeMatcher(graph)
#         assunto_list.append(assunto)
#       if data.attrib.get('tag') == '245':
#         titulo = data.find("./{http://www.loc.gov/MARC21/slim}subfield[@code='a']").text
#         properties["titulo"] = titulo
#       if data.attrib.get('tag') == '260':
#         imprenta = data.findall("./{http://www.loc.gov/MARC21/slim}subfield")
#         imprenta_text = ''
#         for i in range(0, len(imprenta)):
#           imprenta_text += imprenta[i].text + " "
#         imprenta_text = imprenta_text[:-1]
#         properties["imprenta"] = imprenta_text
#       if data.attrib.get('tag') == '300':
#         desc = data.findall("./{http://www.loc.gov/MARC21/slim}subfield")
#         desc_text = ''
#         for i in range(0, len(desc)):
#           desc_text += desc[i].text + " "
#         desc_text = desc_text[:-1]
#         properties["desc_fisica"] = desc_text
#       if data.attrib.get('tag') == '500':
#         nota = data.findall("./{http://www.loc.gov/MARC21/slim}subfield")
#         nota_text = ''
#         for i in range(0, len(nota)):
#           nota_text += nota[i].text + " "
#         properties["nota"] = nota_text
#   for data in child.iter("{http://www.loc.gov/MARC21/slim}controlfield"):
#     if data.attrib.get('tag') == '005':
#       isbn = data.text
#       #print(isbn)
#       properties["isbn"] = isbn
#   createItem(properties)
#   if assunto_list != []:
#     for element in assunto_list:
#       matcher = NodeMatcher(graph)
#       m = matcher.match("Assunto", assunto=element).first()
#       if m is None:
#         createAssunto(element)
#       createRelAssunto(properties, element)

# def remove_repetidos(lista):
#     l = []
#     for i in lista:
#         if i not in l:
#             l.append(i)
#     l.sort()
#     return l