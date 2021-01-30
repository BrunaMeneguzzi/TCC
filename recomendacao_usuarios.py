import py2neo
from py2neo import Graph, Node, Relationship, NodeMatcher, Relationship
import xml.etree.ElementTree as ET

graph = Graph("http://localhost:11009/db/data/", user="neo4j", password="senha")

def allUsers():
    #retorna todos os usuarios do grafo
    users = graph.run('''MATCH (n:Usuário) RETURN n''').data()
    return users

def allItens():
    itens = graph.run('''MATCH (n:Item) RETURN n.isbn''').data()
    return itens

def autores_primarios_comum(item, user):
    autores_list = []
    autores = graph.run('''MATCH (n:`Usuário` {usuario: '''+str(user)+'''}), (m:Item), (j:Autor) 
    WHERE (n)-[:PEGOU_EMPRESTADO]-(m) and (j)-[:`É_AUTOR_DE`]-(m) RETURN m.titulo, j.nome''').data()
    autor_item = graph.run('''MATCH (n:Item {isbn:"'''+item+'''"}), (m:Autor) 
    WHERE (m)-[:`É_AUTOR_DE`]-(n) RETURN m.nome''').data()
    autor_item = autor_item[0]['m.nome']
    for autor in autores:
        autor = autor['j.nome']
        if autor == autor_item:
            return 1
        else:
            return 0

def autores_secundarios_comum(item, user):
    count = 0
    # autores secundários de itens que o usuário já pegou emprestado
    autores_user_list = []
    autores = graph.run('''MATCH (n:`Usuário` {usuario: '''+str(user)+'''}), (m:Item), (j:`Autor Secundário`) 
    WHERE (n)-[:PEGOU_EMPRESTADO]-(m) and (j)-[:`É_AUTOR_SECUNDÁRIO_DE`]-(m) RETURN m.titulo, j.nome''').data()
    if autores == []:
        return 0
    for autor in autores:
        autor = autor['j.nome']
        autores_user_list.append(autor)
    print("Autores secundários:",autores_user_list)
    # autores secundários do item
    autores_item_list = []  
    autor_item = graph.run('''MATCH (n:Item {isbn:"'''+item+'''"}), (m:`Autor Secundário`) 
    WHERE (m)-[:`É_AUTOR_SECUNDÁRIO_DE`]-(n) RETURN m.nome''').data()
    if autor_item == []:
        return 0
    for autor1 in autor_item:
        autor1 = autor1['m.nome']
        autores_item_list.append(autor1)
    print("Lista de autores secundários user: ", autores_user_list)
    print("Lista de autores secundários item: ", autores_item_list)
    for autor in autores_user_list:
        for autor1 in autores_item_list:
            if autor == autor1:
                count += 1
    return count

def termo_titulo(item, user):
    titulo = graph.run('''MATCH (n:Item {isbn:"''' + item + '''"}) RETURN n.titulo''').data()
    titulo = titulo[0]['n.titulo']
    print("Titulo = ", titulo)
    itens = graph.run('''CALL db.index.fulltext.queryNodes("itens", "'''+titulo+'''") 
    YIELD node, score MATCH (m:Usuário {usuario:'''+str(user)+'''}), (n:Item {titulo:node.titulo})
    WHERE (m)-[:PEGOU_EMPRESTADO]-(n) RETURN node.titulo, score ORDER BY score DESC''').data()
    if itens == []:
        return 0
    else:
        return 1

def usuarios_parecidos(item, user):
    #print(item)
    # retorno todos os assuntos que o usuário gosta
    assuntos_user = []
    assuntos = graph.run('''MATCH (u:`Usuário` {usuario:'''+str(user)+'''}), (i:Assunto) 
    WHERE (u)-[:`TEM_PREFERÊNCIA_POR`]-(i) RETURN i.assunto''').data()
    for assunto in assuntos:
        assuntos_user.append(assunto['i.assunto'])
    #print("assuntos_user: ",assuntos_user)
    # vejo quais outros usuários gostam desses mesmos assuntos
    usuarios_list = []
    for assunto in assuntos_user:
        usuario_list = []
        usuarios = graph.run('''MATCH (a:Assunto {assunto:"'''+assunto+'''"}), (u:`Usuário`) 
        WHERE (u)-[:`TEM_PREFERÊNCIA_POR`]-(a) RETURN u.usuario''').data()
        for usuario in usuarios:
            usuario_list.append(usuario['u.usuario'])
        usuarios_list += usuario_list
    #print(usuarios_list)
    usuarios_list = sorted(set(usuarios_list))
    #print(len(usuarios_list))
    # vejo quais itens esses usuarios ja pegaram emprestado
    itens_total = []
    for dict_user in usuarios_list:
        #print(dict_user)
        itens_do_usuario = graph.run('''MATCH (n:Item), (m:`Usuário` {usuario:'''+str(dict_user)+'''}) 
        WHERE (m)-[:PEGOU_EMPRESTADO]-(n) RETURN n.isbn''').data()
        for item2 in itens_do_usuario:
            #print(item2)
            itens_total.append(item2['n.isbn'])
    #print(itens_total)
    # vejo se o item em questão é algum desses itens
    count_itens = 0
    for item_user in itens_total:
        #print(type(item))
        #print(type(item_user))
        if item_user == item: 
            count_itens += 1
    # retorno o numero de vezes que o item aparece nessa lista (quantidade de usuarios que pegaram emprestado)
    return count_itens

def createRelItemUser(properties, user, score):
  graph = Graph("http://localhost:11009/db/data/", user="neo4j", password="senha")
  matcher = NodeMatcher(graph)
  m = matcher.match("Item", isbn=properties).first()
  n = matcher.match("Usuário", usuario=user).first()
  rel = Relationship(n, "PODE_INTERESSAR_A", m, score=score)
  graph.create(rel)

usuario = "7514"
# items = allItens()
# for item in items:
#     isbn = item['n.isbn']
#     assuntos_comum = graph.run('''MATCH (n:`Usuário` {usuario:''' + usuario + '''}), 
#     (m:Item {isbn: "''' + isbn + '''"}), (a:Assunto) WHERE (n)-[:`TEM_PREFERÊNCIA_POR`]-(a) AND 
#     (m)-[:PERTENCE_AO_ASSUNTO]-(a) RETURN a.assunto''').data()
#     assuntos_comum = len(assuntos_comum)
#     print("AC = ",assuntos_comum)
#     # verifica se o item tem como autor algum autor de algum item que o usuário pegou emprestado
#     parecidos = usuarios_parecidos(isbn, usuario)
#     print("parecidos = ", parecidos)
#     score = (2*assuntos_comum + 1*parecidos)
#     print("score = ", score)
#     if score > 0.0:
#         createRelItemUser(isbn, int(usuario), score)

result = graph.run('''MATCH (n:Item), (m:`Usuário` {usuario:'''+usuario+'''}), 
(n)-[r:PODE_INTERESSAR_A]-(m) RETURN n.titulo, r.score ORDER BY r.score DESC LIMIT 10''').data()
for resultado in result:
    print(resultado)

# for user in users:
#     print(user)
#     user = dict(user['n'])
#     itens = []
#     usuario = str(user['usuario'])
#     assuntos = graph.run('''MATCH p=(n:`Usuário` {usuario:''' + usuario + '''})-[r:`TEM_PREFERÊNCIA_POR`]->(m:Assunto) RETURN m.assunto''').data()
#     #print(assuntos)
#     for assunto in assuntos:
#         assunto = assunto['m.assunto']
#         itens1 = graph.run('''MATCH p=(n:Item)-[r:PERTENCE_AO_ASSUNTO]->(m:Assunto {assunto:"''' + assunto + '''"}), (u:`Usuário`)-[s:PEGOU_EMPRESTADO]->(n) RETURN DISTINCT n.titulo''').data()
#     for item1 in itens1:
#         itens.append(item1['n.titulo'])
#     print(itens[:10])

# COMO PRIORIZAR ITENS QUE JÁ FORAM PEGOS
# MATCH p=(n:Item)-[r:PERTENCE_AO_ASSUNTO]->(m:Assunto {assunto:"CONTO"}), q=(u:`Usuário`)-[s]->(n) WHERE s IS NOT "PEGOU_EMPRESTADO" RETURN DISTINCT n.titulo
# COMO RETIRAR AQUELES QUE O USUARIO JA PEGOU EMPRESTADO
# MATCH (j:Usuário {usuario:8493}), (n:Item)-[r:PERTENCE_AO_ASSUNTO]->(m:Assunto {assunto:"LITERATURA"}), (j)-[s:PEGOU_EMPRESTADO]->(n) WHERE NOT EXISTS s RETURN n.titulo