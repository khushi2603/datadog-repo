import os
import json
import glob
import hashlib
from datadog import initialize, api

# Initialize Datadog
options = {
    'api_key': os.getenv('DATADOG_API_KEY'),
    'app_key': os.getenv('DATADOG_APP_KEY'),
    'api_host': 'https://api.us5.datadoghq.com'
}

initialize(**options)

# Function to compute the checksum of a file
def compute_checksum(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

# Function to create dashboard
def create_dashboard(file_path):
    with open(file_path, 'r') as file:
        dashboard_data = json.load(file)
    response = api.Dashboard.create(**dashboard_data)
    print(f"Dashboard created for {file_path}:", response)

# Load previous checksums from file
checksums_file = 'checksums.json'
if os.path.exists(checksums_file):
    with open(checksums_file, 'r') as file:
        previous_checksums = json.load(file)
else:
    previous_checksums = {}

# Find and process all dashboard.json files
dashboard_files = glob.glob('Client*/dashboard.json')
current_checksums = {}

for file_path in dashboard_files:
    checksum = compute_checksum(file_path)
    current_checksums[file_path] = checksum

    if previous_checksums.get(file_path) != checksum:
        print(f'Processing {file_path}')
        create_dashboard(file_path)
    else:
        print(f'Skipping {file_path}, no changes detected')

# Save current checksums to file
with open(checksums_file, 'w') as file:
    json.dump(current_checksums, file)
