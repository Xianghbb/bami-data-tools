suburb_groups={
    'North': ['Prospect','Brompton','Kilburn','Blair Athol','Enfield','Mawson Lakes','Pooraka','Green Fields','Salisbury South'],
    'NorthEast':['Klemzig','Paradise','Rostrevor','Modbury','Highbury','Athelstone',"Tea Tree Gully", "Holden Hill"],
    'East':["Norwood", "Magill", "Kensington",'Marble Hill'],
    'South':["Parkside",'Unley',"Fullarton", "Malvern"],
    'SouthEast':['Glenside','Burnside','Summertown','Crafers','Piccadilly','Mylor','Aldgate'],
    "Hills": ["Belair", "Stirling", "Blackwood"]
}
import requests
import time
import pandas as pd

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY") 

cuisine_list=[
    "Chinese", "Japanese", "Thai", "Indian", "Vietnamese", "Lebanese", "Asian",
    "Korean", "Italian", "French", "Greek", "Turkish", "Mexican"
]

def get_restaurants_by_keyword(suburb, cuisine):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    all_results = []
    next_page_token = None

    while True:
        params = {
            "query": f"{cuisine} restaurants in {suburb} SA",
            "key": API_KEY
        }
        if next_page_token:
            params["pagetoken"] = next_page_token
            time.sleep(2)

        response = requests.get(url, params=params)
        data = response.json()
        results = data.get("results", [])

        for place in results:
            name = place.get("name")
            address = place.get("formatted_address", "")
            types = place.get("types", [])
            all_results.append({
                "Suburb": suburb,
                "Cuisine": cuisine,
                "Name": name,
                "Address": address,
                "Types": types
            })

        next_page_token = data.get("next_page_token")
        if not next_page_token:
            break

    return all_results


# main flow
all_data = []

for region, suburbs in suburb_groups.items():
    for suburb in suburbs:
        for cuisine in cuisine_list:
            print(f"Collecting {cuisine} restaurants in {suburb}...")
            results = get_restaurants_by_keyword(suburb, cuisine)
            for r in results:
                r["Region"] = region
                all_data.append(r)
            time.sleep(2)

# save as CSV
df = pd.DataFrame(all_data)
df.to_csv("adelaide_restaurants_by_keyword.csv", index=False)
print("data is save as adelaide_restaurants_by_keyword1.csv")