from flask import Flask, render_template
import pandas as pd
from io import StringIO
import os
#from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Load environment variables from .env file
#load_dotenv()
#print("🔐 CONNECTION STRING LOADED:", os.getenv("AZURE_STORAGE_CONNECTION_STRING")[:30], "...")


# Get connection string and container name
#AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=retainagentstorage;AccountKey=XH5eHhglYC+pQqvVtujRTIivJRUe97gvjYUWzXVQqH/E4H8sdeQI4e1gjxw9ePGLzlolPw/MS7ch+ASt3czf3Q==;EndpointSuffix=core.windows.net"

CONTAINER_NAME = "raw-csv-data"



# Initialize Blob client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

app = Flask(__name__, static_folder='static', template_folder='templates')

# Mapping of agent names to blob CSV filenames
BLOB_FILENAMES = {
    "stock": "InventoryStatus_1.csv",
    "pricing": "PricingData_1.csv",
    "promotion": "PromotionPlans_1.csv"
}

DESCRIPTIONS = {
    "stock": "Real-time view of inventory status across all stores.",
    "pricing": "Optimized pricing insights based on competitor and catalog data.",
    "promotion": "Plan and evaluate promotional campaigns based on past performance."
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard/<agent>")
def dashboard(agent):
    title_map = {
        "stock": "Stock Monitoring Dashboard",
        "pricing": "Pricing Optimization Dashboard",
        "promotion": "Promotion Planning Dashboard"
    }

    title = title_map.get(agent, "Agent Dashboard")
    blob_name = BLOB_FILENAMES.get(agent)
    data = []

    if blob_name:
        try:
            print(f"Trying to read: {blob_name} from container {CONTAINER_NAME}")
            blob_client = container_client.get_blob_client(blob_name)
            blob_data = blob_client.download_blob().readall().decode("utf-8")
            df = pd.read_csv(StringIO(blob_data))
            print(f"Successfully loaded {len(df)} rows from {blob_name}")
            data = df.fillna("").to_dict(orient="records")
        except Exception as e:
            print(f"❌ Error loading blob '{blob_name}':", e)

    return render_template("dashboard.html", title=title, description=DESCRIPTIONS.get(agent, ""), data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
