# restaurant_scraper

Scrapes restaurant data in Greater Adelaide by suburb and cuisine using Google Maps Text Search API.

## Features
- Covers 60+ suburbs grouped by regions
- Searches 13 cuisine types (e.g., Vietnamese, Italian, Japanese)
- Exports results into a structured CSV

## Requirements
- Python 3
- `requests`, `pandas`
- Google Maps API Key

## How to Use
1. Replace `API_KEY` in the script with your own key or prepare a `.env` file with your API key.
2. Run:
   ```bash
   python restaurant_scraper.py