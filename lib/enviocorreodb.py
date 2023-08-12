import mysql.connector
from dotenv import load_dotenv
from pandas import DataFrame
from lib.enviocorreos import gmail_send_message
import codecs
from oauth2client import client, file, tools
import codecs
import os 

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "parametros"
abs_file_path = os.path.join(script_dir, rel_path)

SCOPES = "https://www.googleapis.com/auth/gmail.send"

#LEYENDO VARIABLES
load_dotenv()
PWD_BD = os.getenv("PWD_BD")
NETWORK = os.getenv("NETWORK")
PORT = int(os.getenv("PORT_EXT"))
USER = os.getenv("USER")

def enviar_correos():
    cnx = mysql.connector.connect(
            host= NETWORK,
            port=PORT,
            user= USER,
            password=PWD_BD)

    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM meliarchivos.archivos WHERE enviocorreo = 0")
    
    df = DataFrame(cursor.fetchall())

    if df.shape[0]:
        field_names = [i[0] for i in cursor.description]
        df.columns = field_names

    store = file.Storage('token.json')
    creds = None

  
    
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
        creds = tools.run_flow(flow, store)

    if df.shape[0]:
        for us in df["duenodelarchivo"].unique().tolist():
            df_filter = df[df["duenodelarchivo"] == us]
            table = ""
            for i, reg in df_filter.iterrows():
                row = f'''
                <tr>
                <td>{reg["idarchivo"]}</td>
                <td>{reg["nombrearchivo"]}</td>
                </tr>
                '''

                table = table + row

            f = codecs.open(abs_file_path + "/correo.html", 'r')    
            body = f.read()
            body = body.format(**{"tabla": table})

            gmail_send_message(body, us, creds)

    cursor.execute("UPDATE meliarchivos.archivos SET enviocorreo = 1 WHERE enviocorreo = 0")
    cnx.commit()