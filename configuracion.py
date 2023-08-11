import os 
from dotenv import load_dotenv
import mysql.connector
from dotenv import load_dotenv
import time
import os 

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "sql_scripts"
abs_file_path = os.path.join(script_dir, rel_path)

#LEYENDO VARIABLES
load_dotenv()
PWD_BD = os.getenv("PWD_BD")
NETWORK = os.getenv("NETWORK")
PORT = os.getenv("PORT")

#CREANDO CONTENEDOR DE DOCKER CON LA BASE DE DATOS DE MYSQL
os.system(f'docker run --name mysqlmeli -h {NETWORK} -p {PORT} -e MYSQL_ROOT_PASSWORD={PWD_BD} -d mysql:5.7.29')

#LEYENDO VARIABLES
load_dotenv()

PORT = int(os.getenv("PORT_EXT"))
USER = os.getenv("USER")

time.sleep(20)

# CREAR CONEXION A LA BASE DE DATOS
cnx = mysql.connector.connect(
    host= NETWORK,
    port=PORT,
    user= USER,
    password=PWD_BD)

cursor = cnx.cursor()

def ejecutar_script(nombre_archivo):
    fd = open(nombre_archivo, 'r')
    sqlfile = fd.read()
    fd.close()

    cursor.execute(sqlfile)

ejecutar_script(abs_file_path + "/script_db.sql")
ejecutar_script(abs_file_path + "/script_tabla.sql")