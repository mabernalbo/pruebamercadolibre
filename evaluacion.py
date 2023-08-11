from lib.listar_archivos import lista_archivos
from lib.enviocorreodb import enviar_correos
import time 

#id del la carpeta de la que se quiere extraer todos los archivos
id = '1tcTX9O5DeK0YTdCqR_GWRPsDto06-QsU'

#Listar archivos de una carpeta en concreto dentro del drive
lista_archivos(id)

time.sleep(2)

#Enviar correos para los dueños de los archivos con el formulario
enviar_correos()