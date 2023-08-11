from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import pandas as pd
import json
import numpy as np
import mysql.connector
from dotenv import load_dotenv
import os 

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "parametros"
abs_file_path = os.path.join(script_dir, rel_path)

#LEYENDO VARIABLES
load_dotenv()
PWD_BD = os.getenv("PWD_BD")
NETWORK = os.getenv("NETWORK")
PORT = int(os.getenv("PORT_EXT"))
USER = os.getenv("USER")

 
SCOPES = "https://www.googleapis.com/auth/forms.responses.readonly"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

def get_preguntas():
    store = file.Storage('token.json')
    creds = None

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = discovery.build('forms', 'v1', http=creds.authorize(
        Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

    form_id = '1GgjLTTmfbBEebvmO-HQu3iUWrN8txziPZCrmep0Tthg'
    result = service.forms().responses().list(formId=form_id).execute()

 
    dfpreguntas = pd.read_json(abs_file_path + "/estructuraforms.json", orient="records")

    lista = dfpreguntas["variable"].tolist()
    lista.append("criticidad")

    df = pd.DataFrame(columns = lista)

    for resp in  result["responses"]:
        dict = {}
        for i , preg in dfpreguntas.iterrows():
            dict[preg["variable"]] = resp["answers"][preg["id"]]["textAnswers"]["answers"][0]["value"]

        new_row = pd.DataFrame(dict, index=[0])
        df = pd.concat([new_row,df.loc[:]]).reset_index(drop=True)
        
    with open(abs_file_path + '/pardeeval.json', encoding='utf-8') as json_file:
        par = json.load(json_file)

    for i in  lista:
        try:
            df = df.replace({i : par[i]}) 
        except:
            pass
    
    #metodo sacado del cve
    df["isc"] = 1 - ((- df["confidencialidad"] + 1) * (- df["integridad"] + 1) * (- df["disponibilidad"] + 1))      
    df["criticidad"] = np.where(df["isc"] < 0.36, "Tolerable", df["criticidad"])     
    df["criticidad"] = np.where(((df["isc"] >= 0.36) & (df["isc"] < 0.63)) , "Moderado", df["criticidad"])     
    df["criticidad"] = np.where(((df["isc"] >= 0.63) & (df["isc"] < 0.82)) , "Alto", df["criticidad"])       
    df["criticidad"] = np.where(df["isc"] >= 0.82 , "Crítico", df["criticidad"])       

    query = "UPDATE `meliarchivos`.`archivos` SET criticidad = %s  WHERE idarchivo = %s"
    values = []

    for i, reg in df.iterrows():
        values.append((reg["criticidad"],reg["idfile"]))

    cnx = mysql.connector.connect(
        host= NETWORK,
        port=PORT,
        user= USER,
        password=PWD_BD)

    cursor = cnx.cursor()
    cursor.executemany(query,values)
    
    cnx.commit()

    return df


#print(get_preguntas())
#get_preguntas()
#

