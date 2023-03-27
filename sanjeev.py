from fastapi import FastAPI, File, UploadFile
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import uuid

app = FastAPI()

# Connect to your Azure Blob Storage account
connection_string = "DefaultEndpointsProtocol=https;AccountName=smarthire;AccountKey=bTXkG+GVRksTXcFqKG6VLJ993OlnRPz3RvdNvWJRPdt+DoTcIzaAVIvZeICOOPIeoGN6+Us/CgX6+AStzCLnRQ==;EndpointSuffix=core.windows.net "
container_name = "resume"
blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_string)
container_client = blob_service_client.get_container_client(container_name)

# Define an endpoint to handle file uploads
@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    # Generate a unique filename to avoid conflicts
    file_name = str(uuid.uuid4())

    # Upload the file to your Azure Blob Storage container
    blob_client = container_client.get_blob_client(file_name)
    data = await file.read()
    blob_client.upload_blob(data)

    # Return the URL to the uploaded file
    return {"file_url": blob_client.url}
