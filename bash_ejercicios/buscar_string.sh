#!/usr/bin/bash

# buscar caracteres dentro de un texto
# argumentos "texto_base""caracter_a_buscar"

texto="$1"
buscar="$2"

	if [[ "$texto" == *"$buscar"* ]]; then
		echo "Encontrado"
	else
		echo "No encontrado"
	fi
