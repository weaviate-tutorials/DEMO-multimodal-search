"""This file implements functions that fetch results from weaviate for the query
entered by user. There are two functions, testImage and testText for image query and text query
respectively."""

import base64
import os

import weaviate
from weaviate import Config

WEAVIATE_URL = os.getenv('WEAVIATE_URL')
if not WEAVIATE_URL:
    WEAVIATE_URL = 'http://localhost:8080'
print(WEAVIATE_URL, flush=True)

client = weaviate.Client(WEAVIATE_URL,
                         additional_config=Config(grpc_port_experimental=50051))
print(f"Client is ready {client.is_ready()} (This is test.py)")


def search_by_text(near_text):
    # I am fetching top 3 results for the user, we can change this by making small 
    # altercations in this function and in upload.html file
    # You can also analyse the result in a better way by taking a look at res.
    # Try printing res in the terminal and see what all contents it has.
    images = client.collection.get("ClipExample")
    res = images.query.near_text(query=near_text, limit=3, return_properties=["text"])
    return tuple(o.properties["text"] for o in res.objects)


def search_by_image(near_image):
    # I am fetching top 3 results for the user, we can change this by making small 
    # altercations in this function and in upload.html file
    with open(near_image, "rb") as f:
        img_file_encoded = base64.b64encode(f.read()).decode()
        images = client.collection.get("ClipExample")
        res = images.query.near_image(near_image=img_file_encoded, limit=3, return_properties=["text"])
        return tuple(o.properties["text"] for o in res.objects)
