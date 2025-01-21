from azure.storage.blob import BlobServiceClient
import requests

# Azure Blob Storage connection
connection_string = "your_connection_string"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "data-ingestion"

# Fetch data from API
url = "https://api.example.com/data"
response = requests.get(url)
data = response.json()

# Save data to Azure Blob Storage
blob_client = blob_service_client.get_blob_client(container=container_name, blob="data.json")
blob_client.upload_blob(str(data), overwrite=True)

print("Data successfully ingested into Azure Data Lake!")
