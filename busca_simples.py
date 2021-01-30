import py2neo
from py2neo import Graph, Node, Relationship, NodeMatcher, Relationship
import xml.etree.ElementTree as ET

graph = Graph("http://localhost:11009/db/data/", user="neo4j", password="senha")

#graph.run('''CALL db.index.fulltext.createNodeIndex("busca_simples2",["Item", "Autor", "Biblioteca"],["titulo", "nome", "biblioteca"])''')
#graph.run('''CALL db.index.fulltext.createNodeIndex("busca_titulo",["Item"],["titulo"],{analyzer: "brazilian"})''')
#graph.run('''CALL db.index.fulltext.createNodeIndex("busca_simples_autor",["Autor"],["nome"])''')
#graph.run('''CALL db.index.fulltext.createNodeIndex("busca_simples_biblioteca",["Biblioteca"],["biblioteca"],{analyzer: "brazilian"})''')

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
        print(autor)
        itens_do_autor = graph.run('''MATCH p=(n:Autor {nome:"''' + autor +  '''"})-[r:É_AUTOR_DE]->(m:Item) RETURN m.titulo''').data()
        for item in itens_do_autor:
            titulo = item['m.titulo']
            titulos.append(titulo)
    return titulos[0:10]


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
        items = graph.run('''MATCH p=(m:Item)-[r:`ESTÁ_ALOCADO_EM`]->(n:Biblioteca {biblioteca:"''' + bib + '''"}) 
        RETURN m.titulo LIMIT 10''').data()
        for item in items:
            lista_itens.append(item["m.titulo"])
    return lista_itens

def itens_biblioteca(termo):
    lista_resultado = []
    item = busca_simples_titulo(termo)
    item = item[0]
    biblioteca = graph.run('''MATCH (n:Item {titulo:"''' + item + '''"}), (b:Biblioteca) 
    WHERE (n)-[:`ESTÁ_ALOCADO_EM`]-(b) RETURN b.biblioteca''').data()
    biblioteca = biblioteca[0]['b.biblioteca']
    #print("Biblioteca = ", biblioteca)
    result = graph.run('''MATCH (n:Item), (m:Biblioteca {biblioteca:"''' + biblioteca + '''"}) 
    WHERE (n)-[:`ESTÁ_ALOCADO_EM`]-(m) RETURN n.titulo LIMIT 10''').data()
    for resultado in result:
        resultado = resultado['n.titulo']
        lista_resultado.append(resultado)
    return lista_resultado

def busca_simples(termo):
    titulo = busca_simples_titulo(termo)
    #print(titulo)        
    autor = busca_simples_autor(termo)
    #print(autor)
    biblioteca = busca_simples_biblioteca(termo)
    #print(biblioteca)
    itens = itens_biblioteca(termo)
    #print(itens)
    lista = titulo + autor + biblioteca + itens
    return lista[0:10]

def busca(termo):
    busca = []
    nodes = graph.run('''CALL db.index.fulltext.queryNodes("busca_simples", "''' + termo + '''") 
    YIELD node, score RETURN node.titulo, score ORDER BY score DESC''').data()
    for node in nodes:
        busca.append(node['node.titulo'])
    return busca

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
    #print(itens)

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

def busca_complexa(item, user):
    lista = []
    list_result = busca_simples(item)
    recomendacoes = dict()
    for rec in list_result:
        recomendacoes[rec] = 0.0
    print(recomendacoes)
    usuario = graph.run('''MATCH (n:Usuário {usuario:''' + user + '''}) RETURN n.usuario''').data()
    usuario = usuario[0]['n.usuario']
    #print("Usuário = ",usuario)
    i=0
    for result in list_result:
        isbn = graph.run('''MATCH (n:Item {titulo:"''' + result + '''"}) RETURN n.isbn''').data()
        isbn = isbn[0]['n.isbn']
        # verifica se o item tem algum assunto em comum com as preferências do usuário
        assuntos_comum = graph.run('''MATCH (n:`Usuário` {usuario:''' + user + '''}), 
        (m:Item {isbn: "''' + isbn + '''"}), (a:Assunto) WHERE (n)-[:`TEM_PREFERÊNCIA_POR`]-(a) AND 
        (m)-[:PERTENCE_AO_ASSUNTO]-(a) RETURN a.assunto''').data()
        assuntos_comum = len(assuntos_comum)
        print("AC = ",assuntos_comum)
        # verifica se o item tem como autor algum autor de algum item que o usuário pegou emprestado
        # autor primário
        autor_primario_comum = autores_primarios_comum(isbn,usuario)
        print("APC = ",autor_primario_comum)
        # autor secundário
        autores_secundarios = autores_secundarios_comum(isbn,usuario)
        print("ASC = ", autores_secundarios)
        # verifica se o item tem no titulo algum termo que tenha nos titulos dos itens 
        # que o usuario ja pegou emprestado
        termo = termo_titulo(isbn, usuario)
        print("TT = ", termo)
        parecidos = usuarios_parecidos(isbn, usuario)
        print("parecidos = ", parecidos)
        score = (2*assuntos_comum + 1*autor_primario_comum + 1*autores_secundarios + 2*termo + 1*parecidos)
        print(score)
        recomendacoes[result] = score
    return recomendacoes
        

#print(busca("tempo"))
#print(busca_complexa("Mulher", "1155"))
#print(busca_complexa("Atlas", "6668"))
print(busca_simples("Alencar"))
#print(busca_simples("Romances brasileiros modernos"))
#print(busca_complexa("Romances brasileiros modernos", "22388"))
#print(usuarios_parecidos("8581641390","22388"))
#print(busca_complexa("Romances brasileiros modernos", "19135"))

#print(autores_secundarios_comum("9788563604019", "1155"))