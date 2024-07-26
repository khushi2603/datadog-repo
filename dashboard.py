import os
import json
import glob
from datadog import initialize, api

# Initialize Datadog
options = {
    'api_key': os.getenv('DATADOG_API_KEY'),
    'app_key': os.getenv('DATADOG_APP_KEY'),
    'api_host': 'https://api.us5.datadoghq.com'
}

initialize(**options)

# Function to create dashboard
def create_dashboard(file_path):
    with open(file_path, 'r') as file:
        dashboard_data = json.load(file)
    response = api.Dashboard.create(**dashboard_data)
    print(f"Dashboard created for {file_path}:", response)

# Find and process all dashboard.json files
dashboard_files = glob.glob('client*/dashboard.json')
for file_path in dashboard_files:
    print(f'Processing {file_path}')
    create_dashboard(file_path)
