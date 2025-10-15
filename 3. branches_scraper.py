"""
This script uses SerpApi to search Google Maps for all "Honest" restaurant branches located in Gujarat, India. 
It automates the process of finding and storing place details (such as name, address, rating, and review count) 
for each branch returned by the search query.

Main features:
1. Loads the SerpApi API key securely from a .env file.
2. Queries Google Maps for "Honest restaurant Gujarat" using SerpApi.
3. Filters results to include only locations that mention both "Honest" and "Gujarat".
4. Extracts relevant information — place ID, title, address, rating, and review count.
5. Saves the collected data into both JSON and CSV formats for further use or analysis.
6. Displays a formatted list of all found branches in the console.

This script is useful for building datasets of business branches or for automating 
local business information gathering through Google Maps search results.
"""


import os
import json
import pandas as pd
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API")

def get_all_place_ids(api_key, query, location_ll=None):
    params = {
        "engine": "google_maps",
        "q": query,
        "api_key": api_key,
        "type": "search",
        "hl": "en"
    }

    if location_ll:
        params["ll"] = location_ll  # Optional: pass lat,long if needed

    search = GoogleSearch(params)
    results = search.get_dict()

    print(json.dumps(results, indent=2))  # Debug print

    branches = []

    if "local_results" in results:
        for place in results["local_results"]:
            address = place.get("address", "")
            title = place.get("title", "")
            if "Gujarat" in address and "Honest" in title:
                branches.append({
                    "place_id": place.get("place_id"),
                    "title": title,
                    "address": address,
                    "rating": place.get("rating"),
                    "reviews": place.get("reviews")
                })

    return branches

def save_to_json(data, filename="honest_branches_gujarat.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON to {filename}")

def save_to_csv(data, filename="honest_branches_gujarat.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Saved CSV to {filename}")

def main():
    query = "Honest restaurant Gujarat"
    location_ll = None  # Optional: specify lat,long if needed

    print("Searching for Honest branches in Gujarat...")
    branches = get_all_place_ids(API_KEY, query, location_ll)

    if not branches:
        print("No Honest branches found in Gujarat.")
        return

    print(f"Found {len(branches)} Honest branches in Gujarat.\n")

    for i, branch in enumerate(branches):
        print(f"{i+1}. {branch['title']} - {branch['address']} (Place ID: {branch['place_id']})")

    save_to_json(branches)
    save_to_csv(branches)

if __name__ == "__main__":
    main()
