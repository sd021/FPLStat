import requests
from bs4 import BeautifulSoup
import json
import MySQLdb
import tables
import yaml


with open("secret_config.yaml", 'r') as stream:
    try:
        config = (yaml.load(stream))
    except yaml.YAMLError as exc:
        print(exc)
class SQL:
    def SQL_Connect(self):
    
        self.db = MySQLdb.connect(host="testdb.ckbnf4kfx74t.us-east-1.rds.amazonaws.com",    
                     user=config["SQL_User"],    
                     passwd=config["SQL_Pass"],  
                     db="test")        

        cur = self.db.cursor()
        return cur

    def SQL_Close(self):
        self.db.close()
    
def main():
    sql = SQL()
    cur = sql.SQL_Connect()
    url = "https://fantasy.premierleague.com/drf/bootstrap-static"
    cur.execute("DROP TABLE IF EXISTS players")
 
    html = requests.get(url).text
    player_info = json.loads(html)

    sql_str = "CREATE TABLE  players (" + tables.table_str + ");"
    cur.execute(sql_str)

    for idx,player in enumerate(player_info["elements"]):
        args = idx, player['first_name'], player['second_name'], player['goals_scored']
        sql_str = "INSERT INTO players  VALUES (%s, %s, %s, %s)"

        placeholders = ', '.join(['%s'] * len(player))
        columns = ', '.join(player.keys())
        sql_str = "INSERT INTO {} ( {} ) VALUES ( {} )".format("players", columns, placeholders)
        cur.execute(sql_str, player.values()) 

    sql.SQL_Close()


if __name__ == '__main__':
    main()
