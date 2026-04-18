#!/usr/bin/bash

echo "Hoy es" `date`

echo -e "\nProporciona un directorio"
read the_path

echo -e "\n El directorio tiene los siguientes archivos: "
ls -r $the_path
