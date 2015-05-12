__author__ = 'phlopes'
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup, SoupStrainer
import pymysql as mariadb

try:
    mariadb_connection = mariadb.connect(user='root', password='admin', database='dollardb', host='127.0.0.1')
    cursor = mariadb_connection.cursor()
except mariadb.Error as error:
    print("Error: {}".format(error))

#minerador
def get_html(url):
    dados = urllib.request.urlopen(url)
    return dados

#escovando dados
def clean_data(dados):
    only_table_tags = SoupStrainer("td") #Define a Tag parseada
    soup = BeautifulSoup(dados, 'html.parser', parse_only=only_table_tags)
    soup = soup.get_text('|', strip=True)
    valor = [valor.replace(",", ".") for valor in soup.split('|')]
    date = datetime.strptime(valor[0], "%d/%m/%Y")
    valor[0] = date.strftime("%Y/%m/%d")

    #A trabalhar ######
    # try:
    #     cursor.execute("""
    #         INSERT INTO dollar (dollar_dia, dollar_compra, dollar_venda)
    #         VALUES (%s, %s, %s)
    #         ON DUPLICATE KEY UPDATE dollar_dia=%s",(str(valor[0]), str(valor[1]), str(valor[2]), str(valor[0]))""")
    # except mariadb.Error as error:
    #     print("Error: {}".format(error))
    # mariadb_connection.commit()

#Otimizar as consultas!
    if cursor.execute("SELECT * FROM dollar WHERE dollar_dia = %s", (valor[0])) < 1:
        try:
            cursor.execute("INSERT INTO dollar (dollar_dia, dollar_compra, dollar_venda) VALUES (%s, %s, %s)",(str(valor[0]), str(valor[1]), str(valor[2])))
        except mariadb.Error as error:
            print("Error: {}".format(error))
    else:
        try:
            cursor.execute("UPDATE dollar SET dollar_compra = %s, dollar_venda=%s WHERE dollar_dia = %s",(str(valor[1]), str(valor[2]), str(valor[0])))
        except mariadb.Error as error:
            print("Error: {}".format(error))
    mariadb_connection.commit()

url = 'https://www3.bcb.gov.br/ptax_internet/consultarUltimaCotacaoDolar.do'
clean_data(get_html(url))