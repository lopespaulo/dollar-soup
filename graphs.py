__author__ = 'paulo'
import plotly.plotly as py
from plotly.graph_objs import *
import pymysql as mariadb
from datetime import datetime

try:
    mariadb_connection = mariadb.connect(user='root', password='admin', database='dollardb', host='127.0.0.1')
    cursor = mariadb_connection.cursor()
except mariadb.Error as error:
    print("Error: {}".format(error))

data_inicial = input("Data Inicial: ")
date = datetime.strptime(data_inicial, "%d/%m/%Y")
data_inicial= date.strftime("%Y/%m/%d")

cursor.execute("SELECT * FROM dollar WHERE dollar_dia >= %s", str(data_inicial))
rows = cursor.fetchall()
for row in rows:
    for col in row:
        print(col)

# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api
#
#import plotly.plotly as py
#from plotly.graph_objs import *

#from datetime import datetime
#x = [
#    datetime(year=2013, month=10, day=04),
#    datetime(year=2013, month=11, day=05),
#    datetime(year=2013, month=12, day=06)
#]
#
#data = Data([
#    Scatter(
#        x=x,
#        y=[1, 3, 6]
#    )
#])
#plot_url = py.plot(data, filename='python-datetime')


