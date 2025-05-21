from src.cloud_storage.azure_storage import AzureBlobStorage
# from pathlib import Path
from src.constants import ROOT_DIR

blob_storage_client = AzureBlobStorage()

# print(azure_storage_client.is_file_available(container_name='nermodel', file_path='temp.txt'))

# blob_storage_client.upload_file(file_path=f'{ROOT_DIR}/models/temp2.txt', file_blob_path='models/temp2.txt', container_name='nermodel', remove=False)

# blob_storage_client.get_storage_account_info()
blob_storage_client.create_container('tempcontainer')