import py2neo
from py2neo import Graph, Node, Relationship, NodeMatcher

graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")

def createUsuario(usuario):
    graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
    nodename = Node('Usuário', usuario=usuario)
    graph.create(nodename)

def createRelUsuarioAssunto(usuario, assunto):
  graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")
  #item_titulo = properties_dict["titulo"]
  matcher = NodeMatcher(graph)
  m = matcher.match("Usuário", usuario=usuario).first()
  n = matcher.match("Assunto", assunto=assunto).first()
  rel = Relationship(m, "TEM_PREFERÊNCIA_POR", n)
  graph.create(rel)

usr = input("Digite seu usuário:")
createUsuario(usr)
print("Dados os seguintes assuntos, escolha o que mais lhe interessa:")
nodes = graph.run("MATCH (a:Assunto) RETURN a.assunto").data()
print(nodes)
assunto_esc = input()
createRelUsuarioAssunto(usr, assunto_esc)
