
import os
import mysql.connector
import subprocess
from mysql.connector import errorcode

USER='root'
PASS='root'
cnx = mysql.connector.connect (user=USER, password=PASS,
                               host='localhost',buffered=True)
cursor = cnx.cursor()

query = "show databases;"

path="/datadrive/backup/"
cursor.execute(query)
response = cursor.fetchall()

for db in response:
    dir=os.path.join(path, db[0])
    print dir
    if os.path.exists(path + db[0]) == True :
        subprocess.call(['innobackupex', '--user=root','--password=root','--databases="db[0]" ','--no-timestamp' , dir ])
        subprocess.call(['innobackupex','--apply-log','--export', dir ])
    else:
         os.mkdir( path + db[0],0777 )
         subprocess.call(['innobackupex', '--user=root','--password=root','--databases="db[0]" ','--no-timestamp', dir ])
         subprocess.call(['innobackupex','--apply-log','--export', dir ])

    print db[0]


cursor.close()
cnx.close()
