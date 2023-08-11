from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

#LEYENDO VARIABLES
load_dotenv()
PWD_BD = os.getenv("PWD_BD")
NETWORK = os.getenv("NETWORK")
PORT = int(os.getenv("PORT_EXT"))
USER = os.getenv("USER")


def login():
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    return drive

def lista_archivos(idfolder):
    query = ""

    drive = login()
    file_list = drive.ListFile({'q': f"'{idfolder}' in parents and trashed=false"}).GetList()

    lista_nombres = []
    lista_extension = []
    lista_dueno = []
    lista_ids = []
    lista_permisos = []

    values = []

    df = pd.DataFrame(columns=['id', 'nombre', 'dueno', 'extension', 'visibilidad'])

    for file in file_list:
        lista_ids.append(file["id"])
        lista_nombres.append(file["title"])
        lista_dueno.append(file["owners"][0]["emailAddress"])

        extension = ""

        if "folder" in file["mimeType"]:
            extension = "folder"
            lista_extension.append("folder")
        else:
            extension = file["fileExtension"]
            lista_extension.append(file["fileExtension"])

        metadata = dict(id = file["id"])
        google_file = drive.CreateFile( metadata = metadata )
        permisos = google_file.GetPermissions()
        
        permiso = "privado"
        for perm in permisos:
            if perm["type"] == "anyone":
                permiso = "público"

        lista_permisos.append(permiso)

        values.append((file["id"],file["title"],extension,file["owners"][0]["emailAddress"],0,permiso))
        

    df["id"] = lista_ids
    df["nombre"] = lista_nombres
    df["dueno"] = lista_dueno
    df["extension"] = lista_extension
    df["visibilidad"] = lista_permisos


    query = "INSERT IGNORE INTO `meliarchivos`.`archivos` (idarchivo,nombrearchivo,extension,duenodelarchivo,enviocorreo,visibilidad) VALUES (%s,%s,%s,%s,%s,%s)"

    cnx = mysql.connector.connect(
        host= NETWORK,
        port=PORT,
        user= USER,
        password=PWD_BD)

    cursor = cnx.cursor()
    cursor.executemany(query,values)

    cnx.commit()

    return "Ok- " + str(cursor.rowcount) + " was inserted."