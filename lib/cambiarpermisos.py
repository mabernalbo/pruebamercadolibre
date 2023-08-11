from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from dotenv import load_dotenv
import os
import mysql.connector
import pandas as pd

def cambiarpermisos():
    def login():
        gauth = GoogleAuth()
        drive = GoogleDrive(gauth)
        return drive

    #LEYENDO VARIABLES
    load_dotenv()
    PWD_BD = os.getenv("PWD_BD")
    NETWORK = os.getenv("NETWORK")
    PORT = int(os.getenv("PORT_EXT"))
    USER = os.getenv("USER")

    cnx = mysql.connector.connect(
        host= NETWORK,
        port=PORT,
        user= USER,
        password=PWD_BD)

    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM meliarchivos.archivos WHERE  criticidad = 'crítico' and visibilidad = 'público'")


    df = pd.DataFrame(cursor.fetchall())

    print(df)

    drive = login()

    if df.shape[0]:
        field_names = [i[0] for i in cursor.description]
        df.columns = field_names
        
        for i, reg in df.iterrows():
            metadata = dict(id = reg["idarchivo"])
            google_file = drive.CreateFile( metadata = metadata )
            permisos = google_file.GetPermissions()

            for perm in permisos:
                if perm["type"] == "anyone":
                    google_file.DeletePermission(perm["id"])
    
    cursor.execute("UPDATE meliarchivos.archivos SET visibilidad = 'privado' WHERE criticidad = 'crítico' and visibilidad = 'público'")
    cnx.commit()
