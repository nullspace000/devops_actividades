# Instrucciones

### 1. Configuración del entorno:

a. Inicia sesión en **AWS Learner Lab** y asegúrate de que el entorno está activo.
b. Accede a la consola de AWS y verifica que la región seleccionada es **us-east-1** o **us-west-2**, conforme a las restricciones del laboratorio.
c. Usa **AWS CloudShell** o una instancia de EC2 con acceso SSH para ejecutar los scipts.

### 2. Automatización con Python y Boto3:

a. Instala y configuta **Boto3** en el entrono si no está disponible: 
``` 
pip install boto3
```

b. Configura las credenciales de AWS si es necesario:
```
aws configure
```
**Nota.** En Learner Lab, el perfil **LabRole** ya está disponible, por lo que no se deben crear nuevas claves de acceso.
c. Desarrolla un script en **Python (gestionar_ec2.py)** que realice las siguientes accciones:
* Listar todas las instancias en la región de su estado actual.
* Iniciar una instancia específica si está detendia.
* Detener una instancia especifica si está en ejecución.

Codigo base sugerido en Python:

d. **Automatización con Bash:**
```
import boto3

ec2 = boto3client('ec2',region_name='us-east-1')

def listar_instancias():
  response = ec2.describe_instances()
  for reservation in response['Reservation']:
    for instance in reservation['instances']:
      print
```
### **3.** Crea un script en **Bash (backup_s3.sh)** para generar un **respaldo** de archivos y enviarlo a un **bucket S3** 

a. El script debe:
* COmprimir un derectorio específico.
* Subir el archivo comprimido a un **buckket S3** en la misma región.
* Generar un log con destalles de la operación.

b. Código base sugerido en bach:
```
```
### Ejecución y validación:
a. Ejecuta el script de **Python** y verifica que las instancias se listan y gestionan correctamente.
b. Ejecuta el script de **Bash** y comprueba que el archivo se genera y sube a **S3** exitosamente.
c. Consulta los logs generados para asegurar que no hay errores en la ejecución.

### 5. Optimización y seguridad:

a. Asegura que los scripts no contienen credenciales en texto plano.
b. Implementa manejo de excepciones en **Python** y validaciones en **Bash** para evitar fallos inesperados.

