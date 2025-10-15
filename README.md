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

## maps_place_reviews_fetcher.py

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
python maps_place_reviews_fetcher.py
