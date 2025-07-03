# collect_info

Python script to collect operational nearby businesses and their contact info (email/website) based on Google Maps APIs.

## Features
- Geocode a given address
- Search nearby places of selected types (e.g., schools, warehouses)
- Get detailed info including website and email (if available)
- Export data to CSV

## Requirements
- Python 3
- `requests`
- A valid **Google Maps API Key**

## How to Use
1. Replace `API_KEY` in the script with your own key or prepare a `.env` file with your API key.
2. Run the script:
   ```bash
   python collect_info.py
