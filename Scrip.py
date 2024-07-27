#se importan las librerias a usar

import re
from colorama import Fore
import requests

#se crea la variable que contiene el valor de la URL a usar en el web scripting
website = "https://www.vulnhub.com/"
result = requests.get(website)
content = result.text
#esto visualiza los datos de la peticiòn HTTP
#print(content) 
#obtener el nombre de cada maquina despues del entry, lo busque al inspeccionar la pagina y lo guarda en la variable patron
pattern = r"/entry/[\w-]*" 
#findall solo funciona con str asi que se pasa content a str, lo que esta en patron me lo guarda en content
same_machine = re.findall (pattern, str(content))
#mustra los nombres de las màquinas en la website
#print(same_machine) 
#se crea la variable que ayude a filtrar los nombres
without_sames = list(set(same_machine))
#print(without_sames)
#en esta linea de codigo se quita el entry, solo mostrarà el nombre de las màquinas
final_machines = [] 

for i in without_sames:
    machine_name = i.replace("/entry/", "")
    final_machines.append(machine_name)
    print(machine_name)


######Identificar si hay una nueva màquina######
#tomo el ultimo elemento de la pagina principal
noob_machine = "noob-1"
#si no esta el elemento anterior significa que han agregado uno nuevo y este paso a la sgte pagina
noob_exist = False


for a in final_machines:
    if a == noob_machine:
        noob_exist = True
        break

magenta_color = Fore.LIGHTMAGENTA_EX
green_color= Fore.GREEN


if noob_exist == True:
    print("\n" + magenta_color + "No hay ninguna novedad" + "\n")
else:
    print("\n" + green_color + "¡Hay novedad!" + "\n")
    