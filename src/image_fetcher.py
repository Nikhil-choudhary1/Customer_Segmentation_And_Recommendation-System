from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()

def get_product_image(product_name):
    try:
        params = {
            "q": product_name,
            "tbm": "isch",
            "api_key": os.getenv("SERP_API_KEY")
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        images = results.get("images_results", [])

        if images:
            return images[0]["thumbnail"]
        else:
            return "https://via.placeholder.com/300x200?text=No+Image"

    except Exception:
        return "https://via.placeholder.com/300x200?text=Error"