from lib.listar_archivos import lista_archivos
from lib.enviocorreodb import enviar_correos
import time 
from dotenv import load_dotenv
import os 

#LEYENDO VARIABLES
load_dotenv()
id = os.getenv("CARPETA")

#Listar archivos de una carpeta en concreto dentro del drive
lista_archivos(id)

time.sleep(2)

#Enviar correos para los dueños de los archivos con el formulario
enviar_correos()