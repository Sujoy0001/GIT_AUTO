import requests
import xml.etree.ElementTree as ET
import sys

def check_hasp_keys():
    """
    Queries the local Sentinel Admin Control Center to find connected HASP keys.
    """
    
    # The URL for the local Sentinel Admin Control Center (ACC)
    # This XML page lists all visible keys.
    url = "http://localhost:1947/_int_/view.html"
    
    print(f"Attempting to connect to: {url}")

    try:
        # Set a short timeout in case the service isn't running
        response = requests.get(url, timeout=5)
        
        # This will raise an error if the status code is 4xx or 5xx
        response.raise_for_status()

        # The response is XML, so we parse it
        root = ET.fromstring(response.text)
        
        # Find all '<hasp>' tags in the XML tree
        keys_found = root.findall('.//hasp')

        if not keys_found:
            print("\n--- Result ---")
            print("Status: No Sentinel HASP keys were found.")
            print("The service is running, but no keys are plugged in or visible.")
            print("--------------")
        else:
            print(f"\n--- Result ---")
            print(f"Success! Found {len(keys_found)} Sentinel HASP key(s):")
            for i, key in enumerate(keys_found):
                key_id_elem = key.find('id')
                if key_id_elem is not None:
                    print(f"  {i+1}. Key ID: {key_id_elem.text}")
            print("--------------")

    except requests.exceptions.ConnectionError:
        print("\n--- Error ---", file=sys.stderr)
        print("Connection failed. Could not connect to the Sentinel License Manager.", file=sys.stderr)
        print("Please ensure the 'Sentinel LDK License Manager' service is installed and running.", file=sys.stderr)
        print("---------------", file=sys.stderr)
    
    except requests.exceptions.Timeout:
        print("\n--- Error ---", file=sys.stderr)
        print("The request timed out. The license manager service is not responding.", file=sys.stderr)
        print("---------------", file=sys.stderr)

    except Exception as e:
        print(f"\n--- An unexpected error occurred ---", file=sys.stderr)
        print(f"Error details: {e}", file=sys.stderr)
        print("--------------------------------------", file=sys.stderr)

if __name__ == "__main__":
    check_hasp_keys()