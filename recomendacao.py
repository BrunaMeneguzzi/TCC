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

# relacionamento entre 2 itens
# assuntos iguais
# autores iguais
# indexação de titulo
# indexação de nota
# mesma lingua (peso baixo)



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

graph.run('''CALL db.index.fulltext.createNodeIndex('itens2', ['Item'], ['titulo', 'nota'], {analyzer: "brazilian"})''')


# CALL db.index.fulltext.createNodeIndex("titlesAndDescriptions",["Movie", "Book"],["title", "description"])

# Função que criou o NodeIndex entre Itens
#nodes = graph.run('''CALL db.index.fulltext.createNodeIndex("entreItens",["Item"],["titulo, nota"])''')
#print(nodes)

# Função que criou o NodeIndex entre Assuntos
#nodes = graph.run('''CALL db.index.fulltext.createNodeIndex("entreAssuntos",["Assunto"],["assunto"])''')
#print(nodes)

# função que retorna os itens relacionados à busca e seus scores.
def index_itens(busca):
    nodes = graph.run('''CALL db.index.fulltext.queryNodes("entreItens", "''' + busca + '''") YIELD node, score
    RETURN node.isbn, node.titulo, score''').data()
    print(nodes)

def itens(busca):
    nodes = graph.run('''CALL db.index.fulltext.queryNodes("entreItens", "''' + busca + '''") YIELD node, score
    RETURN node.isbn, node.titulo, score''').data()
    print(nodes)


itens("folclore")

# Função que criou o NodeIndex entre Assuntos
#nodes = graph.run('''CALL db.index.fulltext.createNodeIndex("entreAssuntos",["Assunto"],["assunto"])''')
#print(nodes)

# CALL db.index.fulltext.createRelationshipIndex("taggedByRelationshipIndex",["TAGGED_AS"],["taggedByUser"], { analyzer: "url_or_email", eventually_consistent: "true" })

# Função que cria RelationshipIndex entre Itens e Assuntos
#nodes = graph.run('''CALL db.index.fulltext.createRelationshipIndex("pertenceAoAssunto", ["Item"],["Assunto"])''')

def index_busca(busca):
    nodes = graph.run('''CALL db.index.fulltext.queryNodes("entreItens", "''' + busca + '''") YIELD node, score
    RETURN node.isbn, node.titulo, score''').data()
    print(nodes)
    nodes = graph.run('''CALL db.index.fulltext.queryNodes("pertenceAoAssunto", "''' + busca + '''") YIELD node, score
    RETURN node, score''').data()
    print(nodes)

#index_busca("folclore")

#assuntos_comum("Zeza", "Bubu")
score_autores = autores_iguais("20200918225200.0", "20191119103535.0")
print("score_autores = ", score_autores)
score_assuntos = assuntos_comum_itens("20200918225200.0", "20191119103535.0")
print("score_assuntos = ", score_assuntos)
score = (9*score_autores + 1*score_assuntos)/10
print("score = ", score)
#createRelItens("20200918225200.0", "20191119103535.0", score)



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