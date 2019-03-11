import csv
import urllib.request
from bs4 import BeautifulSoup
#f = open('tspscrape.csv', 'w', newline = '')
#writer = csv.writer(f)
import mysql.connector

mydb = mysql.connector.connect(
	user = "stockanalysis",
	passwd = "password123",
	host = "localhost",
	auth_plugin = "mysql_native_password",
	database = "stockanalysis",
	connection_timeout = 30,
	)    

# Create cursor instance
my_cursor = mydb.cursor()

#CREATE TSP Table
#my_cursor.execute("CREATE TABLE tsprawscrape (Date VARCHAR(50) PRIMARY KEY, L_Income VARCHAR(50), L_2020 VARCHAR(50), L_2030 VARCHAR(50), L_2040 VARCHAR(50), L_2050 VARCHAR(50), G_Fund VARCHAR(50), F_Fund VARCHAR(50), C_Fund VARCHAR(50), S_Fund VARCHAR(50), I_Fund VARCHAR(50))")
#my_cursor.execute("SHOW TABLES")

soup = BeautifulSoup(urllib.request.urlopen("https://www.tsp.gov/InvestmentFunds/FundPerformance/index.html").read(),'lxml')

tbody = soup('table', {"class":"tspStandard"})[0].find_all('tr')
for row in tbody:
    cols = row.findChildren(recursive=False)
    cols = [ele.text.strip() for ele in cols]
    sqlStuff = "INSERT INTO tsprawscrape (Date, L_Income, L_2020, L_2030, L_2040, L_2050, G_Fund, F_Fund, C_Fund, S_Fund, I_Fund) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE L_Income=VALUES (L_Income), L_2020=VALUES (L_2020), L_2030=VALUES (L_2030), L_2040=VALUES (L_2040), L_2050=VALUES (L_2050), G_Fund=VALUES (G_Fund), F_Fund=VALUES (F_Fund), C_Fund=VALUES (C_Fund), S_Fund=VALUES (S_Fund), I_Fund=VALUES (I_Fund)"
    my_cursor.execute(sqlStuff, cols)
    #writer.writerow(cols)
    #print(cols)

mydb.commit()

