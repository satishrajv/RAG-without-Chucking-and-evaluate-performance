from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
from azure.core.exceptions import ResourceNotFoundError, AzureError

# Load environment variables
load_dotenv()

# Fetch credentials and URL from environment
try:
    client_id = os.environ['AZURE_CLIENT_ID']
    tenant_id = os.environ['AZURE_TENANT_ID']
    client_secret = os.environ['AZURE_CLIENT_SECRET']
    account_url = os.environ['AZURE_STORAGE_URL']
    # Debug: Print the URL to check its value
    print(f"Account URL: '{account_url}'")
    # Clean the URL: remove whitespace and trailing slashes
    account_url = account_url.strip().rstrip('/')
except KeyError as e:
    print(f"Error: Missing environment variable {e}")
    exit(1)

# Create Azure credentials
credentials = ClientSecretCredential(
    client_id=client_id,
    client_secret=client_secret,
    tenant_id=tenant_id
)

def list_all_containers():
    try:
        blob_service_client = BlobServiceClient(account_url=account_url, credential=credentials)
        containers = blob_service_client.list_containers()
        print("\nAvailable containers in your storage account:")
        for container in containers:
            print(f" - {container['name']}")
    except AzureError as e:
        print(f"Error listing containers: {e}")
        return

def download_blobs_to_local(container_name='azureml', download_dir="downloaded"):
    # Ensure local download folder exists
    os.makedirs(download_dir, exist_ok=True)

    # Connect to the container
    try:
        blob_service_client = BlobServiceClient(account_url=account_url, credential=credentials)
        container_client = blob_service_client.get_container_client(container_name)
        container_client.get_container_properties()  # Check if container exists
    except ResourceNotFoundError:
        print(f"\nContainer '{container_name}' not found.")
        list_all_containers()
        return
    except AzureError as e:
        print(f"\nError accessing container '{container_name}': {e}")
        return

    print(f"\nDownloading blobs from container: '{container_name}'")
    blob_list = list(container_client.list_blobs())  # Convert to list to count items
    if not blob_list:
        print(f"No blobs found in container '{container_name}'")
        return

    for blob in blob_list:
        try:
            blob_client = container_client.get_blob_client(blob=blob.name)
            # Create local directory structure if blob name includes folders
            local_path = os.path.join(download_dir, blob.name)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Stream download to handle large files
            with open(local_path, "wb") as file:
                stream = blob_client.download_blob()
                for chunk in stream.chunks():
                    file.write(chunk)
            
            print(f"Success: Downloaded '{blob.name}' to '{local_path}'")
        except Exception as e:
            print(f"Error downloading '{blob.name}': {e}")
            continue

# MAIN
if __name__ == "__main__":
    list_all_containers()  # Optional: lists all containers
    download_blobs_to_local(container_name='azureml', download_dir="downloaded")  # Main function to download blobs