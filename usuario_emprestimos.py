import py2neo
from py2neo import Graph, Node, Relationship, NodeMatcher

graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")

def createUsuario(usuario):
    graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
    nodename = Node('Usuário', usuario=usuario)
    graph.create(nodename)

def createRelEmprestimo(usuario, item):
  graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
  matcher = NodeMatcher(graph)
  m = matcher.match("Usuário", usuario=usuario).first()
  n = matcher.match("Item", isbn=item).first()
  rel = Relationship(m, "PEGOU_EMPRESTADO", n)
  graph.create(rel)

def assuntos_item(item):
    graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
    assuntos = graph.run('''MATCH p=(n:Item {isbn:"''' + item + '''"})-[r:PERTENCE_AO_ASSUNTO]->(m:Assunto) RETURN m.assunto''').data()
    return assuntos

def createRelUsuarioAssunto(usuario, assunto):
  graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
  #item_titulo = properties_dict["titulo"]
  matcher = NodeMatcher(graph)
  m = matcher.match("Usuário", usuario=usuario).first()
  n = matcher.match("Assunto", assunto=assunto).first()
  rel = Relationship(m, "TEM_PREFERÊNCIA_POR", n)
  graph.create(rel)

usuarios = [2044,
7786,
9082,
20029,
6644,
890,
6943,
4811,
6943,
4544,
2106]


assuntos = assuntos_item("20170626125500.0")
assuntos_list = []
for assunto in assuntos:
    assuntos_list.append(assunto['m.assunto'])
print(assuntos_list)

for usr in usuarios:
    createUsuario(usr)
    createRelEmprestimo(usr,"20170626125500.0")
    for assunto in assuntos_list:
        createRelUsuarioAssunto(usr, assunto)