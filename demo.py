# from src.cloud_storage.azure_storage import AzureBlobStorage
# from pathlib import Path
# from src.constants import ROOT_DIR

# azure_storage_client = AzureBlobStorage()

# # print(azure_storage_client.is_file_available(container_name='nermodel', file_path='temp.txt'))

# azure_storage_client.upload_model(file_path=f'{ROOT_DIR}/models/temp2.txt', to_directory='models/temp2.txt', container_name='nermodel')

import os

print(os.path.join('models/first_model/model.pkl'))
print(os.path.dirname('models/first_model/model.pkl'))