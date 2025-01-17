from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.by import By

inicio = time.time()

itens = ["Primeiras estórias", 
"O rito e o tempo : ensaios sobre o carnaval", 
"Urbanismo em fim de linha : e outros estudos sobre o colapso da modernização arquitetônica", 
"Os arquétipos literários", 
"O espaço do cidadão", 
"Espaço e método", 
"Mulheres de papel : um estudo do imaginário em José de Alencar e Machado de Assis", 
"Molde nacional e fôrma cívica : higiene, moral e trabalho no projeto da Associação Brasileira de", 
"Pontos e bordados : escritos de história e política", 
"Mecenato pombalino e poesia neoclássica : Basílio da Gama e a poética do encômio", 
"Diário íntimo", 
"Bang", 
"Metamorfoses do espaço habitado : fundamentos teóricos e metodológicos da geografia", 
"Quem tem medo da geopolítica?", 
"Carnavais, Malandros E Herois : Para Uma Sociologia Do Dilema Brasileiro", 
"Poesia e prosa completas", 
"A carne, a morte e o diabo na literatura romântica", 
"Entre a mão e os anéis : a Lei dos Sexagenários e os caminhos da abolição no Brasil", 
"A arte de descrever : a arte holandesa no século XVII", 
"A nação como artefato : deputados do Brasil nas cortes portuguesas (1821-1822)", 
"Coroas de glória, lágrimas de sangue : a rebelião dos escravos de Demerara em 1823 / c Emilia Vio", 
"Figurações Brasil anos 60 : neofigurações fantásticas e neo-surrealismo, novo realismo e nova o", 
"Nem tudo era italiano : São Paulo e pobreza, 1890-1915", 
"1930 : a crítica e o Modernismo", 
"Por uma outra globalização : do pensamento único à consciência universal", 
"A paixão segundo GH : romance", 
"Metamorfoses do mal : uma leitura de Clarice Lispector", 
"Na senzala, uma flor : esperanças e recordações na formação da família escrava - Brasil Sudest", 
"A vida dos escravos no Rio de Janeiro (1808-1850)", 
"A sociedade do espetáculo : comentários sobre a sociedade do espetáculo", 
"A educação pela pedra e depois", 
"Variedades de história cultural", 
"As artes de enganar : um estudo das máscaras poéticas e biográficas de Gregorio de Mattos", 
"As cidades na economia mundial", 
"Cecília Meireles : o mundo contemplado", 
"Construçao da nação e escravidão no pensamento de José Bonifácio, 1783-1823", 
"Macunaíma : o herói sem nenhum caráter", 
"O problema da consciência histórica", 
"Realismo, racionalismo, surrealismo : a arte no entre-guerras", 
"A casa dos espíritos", 
"A vagabunda", 
"A via crucis do corpo", 
"A Legião Estrangeira", 
"Felicidade clandestina : contos", 
"Água viva : ficção", 
"O antropólogo e sua magia : trabalho de campo e texto etnográfico nas pesquisas antropológicas so", 
"A leitora Clarice Lispector", 
"Memória do fogo", 
"Um espaço para a ciência : a formação da comunidade científica no Brasil", 
"A solidão povoada", 
"Homens livres na ordem escravocrata", 
"O trato dos viventes : formação do Brasil no Atlântico Sul, séculos XVI e XVII", 
"Dialética da colonização", 
"História concisa do Brasil", 
"Morte e alteridade em Estas estórias", 
"Por uma nova história urbana", 
"Templos de civilização : a implantação da escola primária graduada no estado de São Paulo (189", 
"O dialeto caipira : gramática, vocabulário", 
"Bom-Crioulo", 
"Dom Casmurro", 
"Navegantes, bandeirantes, diplomatas : um ensaio sobre a formação das fronteiras do Brasil", 
"Roteiro de Macunaíma", 
"Marco Zero", 
"Historia social do jazz", 
"O diabo : a máscara sem rosto", 
"A donzela-guerreira : um estudo de gênero", 
"História das inquisições : Portugal, Espanha e Itália - séculos XV-XIX", 
"Fluxo-floema", 
"Gramática de usos do português", 
"Itinerário político do romance pós-64 : a festa", 
"Manual do agricultor brasileiro", 
"A república mundial das letras", 
"Da fera à Loira : sobre contos de fadas e seus narradores", 
"A urbanização brasileira", 
"A Berlim de Bertold Brecht : um álbum dos anos 20", 
"Memória em branco e negro : olhares sobre São Paulo", 
"Dorival Caymmi : o mar e o tempo", 
"Impressões de um amador : textos esparsos de crítica, 1882-1909", 
"Os olhos do império : relatos de viagem e transculturação", 
"Olhos de madeira : nove reflexões sobre a distância", 
"Tradição e modernidade : Afonso Schmidt e a literatura paulista, 1906-1928", 
"Raízes do riso : a representação humorística na história brasileira da Belle Époque aos primei", 
"Textos de intervenção", 
"Drummond : da Rosa do povo à rosa das trevas", 
"A guerra dos bárbaros : povos indígenas e a colonização do sertão nordeste do Brasil, 1650-1720", 
"Literatura e resistência", 
"José de Alencar : o poeta armado do século XIX", 
"Oliver Twist", 
"Metafísica", 
"Caos e governabilidade no moderno sistema mundial", 
"Sinta o drama", 
"Antologia ilustrada dos cantadores", 
"Homo sacer : o poder soberano e a vida nua I", 
"O Otelo brasileiro de Machado de Assis : um estudo de Dom Casmurro", 
"Escritos urbanos", 
"Ilíada de Homero", 
"Céu, inferno : ensaios de crítica literária e ideológica", 
"Grande sertão : veredas", 
"O império marítimo português 1415-1825", 
"Mímesis : desafio ao pensamento", 
"Um mestre na periferia do capitalismo : Machado de Assis", 
"A década do impasse : da Rio-92 à Rio+10", 
"Por uma geografia nova : da crítica da geografia a uma geografia crítica", 
"A epopéia bandeirante : letrados, instituições, invenção histórica, 1870-1940", 
"O mundo de Homero", 
"Primeiras trovas burlescas & outros poemas", 
"Leituras 2 : a regiao dos filosofos", 
"Palavra, imagem e poder : o surgimento da imprensa no Brasil do século XIX", 
"Semana de 22 : entre vaias e aplausos", 
"Carlos & Mário : correspondência completa entre Carlos Drummond de Andrade (inédita) e Mário de", 
"O discurso filosófico da modernidade : doze lições", 
"Os carrascos voluntários de Hitler : o povo alemão e o Holocausto", 
"Poesias completas", 
"A loucura de Isabella e outras comédias da Commedia Dell'Arte", 
"Literatura oral para a infância e a juventude : lendas, contos & fábulas populares no Brasil", 
"O folclore em questão", 
"Os domínios de natureza no Brasil : potencialidades paisagísticas", 
"O velho mundo desce aos infernos : auto-análise da modernidade após o trauma de junho de 1848 em P", 
"Terra, trabalho e poder : o mundo dos engenhos no Nordeste colonial", 
"Poesías completas", 
"Ficção científica, fantasia e horror no Brasil, 1875 a 1950", 
"O rei da vela", 
"Noite e musica na poesia de Carlos Drummond de Andrade", 
"Portugal e Brasil na crise do antigo sistema colonial (1777-1808)", 
"Cartas a um jovem escritor e suas respostas", 
"Rebelião escrava no Brasil : a história do levante dos Malês em 1835", 
"Sociologia e antropologia", 
"O tupi e o alaúde : uma interpretação de Macunaíma", 
"Correspondência com seu tradutor alemão Curt Meyer-Clason (1958-1967)", 
"Na trilha do Jeca : Monteiro Lobato e a formação do campo literário no Brasil", 
"Bim bom : a contradição sem conflitos de João Gilberto", 
"Ariel", 
"Libertinagem : Estrela da manhã : edição crítica", 
"Poesia completa : conforme as disposições do autor", 
"Relatório Cruls : Relatório da Comissão Exploradora do Planalto Central do Brasil", 
"A Casa de Dona Yay", 
"América Latina no século XIX : tramas, telas e textos", 
"Iemanjá & Oxum : iniciações, Ialorixás e Olorixás", 
"Contra-revolução e revolta", 
"A natureza do espaço : técnica e tempo, razão e emoção", 
"O espaço dividido : os dois circuitos da economia urbana dos paises subdesenvolvidos", 
"O tempo Saquarema : a formação do estado imperial", 
"Teorias da arte moderna", 
"Machado de Assis, historiador", 
"O cancioneiro de Lésbia", 
"Formas breves", 
"O rei ausente : festa e cultura política nas visitas dos Filipes a Portugal (1581 e 1619)", 
"Ponta de lança", 
"Kant e o fim da metafísica", 
"A ficção da escrita", 
"Trovar claro : poemas", 
"Páginas de sensação : literatura popular e pornográfica no Rio de Janeiro ( 1870-1924)", 
"Correspondências", 
"A pintura da vida moderna : Paris na arte de Manet e seus seguidores", 
"A dominação masculina", 
"As palavras e a Lei : direito, ordem e justiça na história do pensamento jurídico moderno", 
"Noturno do Chile", 
"Testemunha ocular : história e imagem", 
"O romantismo e a idéia de nação no Brasil (1830-1870)", 
"Esquecidos e renascidos : historiografia acadêmica luso-americana, 1724-1759", 
"Grandesertãobr : o romance de formação do Brasil", 
"Desclassificados do ouro : a pobreza mineira no século XVIII", 
"Planejamento e zoneamento : São Paulo 1947-1972", 
"A formação da antropologia americana 1883-1911 : antologia", 
"A interiorização da metrópole e outros estudos", 
"A outra Independência : o federalismo pernambucano de 1817 a 1824", 
"Segredos guardados : orixás na alma brasileira", 
"A história", 
"Escritura e nomadismo : entrevistas e ensaios", 
"Noções de analise histórico-literária", 
"Lembranças de São Paulo : o interior paulista nos cartões-postais e álbuns de lembranças", 
"O primo Basílio : Texto integral", 
"A urbanização brasileira", 
"Literatura e sociedade : estudos de teoria e história literária", 
"Da totalidade ao lugar", 
"Ficções de fundação : os romances nacionais da América Latina", 
"Forças armadas e política no Brasil", 
"A sátira e o engenho : Gregório de Matos e a Bahia do século XVII", 
"Guimarães Rosa e a psicanálise : ensaios sobre imagem e escrita", 
"Elementos de retórica literária", 
"Em busca do tempo perdido", 
"Razão da recusa : um estudo da poesia de Carlos Drummond de Andrade", 
"Os excluídos do reino : a Inquisição portuguesa e o degredo para o Brasil colônia", 
"Brigada ligeira", 
"Rosa em 2 tempos", 
"Aproximações : estudos de história e historiografia", 
"Música do parnaso : edição fac-similar (1705-2005)", 
"Castro Alves", 
"Poemas escolhidos", 
"Ignorância do sempre", 
"Torquatália", 
"Estética : literatura e pintura, música e cinema", 
"Lugar do mito : narrativa e processo social nas Primeiras estórias de Guimarães Rosa", 
"O Brasil nas letras de um pintor : Manuel de Araújo Porto Alegre (1806-1879)", 
"Arquitetura do século XX e outros escritos : Gregori Warchavchik", 
"História Ficçao Literatura", 
"Há uma gota de sangue em cada Museu : a ótica museológica de Mário de Andrade", 
"Passos de Drummond", 
"A ecologia de Marx : materialismo e natureza", 
"Autonomia e parceria : estados e transformação industrial", 
"Portugal e Brasil na crise do antigo sistema colonial (1777-1808)", 
"O paraíso destruído", 
"A idéia de história", 
"Lavoura arcaica", 
"Primeiras estórias", 
"O último leitor", 
"Corpo de baile", 
"Sagarana", 
"O Brasil de Rosa : mito e história no universo rosiano : o amor e o poder", 
"Tantas palavras", 
"O sol e a sombra : política e administração na América Portuguesa do século XVIII", 
"Teoria da poesia concreta : textos críticos e manifestos 1950-1960", 
"A formação do romance inglês : ensaios teóricos", 
"Como eles agiam : os subterrâneos da ditadura militar : espionagem e polícia política", 
"Tempo passado : cultura da memória e guinada subjetiva", 
"Formação da literatura brasileira : momentos decisivos 1750-1880", 
"Em defesa da sociedade : curso no Collège de France (1975-1976)", 
"O local da diferença : ensaios sobre memória, arte, literatura e tradução", 
"A metáfora viva", 
"Moderno e Brasileiro : a história de uma nova linguagem na arquitetura (1930-60)", 
"A síncope das idéias : a questão da tradição na música popular brasileira", 
"Lundu do escritor díficil : canto nacional e fala brasileira na obra de Mário de Andrade", 
"Dialética do esclarecimento : fragmentos filosóficos", 
"Conceitos fundamentais da história da arte : o problema da evolução dos estilos na arte mais rece", 
"Machado de Assis : o enigma do olhar", 
"Nas malhas da consciência : Igreja e Inquisição no Brasil : Nordeste 1640-1750", 
"Redes de criação : construção da obra de arte", 
"Ver a terra : seis ensaios sobre a paisagem e a geografia", 
"Antônio Vieira e o Império universal : a Clavis prophetarum e os documentos inquisitoriais", 
"A Europa : gênese de uma civilização", 
"Versificação portuguesa", 
"Estudos de literatura brasileira e portuguesa", 
"A educação pela noite", 
"Literatura e sociedade", 
"Formação econômica do Brasil", 
"Em defesa da honra : moralidade, modernidade e nação no Rio de Janeiro (1918-1940)", 
"Não verás país nenhum : memorial descritivo", 
"Ser escravo no Brasil", 
"Folhetim : uma história", 
"Clarice Lispector com a ponta dos dedos", 
"Minhas queridas", 
"Fragmentos setecentistas : escravidão, cultura e poder na América portuguesa", 
"50 poemas escolhidos pelo autor", 
"Ensaios de literatura ocidental : filologia e crítica", 
"As américas e a civilização : processo de formação histórica e causas do desenvolvimento desig", 
"A jangada de pedra", 
"Macunaíma, o herói sem nenhum caráter", 
"África e Brasil africano", 
"O primo Basílio na imprensa brasileira do século XIX : estética e história", 
"Pensamento e lirismo puro na poesia de Cecília Meireles", 
"Mínima mímica : ensaios sobre Guimarães Rosa", 
"Soldados da pátria : história do Exército Brasileiro, 1889-1937", 
"O vôo da Embraer : a competitividade brasileira na indústria de alta tecnologia", 
"Tese e antítese", 
"Formação da literatura brasileira : momentos decisivos 1750-1880", 
"Teresina etc", 
"Ficção e confissão : ensaios sobre Graciliano Ramos", 
"Marília de Dirceu", 
"Quincas Borba", 
"Dom Casmurro", 
"Uma história da cidade da Bahia", 
"Brancos e negros em São Paulo : ensaio sociológico sobre aspectos da formação, manifestações a", 
"O negro no mundo dos brancos", 
"A experiência do tempo : conceitos e narrativas na formação nacional brasileira (1813-1845)", 
"Guimarães Rosa : fronteiras, margens, passagens", 
"Geografia política da água", 
"A economia latino-americana : formação histórica e problemas contemporâneos", 
"Espaço e método", 
"Armazém literário : ensaios", 
"Manuel Bandeira e a música : com três poemas visitados", 
"Domingos Sodré, um sacerdote africano : escravidão, liberdade e candomblé na Bahia do século XIX", 
"Profissão artista : pintoras e escultoras acadêmicas brasileiras", 
"Arqueologia das ciências e história dos sistemas de pensamento", 
"A retórica de Rousseau e outros ensaios", 
"Antropologia cultural", 
"O bumba-boi maranhense em São Paulo", 
"Antropologia estrutural", 
"A formação da classe operária inglesa", 
"Cinematógrafo de letras : literatura, técnica e modernização no Brasil", 
"Comunidades imaginadas : reflexões sobre a origem e a difusão do nacionalismo", 
"Ser-tão natureza : a natureza em Guimarães Rosa", 
"Riso e melancolia : a forma shandiana em Sterne, Diderot, Xavier de Maistre, Almeida Garrett e Macha", 
"Dificuldades da língua Portuguêsa : estudos e observaçoes", 
"Leréias : (historias contadas por eles mesmos)", 
"Veneno remédio : o futebol e o Brasil", 
"Metamorfoses do espaço habitado : fundamentos teóricos e metodológicos da geografia", 
"Noções de paleografia e de diplomática", 
"Uma história da música popular brasileira : das origens à modernidade", 
"O artista inconfessável", 
"História de Antônio Vieira", 
"O direito de sonhar", 
"Pequeno guia histórico das livrarias brasileiras", 
"Obra completa em quatro volumes", 
"A formação do mercado de trabalho no Brasil", 
"A integração do negro na sociedade de classes", 
"Modernismo : o fascínio da heresia de Baudelaire a Beckett e mais um pouco", 
"A invenção do Nordeste e outras artes", 
"Adam Smith em Pequim : origens e fundamentos do século XXI", 
"A literatura através do cinema : realismo magia e a arte da adaptação", 
"Introdução à sociologia : (1968)", 
"Cultura com aspas : e outros ensaios", 
"Hermenêutica e ideologias", 
"Dialética negativa", 
"A arte de escrever : sobre a erudição e os eruditos  pensar por si mesmo  sobre a escrita e o es", 
"Poesia completa e prosa : volume único", 
"Os sertões : (Campanha de Canudos)", 
"Teoria da vanguarda", 
"O guarani", 
"Metalinguagem & outras metas : ensaios de teoria e crítica literária", 
"Escritos sobre teatro", 
"Línguas, poetas e bacharéis : uma crônica da tradução no Brasil", 
"Ensaios reunidos : escritos sobre Goethe", 
"A biblioteca esquecida de Hitler : os livros que moldaram a vida do Führer", 
"As meninas", 
"Natureza e cultura no Brasil (1870-1922)", 
"Machado de Assis e a crítica internacional", 
"Dos canibais", 
"Semiótica à luz de Guimarães Rosa", 
"Civilização material, economia e capitalismo séculos XV-XVIII", 
"Educação e emancipação", 
"Estratégia, poder-saber", 
"João do Rio", 
"Vigiar e punir : nascimento da prisão", 
"Notas de literatura I", 
"Nísia Floresta : vida e obra", 
"Câmara Cascudo e Mário de Andrade : cartas, 1924-1944", 
"A vida social das coisas : as mercadorias sob uma perspectiva cultural", 
"O guardador de segredos : ensaios", 
"Contos completos", 
"A investigação etnológica no Brasil e outros ensaios", 
"A revolta da vacina : mentes insanas em corpos rebeldes", 
"Escritos urbanos", 
"A memória, a história, o esquecimento", 
"História da sexualidade 1 : a vontade de saber", 
"Resumo dos Cursos do Collège de France 1970-1982", 
"O corpo da liberdade : reflexões sobre a pintura do século XIX", 
"Cores de Rosa", 
"O altar & o trono : dinâmica do poder em O alienista", 
"Ficção completa em dois volumes", 
"Geografias pós-modernas : a reafirmação do espaço na teoria social crítica", 
"O trabalho do geógrafo no terceiro mundo", 
"Mitos, emblemas, sinais : morfologia e história", 
"Falando da sociedade : ensaios sobre as diferentes maneiras de representar o social", 
"Sob o império das leis : Constituição e unidade nacional na formação do Brasil (1822-1834)", 
"Ô da rua! : o transeunte e o advento da modernidade em São Paulo", 
"Grande sertão: veredas", 
"O mal-estar na civilização, novas conferências introdutórias à psicanálise e outros textos : 1", 
"Os cangaceiros : ensaio de interpretação histórica", 
"Essencial Padre Antonio Vieira", 
"Ficções de Guimarães Rosa : perspectivas", 
"A aventura do livro : do leitor ao navegador : conversações com Jean Lebrun", 
"1922 : a semana que não terminou", 
"História e memória", 
"Iniciação à literatura brasileira", 
"Cabeza de Vaca", 
"Economia política da urbanização", 
"Correspondência Mário de Andrade & Henriqueta Lisboa", 
"Graciliano Ramos : a infância pelas mãos do escritor: um ensaio sobre a formação da subjetividad", 
"Antônio Vieira : jesuíta do rei", 
"O cavaleiro da esperança : vida de Luís Carlos Prestes", 
"Macário, ou do drama romântico em Álvares de Azevedo", 
"Garranchos", 
"Amores & arte de amar", 
"Relações exteriores do Brasil, 1939-1950 : mudanças na natureza das relações Brasil-Estados Uni", 
"Correspondência", 
"Melancolias, mercadorias : Dorival Caymmi, Chico Buarque, o pregão de rua e a canção popular-come", 
"Caetés", 
"Cartas a favor da escravidão", 
"Brasil, Argentina e Estados Unidos : conflito e integração na América do Sul : da Tríplice Alian", 
"Um crime adormecido", 
"Invenção de Orfeu", 
"Gregório de Matos", 
"Viver", 
"Arquivos para quê? : textos escolhidos", 
"Ditadura e democracia no Brasil : do golpe de 1964 à constituição de 1988", 
"1964 : história do regime militar brasileiro", 
"As universidades e o regime militar : cultura política brasileira e modernização autoritária", 
"Antologia poética : Murilo Mendes", 
"A cidade no Brasil", 
"Os leitores de Machado de Assis : o romance machadiano e o público de literatura no século 19", 
"O turista aprendiz", 
"Esplendor do barroco luso-brasileiro", 
"No limiar do silêncio e da letra : traços da autoria em Clarice Lispector", 
"Estas estórias", 
"Imprensa feminina e feminista no Brasil : século XIX: dicionário ilustrado", 
"Manual da redação : as normas de escrita e conduta do principal jornal do país", 
"História econômica e social do estado de São Paulo"]

itens2 = ["Dom Casmurro"]
numero = ["001218504"]

for name in itens2:
    #try:
        DRIVER_PATH = 'C:/Users/brubz/Downloads/chromedriver'
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get('http://dedalus.usp.br/F')


        #<input size=40 name="request" value='Gramática de usos do português.'>

        driver.find_elements_by_name('request')[0].send_keys(name)
        driver.find_element_by_xpath("//select[@name='find_code']/option[text()='Título']").click()
        #driver.find_element_by_xpath("//input[@value='Y']").click()
        driver.find_element_by_xpath("//select[@name='local_base']/option[text()='IEB - Inst. Estudos Brasileiros']").click()
        driver.execute_script("arguments[0].click();",driver.find_element_by_xpath('//input[@type="image"][@src="http://dedalus.usp.br/exlibris/aleph/u23_1/alephe/www_f_por/icon/f-go.gif"]'))

        # #Iterar linhas (rows)
        # trs = driver.find_elements(By.TAG_NAME, "tr") 
        # #Iterar células
        # tds = trs[1].find_elements(By.TAG_NAME, "td")
        # #Obter valor das células
        # print(tds[0].text

        #totals_rows = driver.find_elements_by_xpath("html/body/table")
        #totals_rows_8 = driver.find_elements_by_xpath("html/body/table[8]/tbody")
        #for row in table:
        #    count = 1
        #    site =  "html/body/table[8]/tbody/tr["+count+"]/td[2]"
        #    print("site name is :"+ driver.find_element_by_xpath(site).text)
        #    count += 1
        ##print("type total_rows", type(totals_rows))
        ##print("len: ", len(totals_rows))
        #table = totals_rows[8]
        #elements = driver.find_elements(By.TAG_NAME, 'tr')

        #for e in elements:
         #   print(e.text)
        #print(totals_rows[8])
        #print(type(totals_rows[8]))
        #print('object:' )
        #totals_rows2 =chrome.find_elements_by_xpath("html/body/table[8]/tbody/tr")
        #total_rows_length = len(totals_rows)
        # pegar os trs dentro da table
        total_rows = driver.find_elements_by_xpath("html/body/table[8]/tbody//tr")
        #row_5 = driver.find_elements_by_xpath("html/body/table[8]/tbody/tr[5]")
        
        #print('linha 5:::::', len(linha_5))
        #total_tds = row_5.find_elements_by_xpath("//td[@class='td1']")
        row_index = 1
        td_index = 1
        achou = False
        for row in driver.find_elements_by_xpath("html/body/table[8]/tbody//tr"):
            td_index = 1
            for td in row.find_elements_by_xpath(".//td[@class='td1']"): 
                if td_index == 4:
                    button = td.find_element_by_xpath('a')
                    chrome = webdriver.Chrome(executable_path=DRIVER_PATH)
                    chrome.get(button.get_attribute('href'))
                    row_2_index = 1
                    td_2_index = 1
                    
                    for row_2 in chrome.find_elements_by_xpath("html/body/table[7]//tr"):
                        td_2_index = 1
                        #print('row_2: ',row_2.text)
                        for td_2 in row_2.find_elements_by_xpath(".//td[@class='td1']"): 
                            if td_2_index == 2 and row_2_index == 1: 
                                if td_2.text == numero[0]:
                                    print('achou!!!!!!!!!!!!!!!!!!!')
                                    achou = True
                                    break
                                print('Valor Comparado: ', td_2.text)
                            td_2_index += 1
                        if achou == True:
                            break
                        row_2_index += 1
                    #print('len rows: ',len(chrome.find_elements_by_xpath("html/body/table[7]//tr")))
                    #print('len tds: ',len(row_2.find_elements_by_xpath(".//td[@class='td1']")))
                if achou:
                    break
                td_index += 1
            if achou == True:
                break
            row_index += 1    
        #print("##########################")
        #print('total_rows',len(total_tds))
        #####for row in total_rows:
        #####    count = 1
        #####    if count == 1:
        #####        continue
        #####    site =  "html/body/table[8]/tbody/tr["+str(count)+"]/td[1]"
        #####    #print("Site name is :"+ driver.find_element_by_xpath(site).get_attribute('a'))
        #####    print("Site name is :"+driver.find_element_by_xpath(site).text)
        #####    count += 1


        driver.find_element_by_link_text('Salvar / E-mail').click()
        driver.find_element_by_xpath("//select[@name='format']/option[text()='Formato MARC']").click()
        driver.execute_script("arguments[0].click();",driver.find_element_by_xpath('//input[@type="image"][@src="http://dedalus.usp.br/exlibris/aleph/u23_1/alephe/www_f_por/icon/f-go.gif"]'))

        #driver.set_page_load_timeout(20)
        #driver.maximize_window()

        driver.execute_script("arguments[0].click();",driver.find_element_by_xpath('//img[@alt="Salvar"]'))
        #driver.close()
    #except:
        print("An exception occurred")

fim = time.time()
print(fim - inicio) 