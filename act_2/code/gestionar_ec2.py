import boto3
import sys

# Configuración del cliente
ec2 = boto3.client('ec2', region_name='us-east-1')

def listar_instancias():
    print("--- Listado de Instancias ---")
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(f"ID: {instance['InstanceId']} | Estado: {instance['State']['Name']}")
    print("-----------------------------\n")

def gestionar_instancia(instancia_id, accion):
    try:
        if accion == "iniciar":
            ec2.start_instances(InstanceIds=[instancia_id])
            print(f"Comando enviado: Iniciando {instancia_id}...")
        elif accion == "detener":
            ec2.stop_instances(InstanceIds=[instancia_id])
            print(f"Comando enviado: Deteniendo {instancia_id}...")
        else:
            print("Acción no válida. Usa 'iniciar' o 'detener'.")
    except Exception as e:
        print(f"Error al procesar la instancia: {e}")

if __name__ == "__main__":
    # Si se pasan argumentos: python gestionar_ec2.py <id> <accion>
    if len(sys.argv) > 2:
        id_instancia = sys.argv[1]
        accion_usuario = sys.argv[2].lower()
        gestionar_instancia(id_instancia, accion_usuario)
    else:
        # Si no hay argumentos, solo lista
        listar_instancias()
        print("Uso: python gestionar_ec2.py <ID_INSTANCIA> <iniciar|detener>")
