import pymarc
import time
from pymarc import parse_xml_to_array
from pymarc import MARCReader 
import os
 
#pymarc.marcxml.record_to_xml("teste.mrk", quiet=False, namespace=False)

inicio = time.time()

import os
directory = 'C:\\Users\\brubz\\Downloads\\Teste'

f = open('item_exemplo.xml', 'w', encoding = 'utf-8') #utf8
f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?><marc:collection xmlns:marc=\"http://www.loc.gov/MARC21/slim\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.loc.gov/MARC21/slim http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd\">")

i = 0
for item in os.listdir(directory):
    item = directory+"\\"+item
    with open(item, 'rb') as fh:
        reader = MARCReader(fh, force_utf8=True)
        for record in reader:
            xml = pymarc.marcxml.record_to_xml(record)
            xml = str(xml)[2:-1].replace("<", "<marc:").replace("<marc:/", "</marc:")
            f.write(str(xml))
f.write("</marc:collection>")

f.close()

fim = time.time()
print(fim - inicio) 