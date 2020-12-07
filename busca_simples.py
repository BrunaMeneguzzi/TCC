import py2neo
from py2neo import Graph, Node, Relationship, NodeMatcher, Relationship
import xml.etree.ElementTree as ET

graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="senha")

mytree = ET.parse('SAV1431425.xml')
myroot = mytree.getroot()

#graph.run('''CALL db.index.fulltext.createNodeIndex("busca_simples",["Titulo", "Autor", "Biblioteca"],["titulo", "nome", "biblioteca"])''')
#graph.run('''CALL db.index.fulltext.createNodeIndex("busca_titulo",["Titulo", "Autor", "Biblioteca"],["titulo", "nome", "biblioteca"])''')
#graph.run('''CALL db.index.fulltext.createNodeIndex("busca_simples_autor",["Autor"],["nome"])''')
#graph.run('''CALL db.index.fulltext.createNodeIndex("busca_simples_biblioteca",["Biblioteca"],["biblioteca"])''')

def busca_simples_titulo(termo):
    titulos = []
    nodes = graph.run('''CALL db.index.fulltext.queryNodes("itens", "''' + termo + '''") 
    YIELD node, score RETURN node.titulo, score ORDER BY score DESC''').data()
    for node in nodes:
        titulos.append(node['node.titulo'])
    return titulos

def busca_simples_autor(termo):
    # preciso retornar os itens em que esse autor é autor
    autores = []
    itens = []
    titulos = []
    nodes = graph.run('''CALL db.index.fulltext.queryNodes("busca_simples_autor", "''' + termo + '''") 
    YIELD node, score RETURN node.nome, score ORDER BY score DESC''').data()
    for node in nodes:
        autores.append(node['node.nome'])
    for autor in autores:
        #print(autor)
        itens_do_autor = graph.run('''MATCH p=(n:Autor {nome:"''' + autor +  '''"})-[r:É_AUTOR_DE]->(m:Item) RETURN m.titulo''').data()
        for item in itens_do_autor:
            titulo = item['m.titulo']
            titulos.append(titulo)
    return titulos


# uma função que recebe uma lista de campos para a busca
# OU - campos
# chamar mais de uma das funções -> juntar os resultados -> ordenar 

def busca_simples_biblioteca(termo):
    # preciso retornar os itens em que esse autor é autor
    bibliotecas = []
    lista_itens = []
    nodes = graph.run('''CALL db.index.fulltext.queryNodes("busca_simples_biblioteca", "''' + termo + '''") 
    YIELD node, score RETURN node.biblioteca, score ORDER BY score DESC''').data()
    for node in nodes:
        biblioteca = node['node.biblioteca']
        bibliotecas.append(biblioteca)
    #print(bibliotecas)
    for bib in bibliotecas:
        items = graph.run('''MATCH p=(m:Item)-[r:`ESTÁ_ALOCADO_EM`]->(n:Biblioteca {biblioteca:"''' + bib + '''"}) RETURN m.titulo ORDER BY m.titulo LIMIT 10''').data()
        for item in items:
            lista_itens.append(item["m.titulo"])
    return lista_itens

def busca_simples(termo):
    titulo = busca_simples_titulo(termo)
    print(titulo)
    autor = busca_simples_autor(termo)
    print(autor)
    biblioteca = busca_simples_biblioteca(termo)
    print(biblioteca)
    lista = titulo + autor + biblioteca
    return lista

def busca(termo):
    busca = []
    nodes = graph.run('''CALL db.index.fulltext.queryNodes("busca_simples", "''' + termo + '''") 
    YIELD node, score RETURN node.titulo, score ORDER BY score DESC''').data()
    for node in nodes:
        busca.append(node['node.titulo'])
    return busca

#print(busca("tempo"))
print(busca_simples("Ribeiro"))

# def busca_simples_usuario():
#     lista_itens = busca_simples_titulo("Mulher")
#     for item in lista_itens:

#print(busca_simples_autor("Carvalho"))

# print("Busca simples por título:")
# print(busca_simples_titulo("Libertinagem"))
# print(busca_simples_titulo("Meireles"))
# print(busca_simples_titulo("Mulher"))
# print(busca_simples_titulo("tempo"))
# print("Busca simples por autor:")
# print(busca_simples_autor("Carvalho"))
# print("----")
# print("----")
# busca_simples_autor("Ribeiro")
# print("----")
# busca_simples_autor("Ana Paula Pacheco")
#print(busca_simples_biblioteca("IEB"))
#print(busca_simples_usuario())