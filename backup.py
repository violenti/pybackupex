
import os
import mysql.connector
from subprocess import call
from mysql.connector import errorcode
from slackclient import SlackClient

USER='root' #name of the user of mysql  with privileges
PASS='root' #password of the user of mysql with privileges
slack_token=""
sc = SlackClient(slack_token)

#path where save your backup
path="/datadrive/backup/"


def get_connection():
    return mysql.connector.connect (user=USER, password=PASS,
                               host='localhost',buffered=True)
conn=get_connection()
cu=conn.cursor()
cu.execute("show databases")

response=cu.fetchall()
conn.close()
#call different databases one for one
# and generate a backup
for db in response:
    destination_dir=os.path.join(path, db[0])
    base=db[0]
    print base

    if not os.path.exists(path + db[0]):
           os.mkdir( path + db[0],0755)
    backup=call(["/usr/bin/innobackupex", "--user=" + USER, "--password=" + PASS, "--databases=" + base,destination_dir,"--no-timestamp"])
    sc.api_call("chat.postMessage",channel="#sensu",text="The Full backup of is correctly  :tada:")
