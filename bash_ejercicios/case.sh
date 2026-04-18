#!/usr/bin/bash

fruta="manzana"

case $fruta in
	"manzana")
		echo "Es una fruta roja."
		;;
	"platano")
		echo "Es una fruta amarilla."
		;;	
	"naranja")
		echo "Es una fruta naranja."
		;;	
	*)
		echo "No se que fruta sea"
		;;
esac

