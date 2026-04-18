#!/usr/bin/bash
x=$1
y=$2
# Asignación de variables
echo "x = $x"
echo "y = $y"

# Operadores aritméticos
echo ""
echo "Operadores ariteméticos"
echo "x + y = $((x + y))"
echo "x - y = $((x - y))"
echo "x / y = $((x / y))"
echo "x % y = $((x % y))"

# Operadores de comparación
echo ""
echo "Operadores de comparación"
if [ "$x" -eq "$y" ]; then
echo "x es igual a y"
else
echo "x no es igual a y"
fi

if [ "$x" -ne "$y" ]; then
echo "x no es igual a y"
else
echo "x es igual a y"
fi

if [ "$x" -lt "$y" ]; then
echo "x es menor que y"
else
echo "x no es menor que y"
fi

if [ "$x" -gt "$y" ]; then
echo "x es mayor que y"
else
echo "x no es mayor que y"
fi
