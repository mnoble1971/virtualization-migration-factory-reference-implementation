import yaml
import sys
import os
import requests
from requests.auth import HTTPBasicAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Ensure correct usage
if len(sys.argv) != 2:
    print("Usage: python script.py <input_file.yaml>")
    sys.exit(1)

# Load username and password from environment variables
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Ensure username and password are set before proceeding
if not username or not password:
    print("Error: USERNAME and PASSWORD environment variables must be set before running this script.")
    sys.exit(1)

# Load YAML file
input_file = sys.argv[1]

def extract_baremetalhosts(file_path):
    """Extract only the list under 'baremetalhosts'."""
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    # Extract only the baremetalhosts section
    if isinstance(data, dict) and 'baremetalhosts' in data:
        hosts = data['baremetalhosts']
        if isinstance(hosts, list):
            return hosts
    return None  # Return None if format is incorrect

def print_extracted_hosts(hosts):
    """Print the list of extracted hosts before connecting."""
    print("\nExtracted Entries from YAML File:")
    print("-" * 50)
    for index, host in enumerate(hosts, start=1):
        print(f"Host {index}:")
        for key, value in host.items():
            print(f"  {key}: {value}")
        print("-" * 50)

def query_redfish(management_ip, serial):
    """Query the Redfish API for hardware details."""
    endpoint = f"redfish/v1/Systems/{serial}"
    url = f"https://{management_ip}/{endpoint}"

    # Send the request (disabling SSL verification)
    response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)

    # Check if request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract details
        memory_gib = data.get("MemorySummary", {}).get("TotalSystemMemoryGiB", "Not found")
        blade_model = data.get("Model", "Not found")
        powerstate = data.get("PowerState", "Not found")
        cpu_model = data.get("ProcessorSummary", {}).get("Model", "Not found")
        cpu_count = data.get("ProcessorSummary", {}).get("Count", "Not found")
        cpu_core_count = data.get("ProcessorSummary", {}).get("CoreCount", "Not found")
        health = data.get("Status", {}).get("Health", "Not found")
        id = data.get("Id", "Not found")

        # Print details
        print(f"\nProcessing host: {management_ip} (Serial: {serial})")
        print(f"Id: {id}")
        print(f"Model: {blade_model}")
        print(f"CPU Model: {cpu_model}")
        print(f"CPU Count: {cpu_count}")
        print(f"CPU Cores: {cpu_core_count}")
        print(f"Total System Memory (GiB): {memory_gib}")
        print(f"Health: {health}")
        print(f"Powerstate: {powerstate}")
        print("-" * 50)

    else:
        print(f"Error {response.status_code} for {management_ip}: {response.text}")

# Process each host in the YAML file
hosts = extract_baremetalhosts(input_file)

if hosts:
    # Print extracted host details before connecting
    print_extracted_hosts(hosts)

    # Proceed with connections
    for host in hosts:
        management_ip = host.get('management_ip')
        serial = host.get('serial')

        if management_ip and serial:
            query_redfish(management_ip, serial)
        else:
            print(f"Skipping host entry due to missing management_ip or serial: {host}")

else:
    print("Invalid YAML format. Expected a 'baremetalhosts' key with a list of dictionaries.")

