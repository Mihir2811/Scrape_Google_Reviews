import os
import json
import pandas as pd

# Folder containing your individual JSON files
json_folder = "/home/mihir/Desktop/DigitQt/Projects/Google Reviews/Motilal/reviews"  # change if your files are in a different folder
output_csv = "motilal_oswal_reviews_combined.csv"

def load_reviews_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    place_info = data.get("place_info", {})
    reviews = data.get("reviews", [])
    rows = []

    for review in reviews:
        rows.append({
            "place_id": place_info.get("place_id", ""),
            "branch_name": place_info.get("title", ""),
            "branch_address": place_info.get("address", ""),
            "branch_rating": place_info.get("rating", ""),
            "review_rating": review.get("rating", ""),
            "review_date": review.get("date", ""),
            "review_text": review.get("snippet", ""),
            "review_author": review.get("user", {}).get("name", "") if review.get("user") else ""
        })

    return rows

def main():
    all_reviews = []

    # List all JSON files in the folder that end with '.json'
    files = [f for f in os.listdir(json_folder) if f.endswith(".json")]

    print(f"Found {len(files)} JSON files. Processing...")

    for file in files:
        filepath = os.path.join(json_folder, file)
        try:
            reviews = load_reviews_from_file(filepath)
            all_reviews.extend(reviews)
            print(f"Processed {file} ({len(reviews)} reviews)")
        except Exception as e:
            print(f"Error processing {file}: {e}")

    # Convert to DataFrame
    df = pd.DataFrame(all_reviews)

    # Save to CSV
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"\nAll reviews saved to {output_csv}")

if __name__ == "__main__":
    main()
