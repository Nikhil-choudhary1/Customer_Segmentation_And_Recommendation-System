import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def load_and_prepare_data(file_path):
    df = pd.read_excel(file_path)

    df = df.dropna(subset=['CustomerID'])
    df = df.dropna(subset=['Description'])
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]
    df = df.drop_duplicates()

    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

    return df


def create_similarity_matrix(df):
    customer_product = df.pivot_table(
        index='CustomerID',
        columns='Description',
        values='Quantity',
        aggfunc='sum',
        fill_value=0
    )

    similarity = cosine_similarity(customer_product.T)

    similarity_df = pd.DataFrame(
        similarity,
        index=customer_product.columns,
        columns=customer_product.columns
    )

    return similarity_df


def recommend_products(product_name, similarity_df, top_n=5):
    similar_products = similarity_df[product_name].sort_values(ascending=False)
    return [(item, float(score)) for item, score in similar_products[1:top_n+1].items()]

def get_product_image(product_name):
    keyword = product_name.split()[0].lower()

    return f"https://source.unsplash.com/300x200/?{keyword}"

def create_customer_similarity(df):
    customer_product = df.pivot_table(
        index='CustomerID',
        columns='Description',
        values='Quantity',
        aggfunc='sum',
        fill_value=0
    )

    similarity = cosine_similarity(customer_product)

    similarity_df = pd.DataFrame(
        similarity,
        index=customer_product.index,
        columns=customer_product.index
    )

    return similarity_df, customer_product


