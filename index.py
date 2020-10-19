import py2neo
from py2neo import Graph, Node, Relationship

graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")

#graph.run('''CALL db.index.fulltext.createNodeIndex('itens', ['Item'], ['titulo'], {analyzer: "brazilian"})''')


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
#index_itens("folklore")

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

