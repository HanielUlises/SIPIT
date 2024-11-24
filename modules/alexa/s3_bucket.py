import boto3 
import json

# Codigo base para que lambda y s3 esten en comunicacion
def subirAS3(nombre_bucket, file_path, llave_archivo):
    s3 = boto3.client('s3')
    try:
        with open(file_path, "rb") as file_data:
            s3.put_object(Bucket=nombre_bucket, Key=llave_archivo, Body=file_path)
            print(f"Archivo subido exitosamente a S3: {llave_archivo}")
            return True
    except Exception as e:
        print(f"Error al subir arhivo a s3: {e}")
        return None
