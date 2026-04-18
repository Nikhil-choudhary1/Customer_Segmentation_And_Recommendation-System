from serpapi import GoogleSearch

def get_product_image(product_name):
    try:
        params = {
            "q": product_name,
            "tbm": "isch",
            "api_key": "9ec82ad426e779a93273873886e4ca1046d36ceea7147bd552c53a7063f0fe30"
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