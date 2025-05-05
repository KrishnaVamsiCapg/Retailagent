from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

BLOB_MOUNT_PATH = "C:\\Users\\regkrish\\retain-agent\\data"


DATA_PATHS = {
    "stock": f"{BLOB_MOUNT_PATH}/InventoryStatus_1.csv",
    "pricing": f"{BLOB_MOUNT_PATH}/PricingData_1.csv",
    "promotion": f"{BLOB_MOUNT_PATH}/PromotionPlans_1.csv"
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
    path = DATA_PATHS.get(agent)
    data = []
    if path and os.path.exists(path):
        df = pd.read_csv(path)
        data = df.fillna("").to_dict(orient="records")

    return render_template("dashboard.html", title=title, description=DESCRIPTIONS.get(agent, ""), data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
