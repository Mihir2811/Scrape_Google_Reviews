# Google Maps Review Intelligence Suite

This repository provides a collection of Python scripts designed to automate the process of collecting, analyzing, and summarizing Google Maps data — including business locations, detailed place information, and customer reviews.  
It uses **SerpApi** for Google Maps data extraction and **AWS Bedrock (Meta LLaMA 3)** for advanced AI-powered review summarization.

---

## Project Overview

The project consists of three main scripts that together form a complete data workflow:

| Script | Description | Tools |
|--------|--------------|-------|
| `maps_place_reviews_fetcher.py` | Retrieves details and reviews for a single Google Maps location using SerpApi. | SerpApi, Python |
| `honest_branches_scraper.py` | Searches Google Maps for all “Honest” restaurant branches in Gujarat and exports their details. | SerpApi, Python |
| `review_summarizer_bedrock.py` | Summarizes large sets of reviews using AWS Bedrock’s Meta LLaMA 3 model. | AWS Bedrock, LLaMA 3, Python |

---

## 1. serpapi_place_reviews_collector.py

### Description
This script retrieves detailed information and user reviews for a specific Google Maps location using SerpApi. It can extract place details like name, address, rating, and contact info, and then download all available customer reviews.

### Features
1. Loads the SerpApi API key from a `.env` file.
2. Validates the API key before fetching data.
3. Retrieves comprehensive place information using a Google Maps Place ID.
4. Fetches all available reviews with automatic pagination handling.
5. Saves results to a JSON file and displays sample reviews in the console.

### Usage
```bash
python serpapi_place_reviews_collector.py
````

This script is useful for collecting reviews and details from a specific business on Google Maps.

---

## 2. review_summarizer_bedrock.py

### Description

This script reads large sets of customer reviews from a CSV file and uses AWS Bedrock’s Meta LLaMA 3 model to create structured summaries. It handles token limits intelligently and produces insights that highlight overall sentiment, common themes, and improvement areas.

### Features

1. Loads AWS credentials securely using `dotenv`.
2. Counts tokens using the `tiktoken` library to manage model input limits.
3. Uses Bedrock’s `meta.llama3-70b-instruct-v1:0` model to summarize reviews.
4. Automatically splits and processes large review datasets.
5. Combines multiple summaries into one cohesive report.
6. Focuses on these analysis areas:

   * Customer Experience
   * Product or Service Quality
   * Pricing and Charges
   * Digital Platform Experience
   * Support and Issue Resolution

### Output

* Provides a clear summary of customer sentiment.
* Lists key positives and negatives.
* Highlights recurring themes and actionable insights.

### Usage

```bash
python review_summarizer_bedrock.py
```

---

## 3. branches_scraper.py

### Description

This script uses SerpApi to search Google Maps for all “Honest” restaurant branches located in Gujarat. It filters search results, extracts details for each branch, and exports the data to both JSON and CSV formats.

### Features

1. Loads the SerpApi API key securely from `.env`.
2. Searches Google Maps for “Honest restaurant Gujarat”.
3. Filters and extracts only relevant results.
4. Captures key details such as place ID, name, address, rating, and review count.
5. Saves data into structured JSON and CSV files.
6. Displays all branches and their information in the console.

### Usage

```bash
python branches_scraper.py
```

This script is ideal for building datasets of local business branches or automating business information collection.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/Scrape_Google_Reviews.git
cd Scrape_Google_Reviews
```

### 2. Create a `.env` File

Add your credentials:

```
API=your_serpapi_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

### 3. Install Dependencies

```bash
pip install serpapi python-dotenv boto3 pandas tiktoken
```

---
