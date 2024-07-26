from datadog import initialize, api
import json
import os
 
# Replace with your actual API and APP keys
options = {
    'api_key': os.getenv('DATADOG_API_KEY'),
    'app_key': os.getenv('DATADOG_APP_KEY'),
    'api_host': 'https://api.us5.datadoghq.com'
}
 
initialize(**options)
 
# Load your dashboard JSON
with open('**/dashboard.json', 'r') as file:
    dashboard_data = json.load(file)
 
# Create the dashboard
response = api.Dashboard.create(**dashboard_data)
 
print("Dashboard created:", response)