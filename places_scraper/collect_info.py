import requests
import csv
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY") 

# 1. Geocoding with error handling
def geocode_address(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        # Check if we got results
        if not data.get('results'):
            print(f"No geocoding results found for address: {address}")
            return None, None
            
        # Check API status
        if data.get('status') != 'OK':
            print(f"Geocoding API error: {data.get('status')} - {data.get('error_message', 'Unknown error')}")
            return None, None
            
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
        
    except requests.exceptions.RequestException as e:
        print(f"Request error during geocoding: {e}")
        return None, None
    except KeyError as e:
        print(f"Unexpected response format from geocoding API: {e}")
        return None, None

# 2. Search nearby locations with error handling
def search_places(lat, lng, place_type, keyword=None, radius=5000):
    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={lat},{lng}&radius={radius}&type={place_type}&key={API_KEY}"
    )
    if keyword:
        url += f"&keyword={keyword}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') not in ['OK', 'ZERO_RESULTS']:
            print(f"Places API error: {data.get('status')} - {data.get('error_message', 'Unknown error')}")
            return []
            
        return data.get('results', [])
        
    except requests.exceptions.RequestException as e:
        print(f"Request error during place search: {e}")
        return []
    
# get emails 
import requests
import re

def extract_email_from_website(url):
    try:
        resp = requests.get(url, timeout=10)
        raw_emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", resp.text)
        emails=[]

        for email in raw_emails:
            if not any(email.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']):
                emails.append(email)
        return list(set(emails))
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return []
    
# 3. Get merchant details with error handling
def get_place_details(place_id):
    fields = "name,formatted_address,formatted_phone_number,website,business_status"
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') != 'OK':
            print(f"Place details API error: {data.get('status')} - {data.get('error_message', 'Unknown error')}")
            return None
            
        result = data.get('result', {})
        if result.get('business_status') == 'OPERATIONAL':
            website = result.get("website", "")
            email = ""
            if website:
                emails = extract_email_from_website(website)
                if emails:
                    email = emails[0]  # get the first one

            return {
                "name": result.get("name", ""),
                "address": result.get("formatted_address", ""),
                "phone": result.get("formatted_phone_number", ""),
                "website": website,
                "email": email,
            }
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Request error during place details: {e}")
        return None

# 4. Collect data on all target types
def collect_nearby_businesses(center_address):
    lat, lng = geocode_address(center_address)
    
    # Check if geocoding was successful
    if lat is None or lng is None:
        print("Failed to geocode the center address. Exiting.")
        return []
    
    print(f"Successfully geocoded address to: {lat}, {lng}")
    
    types_keywords = [
        ("school", None),
        ("community_center", None),
        ("establishment", "business park"),
        ("establishment", "warehouse"),
    ]
    collected_data = []

    for place_type, keyword in types_keywords:
        print(f"Searching for {place_type} with keyword: {keyword}")
        places = search_places(lat, lng, place_type, keyword)
        print(f"Found {len(places)} places for {place_type}")
        
        for place in places:
            place_id = place.get("place_id")
            if place_id:
                details = get_place_details(place_id)
                if details:
                    details["type"] = keyword if keyword else place_type
                    collected_data.append(details)
                    
    return collected_data

# 5. Export to CSV
def save_to_csv(data, filename="brighton_nearby_operational_places.csv"):
    if not data:
        print("No data found to save.")
        return
        
    try:
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "address", "phone", "website", "email", "type"])
            writer.writeheader()
            writer.writerows(data)
        print(f"✅ Data saved to '{filename}' with {len(data)} records.")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# Execute the main program
if __name__ == "__main__":
    address = "525 Brighton Rd, Brighton SA 5048, Australia"
    print(f"Starting data collection for: {address}")
    
    data = collect_nearby_businesses(address)
    save_to_csv(data)
    
    if data:
        print("✅ Done. Data collection completed successfully!")
    else:
        print("❌ No data was collected. Please check your API key and address.")