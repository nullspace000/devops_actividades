# Escribe un Bash script que encuentre una palabra dentro de un archivo e indique si se enconró o no
# Tanto el nombre del archivo como el del texto a buscar set tienen que pasar como arumentos al script, 
# si no se pasan los dos valores de los argumentos se tiene que terminar el programa.

#!/usr/bin/bash
# Verificación de los argumentos del script
if [ "$#" -ne 2 ]; then
	echo "Uso: $0 <archivo_de_log> <termino_de_busqueda>"
	exit
fi

# Declaro variales con argumentos de entrada
archivo_log=$1
termino_busqueda=$2
echo "Buscando el término $termino_busqueda en $archivo_log"
grep -i "$termino_busqueda" "$archivo_log"

# Verificamos si hubo coincidencias
if [ $? -eq 0 ]; ten
	echo "Se encontraron coincidencias."
else
	echo "No se encontraron coincidencias."
