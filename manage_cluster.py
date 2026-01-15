import os
import requests
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIGURATION (from env) ---
# Retrieve Atlas Admin credentials and info from .env
ATLAS_PUBLIC_KEY = os.getenv("ATLAS_PUBLIC_KEY")
ATLAS_PRIVATE_KEY = os.getenv("ATLAS_PRIVATE_KEY")
ATLAS_PROJECT_ID = os.getenv("ATLAS_PROJECT_ID")
ATLAS_CLUSTER_NAME = os.getenv("ATLAS_CLUSTER_NAME")

# --- API ENDPOINT ---
BASE_URL = "https://cloud.mongodb.com/api/atlas/v1.0"
CLUSTER_URL = f"{BASE_URL}/groups/{ATLAS_PROJECT_ID}/clusters/{ATLAS_CLUSTER_NAME}"

# --- HELPER: Auth Header ---
# Requests supports HTTPDigestAuth which is required for Atlas API
from requests.auth import HTTPDigestAuth

def get_auth():
    if not ATLAS_PUBLIC_KEY or not ATLAS_PRIVATE_KEY:
        print("Error: Missing ATLAS_PUBLIC_KEY or ATLAS_PRIVATE_KEY in .env")
        return None
    return HTTPDigestAuth(ATLAS_PUBLIC_KEY, ATLAS_PRIVATE_KEY)

def check_status():
    auth = get_auth()
    if not auth: return

    try:
        response = requests.get(CLUSTER_URL, auth=auth)
        if response.status_code == 200:
            data = response.json()
            state = data.get("stateName")
            paused = data.get("paused")
            print(f"\nCurrent Status: {state} (Paused: {paused})")
            return data
        else:
            print(f"Error checking status: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def pause_cluster():
    auth = get_auth()
    if not auth: return

    print(f"\nAttempting to PAUSE cluster '{ATLAS_CLUSTER_NAME}'...")
    payload = {"paused": True}

    try:
        response = requests.patch(CLUSTER_URL, json=payload, auth=auth, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            print("✓ Pause request sent successfully.")
            print("Cluster state is now changing. This may take a few minutes.")
        else:
            print(f"Failed to pause: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def resume_cluster():
    auth = get_auth()
    if not auth: return

    print(f"\nAttempting to RESUME cluster '{ATLAS_CLUSTER_NAME}'...")
    payload = {"paused": False}

    try:
        response = requests.patch(CLUSTER_URL, json=payload, auth=auth, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            print("✓ Resume request sent successfully.")
            print("Cluster is resuming. This may take a few minutes.")
        else:
            print(f"Failed to resume: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def terminate_cluster():
    auth = get_auth()
    if not auth: return

    print(f"\nWARNING: You are about to TERMINATE (DELETE) cluster '{ATLAS_CLUSTER_NAME}'.")
    print("This action is IRREVERSIBLE. All data will be lost.")
    confirm = input(f"Type '{ATLAS_CLUSTER_NAME}' to confirm termination: ")

    if confirm == ATLAS_CLUSTER_NAME:
        try:
            response = requests.delete(CLUSTER_URL, auth=auth)
            if response.status_code == 202: # 202 Accepted
                print("✓ Termination request accepted.")
                print("Cluster is being deleted.")
            else:
                print(f"Failed to terminate: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Termination cancelled. Name mismatch.")

def main():
    if not all([ATLAS_PROJECT_ID, ATLAS_CLUSTER_NAME]):
        print("Error: Missing ATLAS_PROJECT_ID or ATLAS_CLUSTER_NAME in .env")
        return

    while True:
        print("\n" + "="*50)
        print(f"MongoDB Atlas Cluster Manager: {ATLAS_CLUSTER_NAME}")
        print("="*50)

        # Optional: Auto-check status on loop start
        # check_status() 

        print("1. Check Status")
        print("2. Pause Cluster")
        print("3. Resume Cluster")
        print("4. Terminate Cluster (DELETE)")
        print("5. Exit")

        choice = input("\nEnter choice (1-5): ")

        if choice == '1':
            check_status()
        elif choice == '2':
            pause_cluster()
        elif choice == '3':
            resume_cluster()
        elif choice == '4':
            terminate_cluster()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
