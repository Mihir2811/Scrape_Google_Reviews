from serpapi import GoogleSearch
from urllib.parse import parse_qsl
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API")  # Your SerpApi API key

def get_place_info(api_key, place_id):
    params = {
        "engine": "google_maps",
        "place_id": place_id,
        "api_key": api_key,
        "hl": "en"
    }
    
    search = GoogleSearch(params)
    result = search.get_dict()
    
    place_info = {}
    if "place_results" in result:
        place_data = result["place_results"]
        place_info = {
            "place_id": place_id,
            "title": place_data.get("title", ""),
            "address": place_data.get("address", ""),
            "rating": place_data.get("rating", ""),
            "reviews_count": place_data.get("reviews", ""),
            "phone": place_data.get("phone", ""),
            "website": place_data.get("website", ""),
            "hours": place_data.get("hours", {}),
            "type": place_data.get("type", "")
        }
    
    return place_info

def fetch_reviews(api_key, place_id):
    params = {
        "engine": "google_maps_reviews",
        "place_id": place_id,
        "api_key": api_key,
        "hl": "en",
        "sort_by": "qualityScore"
    }

    search = GoogleSearch(params)
    reviews = []

    while True:
        result = search.get_dict()
        if "reviews" in result:
            reviews.extend(result["reviews"])
        else:
            break

        serpapi_pagination = result.get("serpapi_pagination", {})
        next_page = serpapi_pagination.get("next")
        next_page_token = serpapi_pagination.get("next_page_token")

        if next_page and next_page_token:
            search.params_dict.update(dict(parse_qsl(next_page.split('?', 1)[1])))
        else:
            break

    return reviews

def main():
    # Load your list of branches from a JSON file or hardcode it here
    # For example, load from a file:
    with open("motilal_oswal_branches_gujarat.json", "r", encoding="utf-8") as f:
        branches = json.load(f)

    print(f"Found {len(branches)} branches. Starting review scraping...\n")

    for branch in branches:
        place_id = branch.get("place_id")
        if not place_id:
            print("Skipping branch with missing place_id")
            continue

        print(f"Fetching data for: {branch.get('title')} ({place_id})")

        # Get place info (optional - you already have some from the list)
        place_info = get_place_info(API_KEY, place_id)

        # Fetch reviews
        reviews = fetch_reviews(API_KEY, place_id)
        print(f" - Fetched {len(reviews)} reviews")

        output_data = {
            "place_info": place_info,
            "reviews": reviews,
            "total_reviews": len(reviews)
        }

        # Create a safe filename using the place title or place_id
        safe_title = place_info.get('title', 'place').replace(' ', '_').replace('/', '_').lower()
        filename = f"{safe_title}_{place_id}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f" - Saved data to {filename}\n")

if __name__ == "__main__":
    main()
