"""
This script retrieves detailed information and user reviews for a specific Google Maps location 
using the SerpApi service. It performs the following tasks:
1. Loads the SerpApi API key securely from a .env file.
2. Validates the API key with a test request to ensure connectivity.
3. Fetches place details (name, address, rating, phone, website, etc.) using a Google Maps Place ID.
4. Iteratively retrieves all available reviews for the given place, handling pagination automatically.
5. Saves the place information and reviews into a structured JSON file for offline use or analysis.
6. Displays a few sample reviews in the console for quick reference.
The script is modular, with separate functions for validation, fetching data, saving files, 
and displaying results, making it easy to adapt or extend for different places or use cases.
"""

from serpapi import GoogleSearch
from urllib.parse import parse_qsl
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("API")  # Your SerpApi API key

def validate_api_key(api_key):
    """
    Validate the SerpApi key by making a simple test request.
    """
    test_params = {
        "engine": "google_maps",
        "q": "Test",
        "api_key": api_key
    }
    response = GoogleSearch(test_params).get_dict()

    if "error" in response:
        raise Exception(f"SerpApi Error: {response['error']}")


def get_place_info(api_key, place_id):
    """
    Retrieve basic place information using a Google Maps Place ID.
    """
    params = {
        "engine": "google_maps",
        "place_id": place_id,
        "api_key": api_key,
        "hl": "en"
    }

    result = GoogleSearch(params).get_dict()

    if "error" in result:
        raise Exception(f"SerpApi Error: {result['error']}")

    place_data = result.get("place_results", {})
    return {
        "place_id": place_id,
        "title": place_data.get("title", ""),
        "address": place_data.get("address", ""),
        "rating": place_data.get("rating", ""),
        "reviews_count": place_data.get("reviews", ""),
        "phone": place_data.get("phone", ""),
        "website": place_data.get("website", ""),
        "hours": place_data.get("hours", {}),
        "type": place_data.get("type", "")
    } if place_data else {}


def fetch_reviews(api_key, place_id):
    """
    Fetch all available reviews for a given Place ID.
    """
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

        if "error" in result:
            raise Exception(f"SerpApi Error: {result['error']}")

        reviews.extend(result.get("reviews", []))

        pagination = result.get("serpapi_pagination", {})
        next_page = pagination.get("next")
        next_page_token = pagination.get("next_page_token")

        if next_page and next_page_token:
            search.params_dict.update(dict(parse_qsl(next_page.split('?', 1)[1])))
        else:
            break

    return reviews


def save_to_file(place_info, reviews):
    """
    Save place info and reviews to a JSON file.
    """
    filename = f"{place_info['title'].replace(' ', '_').replace('/', '_').lower()}_reviews.json"
    data = {
        "place_info": place_info,
        "reviews": reviews,
        "total_reviews": len(reviews)
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Place info and reviews saved to: {filename}")


def display_sample_reviews(reviews, count=3):
    """
    Display a few sample reviews.
    """
    print("\n📌 Sample reviews:")
    for i, review in enumerate(reviews[:count]):
        print(f"\nReview {i + 1}:")
        print(f"Rating: {review.get('rating', 'N/A')} stars")
        print(f"Date: {review.get('date', 'N/A')}")
        print(f"Text: {review.get('snippet', 'N/A')[:200]}...")


def main():
    try:
        # Validate API key
        validate_api_key(API_KEY)

        # Replace this with your desired place ID
        place_id = "ChIJDT4-m02FXjkRL0OGzSj-W18"
        print(f"🔍 Using Place ID: {place_id}")

        # Get place information
        place_info = get_place_info(API_KEY, place_id)

        if not place_info or not place_info.get("title"):
            print("⚠️ Failed to retrieve place information. Please check the Place ID.")
            return

        # Print place info
        print(f"\n🏢 Place: {place_info['title']}")
        print(f"📍 Address: {place_info['address']}")
        print(f"⭐ Rating: {place_info['rating']} ({place_info['reviews_count']} reviews)")
        print(f"📞 Phone: {place_info['phone']}")
        print(f"🌐 Website: {place_info['website']}")

        # Fetch reviews
        print("\n⏳ Fetching reviews...")
        reviews = fetch_reviews(API_KEY, place_id)
        print(f"✅ Fetched {len(reviews)} reviews.")

        # Save results to file
        save_to_file(place_info, reviews)

        # Display sample reviews
        if reviews:
            display_sample_reviews(reviews)

    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
