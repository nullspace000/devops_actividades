import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')

def listar_instancias():
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(f"ID: {instance['InstanceId']}, Estado: {instance['State']['Name']}")

def gestionar_instancia(instancia_id, accion):
    if accion == "iniciar":
        ec2.start_instances(InstanceIds=[instancia_id])
        print(f"Instancia {instancia_id} iniciada.")
    elif accion == "detener":
        ec2.stop_instances(InstanceIds=[instancia_id])
        print(f"Instancia {instancia_id} detenida.")

if __name__ == "__main__":
    listar_instancias()
    gestionar_instancia("ID_INSTANCIA", "iniciar")  # Reemplazar ID_INSTANCIA según corresponda.
