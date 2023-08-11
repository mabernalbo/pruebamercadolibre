from lib.forms import  get_preguntas
from lib.cambiarpermisos import cambiarpermisos
import time 
#recolectar preguntas del formulario y cambiar la criticidad en la base de datos
get_preguntas()

time.sleep(2)

#Eliminar los permisos "públicos" para los archivos criticos.
cambiarpermisos()