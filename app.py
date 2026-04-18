from flask import Flask, request, jsonify, render_template
from src.recommendation import load_and_prepare_data, create_similarity_matrix, recommend_products
from src.logger import logging
from difflib import get_close_matches
from src.image_fetcher import get_product_image
import os
app = Flask(__name__)


logging.info("Loading dataset...")
df = load_and_prepare_data("data/Online_Retail.xlsx")
similarity_df = create_similarity_matrix(df)
logging.info("Data loaded successfully")


@app.route('/')
def home():
    logging.info("Home page loaded")
    return render_template("index.html")


@app.route('/recommendation', methods=['POST'])
def recommend_ui():

    product = request.form.get('product')

    logging.info(f"User searched for product: {product}")

    try:
       
        if not product:
            logging.warning("Empty product input")
            return render_template("index.html", error="Please enter a product name")

        if product not in similarity_df.index:
            logging.warning(f"Product not found: {product}")

            # Fuzzy matching
            suggestions = get_close_matches(product, similarity_df.index, n=5, cutoff=0.3)

            return render_template(
                "index.html",
                error=f"'{product}' not found",
                suggestions=suggestions
            )

       
        result = recommend_products(product, similarity_df)
        logging.info("Recommendation generated successfully")

        result_with_images = [
        {
            "name": item,
            "score": score,
            "image": get_product_image(item)
        }
        for item, score in result
    ]

        return render_template("index.html", recommendations=result_with_images)

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return render_template("index.html", error="Something went wrong")


@app.route('/recommend', methods=['GET'])
def recommend():
    product = request.args.get('product')

    logging.info(f"API request for product: {product}")

    try:
        result = recommend_products(product, similarity_df)
        return jsonify(result)
    except Exception as e:
        logging.error(f"API error: {str(e)}")
        return jsonify({"error": "Something went wrong"})


@app.route('/search_suggestions', methods=['GET'])
def search_suggestions():
    query = request.args.get('query', '')

    suggestions = [
        item for item in similarity_df.index
        if query.lower() in item.lower()
    ]

    return jsonify(suggestions[:10])


if __name__ == "__main__":
    if os.getenv("ENV") == "dev":
        app.run(host="0.0.0.0", port=5000)