import requests
from bs4 import BeautifulSoup
import json
import MySQLdb
import tables

url = "https://fantasy.premierleague.com/drf/bootstrap-static"

html = requests.get(url).text
player_info = json.loads(html)
db = MySQLdb.connect(host="testdb.ckbnf4kfx74t.us-east-1.rds.amazonaws.com",    # your host, usually localhost
                     user="root",         # your username
                     passwd="rootroot",  # your password
                     db="test")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
cur.execute("drop table if exists players")
sql_str = "CREATE TABLE  players (" + tables.table_str + ");"
cur.execute(sql_str)

for idx,player in enumerate(player_info["elements"]):
    args = idx, player['first_name'], player['second_name'], player['goals_scored']
    sql = "INSERT INTO players  VALUES (%s, %s, %s, %s)"

    placeholders = ', '.join(['%s'] * len(player))
    columns = ', '.join(player.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("players", columns, placeholders)
    cur.execute(sql, player.values()) 


cur.execute("SELECT * FROM players WHERE first_name = 'Harry' AND second_name = 'Kane'")

rows = cur.fetchall()
col_names = [i[0] for i in cur.description]
for item in rows:
    for col, val in zip(item,col_names):
        print str(val) + ": " + str(col)
db.close()
