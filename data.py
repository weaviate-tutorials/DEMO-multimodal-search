"""This file contains code that adds data to weaviate from the Images folder.
These images will be the ones with which the module multi2-vec-clip will compare
the image or text query given by the user."""
import base64

import weaviate
import os
from pathlib import Path

from weaviate import Config
import weaviate.classes as wvc
from weaviate.collection.classes.config import VectorIndexType, Multi2VecField

# initiating the Weaviate client
WEAVIATE_URL = os.getenv('WEAVIATE_URL')
if not WEAVIATE_URL:
    WEAVIATE_URL = 'http://localhost:8080'
print(WEAVIATE_URL, flush=True)

client = weaviate.Client(WEAVIATE_URL,
                         additional_config=Config(grpc_port_experimental=50051))
print(f"Client is ready {client.is_ready()}")

# delete the ClipExample collection if already exists
client.collection.delete(["ClipExample"])

# creating the ClipExample collection to add images
# I have used the https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/multi2vec-clip
# to get help on making a suitable schema. You can read the contents of this web page to know more.
images = client.collection.create(
    name="ClipExample",
    description="Implement CLIP example",
    properties=[
        wvc.Property(
            name="text",
            data_type=wvc.DataType.TEXT,
        ),
        wvc.Property(
            name="image",
            data_type=wvc.DataType.BLOB,
        ),
    ],
    # the img2vec-neural Weaviate module
    vectorizer_config=wvc.ConfigFactory.Vectorizer.multi2vec_clip(
        image_fields=[Multi2VecField(name="image", weight=0.3)],
        text_fields=[Multi2VecField(name="text", weight=0.7)]),
    vector_index_type=VectorIndexType.HNSW
)
print("The 'ClipExample' class has been defined.")

# Adding all images from static/Images folder
images_to_add = []
imgdir = Path("static/Images/")
for filepath in imgdir.glob("*.jfif"):
    img_file_encoded = base64.b64encode(filepath.read_bytes()).decode()
    image = wvc.DataObject(
        properties={
            "image": img_file_encoded,
            "text": filepath.name
        })
    images_to_add.append(image)

images.data.insert_many(images_to_add)
print("Images added")

# You can try uncommenting the below code to add text as well
# After adding the texts, these texts can also be fetched as results if their
# embeddings are similar to the embedding of the query. Currently, the frontend is
# designed to accommodate these as well.

# Adding texts
# texts = [
#    'A dense forest',
#    'A beautiful beach',
#    'people playing games',
#    'Students syudying in class',
#    'a beautiful painting',
#    'place with scenic beauty',
#    'confident woman',
#    'cute little creature',
#    'players playing badminton'
# ]
# texts_to_add = []
# for t in texts:
#    text = wvc.DataObject(
#        properties={
#            "text": t
#        })
#    texts_to_add.append(text)

# images.data.insert_many(texts_to_add)
# print("Texts added")
