#!/usr/bin/env python
# coding: utf-8

################################################################################
#
# Nombre del guión         : broker.py
# Descripción              : Módulo con funciones que cargan y descargan 
#                             archivos de MS Azure Storage
# Autor(es)                : Alfredo Espinoza Pelayo
# Correo(s) electrónico(s) : c.aespel@ternium.com.mx
# Última fecha edición     : 26/08/2022
#
################################################################################


# Índice:
## • Importaciones
## • Funciones Auxiliares
###   1. upload_to_blob
###   2. download_from_blob
## • Función de Prueba


################################################################################
# Importaciones ################################################################
################################################################################
# region

## NATIVE
### Módulo que provee facilidades principales para manejar diferentes tipos de E/S
import io

## THIRD PARTY
### Módulo para manejar conexión al almacén remoto de Azure
from azure.storage.blob import BlobServiceClient
### Import module for data manipulation
import pandas as pd

# endregion


################################################################################
# Funciones Auxiliares #########################################################
################################################################################
# region

## Función para cargar archivo al almacén en la nube
def upload_to_blob(
    url: str,
    container: str,
    shared_access_key: str,
    uploading_file_path: str,
    blob_file_name: str,
    overwrite: bool,
) -> \
None:
    """
    Función que transfiere un archivo local a un contenedor de almacenamiento remoto
    """
    
    ### Verificar si el nombre de la ruta al archivo es una cadena de caracteres
    assert type(uploading_file_path) is str, "file_path should be type str"
    
    ### (refactor) suggestion: if not blob_service_client:
    ### Initializes connection as client
    blob_service_client = BlobServiceClient(account_url=url, credential=shared_access_key)
    ### Initializes connection to specific container and blob
    blob_client = blob_service_client.get_blob_client(container=container, blob=blob_file_name)

    ### Upload local file to blob
    with open(uploading_file_path, "rb") as file:
        blob_client.upload_blob(file, overwrite=overwrite)


## Función para descargar archivo del almacén en la nube
def download_from_blob(
    url: str,
    container: str,
    shared_access_key: str,
    blob_file_name: str,
) -> \
pd.DataFrame:
    """
    Función para bajar archivos del blob storage
    """
    buffer = io.BytesIO()
    
    blob_service_client = BlobServiceClient(account_url=url, credential=shared_access_key)
    blob_client = blob_service_client.get_container_client(container=container)
    blob_client.download_blob(blob_file_name).readinto(buffer)
    
    df = pd.read_parquet(buffer, engine='pyarrow')
    return df

# endregion


################################################################################
# Función de Prueba ############################################################
################################################################################
# region

if __name__ == '__main__':
    
    df = pd.DataFrame()
    df.to_parquet('./local_borrar_prueba0.parquet')
    
    upload_to_blob(
        url=url,
        container=container,
        shared_access_key=shared_access_key,
        uploading_file_path='./local_borrar_prueba0.parquet',
        blob_file_name='nube_borrar_prueba0.parquet',
        overwrite=True
    )

# endregion