from datetime import datetime
from google.cloud import firestore
from faker import Faker
import random
import os 
from dotenv import load_dotenv

load_dotenv('../.env')
# get database name
FIRESTORE_DATABASE = os.environ.get('FIRESTORE_DATABASE')

# Initialize Firestore and Faker
firestore_client = firestore.Client(database=FIRESTORE_DATABASE)
fake = Faker()

def generate_random_product():
    return {
        "_id": fake.uuid4(),
        "name": fake.company(),
        "description": fake.text(),
        "category": "Electronics",
        "subcategory": "Laptops",
        "brand": fake.company_suffix(),
        "price": round(random.uniform(500, 1500), 2),
        "currency": "USD",
        "inStock": random.choice([True, False]),
        "specifications": {
            "processor": random.choice(["Intel Core i7", "Intel Core i5", "AMD Ryzen 7"]),
            "ram": random.choice(["8GB", "16GB", "32GB"]),
            "storage": random.choice(["256GB SSD", "512GB SSD", "1TB SSD"]),
            "display": random.choice(["13.3-inch FHD", "15.6-inch FHD", "17.3-inch FHD"])
        },
        "reviews": [
            {
                "user": fake.user_name(),
                "rating": random.randint(1, 5),
                "comment": fake.sentence()
            },
            {
                "user": fake.user_name(),
                "rating": random.randint(1, 5),
                "comment": fake.sentence()
            }
        ]
    }

def populate_firestore(rows):
    collection_ref = firestore_client.collection('products')
    for _ in range(rows):
        product = generate_random_product()
        collection_ref.document(product["_id"]).set(product)
    print(f"Inserted {rows} random products into Firestore.")


populate_firestore(100)
