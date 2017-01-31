
import os
import mysql.connector
import subprocess
from mysql.connector import errorcode


cnx = mysql.connector.connect (user='root', password='root',
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
        subprocess.call(['innobackupex', '--user=root', '--password=root','--databases="db[0]" ' , dir,'--no-timestamp'])
        subprocess.call(['innobackupex','--apply-log','--export', dir])
    else:
         os.mkdir( path + db[0],0755 )
         subprocess.call(['innobackupex', '--user=root', '--password=root','--databases="db[0]" ', dir,'--no-timestamp'])
         subprocess.call(['innobackupex','--apply-log','--export', dir])

    print db[0]


cursor.close()
cnx.close()
