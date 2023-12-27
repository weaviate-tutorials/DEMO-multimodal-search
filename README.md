# Multimodal (and multi-lingual) search demo

This app demonstrates Weaviate's multi-modal capabilities.

It uses a CLIP model to encode images and text into the same vector space.

## Prerequisites

To run this example, you need:
- Docker (to run Weaviate)
- Python 3.8 or higher

## Setup instructions

1. Install the Python dependencies.
    ```bash
    pip install -r requirements.txt
    ```
2. Run docker-compose to spin up an Weaviate instance and the CLIP inference container.
    ```bash
    docker compose up -d
    ```
3. Create the collection definition and import data, as well as some pre-prepared queries.
    ```bash
    python add_data.py
    ```
4. Start the Streamlit app.
    ```bash
    streamlit run app.py
    ```

## Usage instructions

Input a search query into the text box, or upload an image. This will return the top 6 results from the Weaviate instance. The results are sorted by the cosine similarity between the query and the vector representation of the object.

The model used is multi-lingual! That means it can understand queries in multiple languages. Try a search with an image, and then try inputting a description for that image in different languages!

## Dataset license

[Universe image](data/images/universe1.jpg) from [Unsplash](https://unsplash.com/photos/two-stars-in-the-middle-of-a-black-sky-fsH1KjbdjE8)

[Forest image](data/images/forest2.jpg) from [Unsplash](https://unsplash.com/photos/green-pine-trees-d6kSvT2xZQo)
