from pathlib import Path
import weaviate
import weaviate.classes as wvc
import streamlit as st
import base64
from add_data import COLLECTION_NAME

client = weaviate.connect_to_local()

logo_path = Path("assets/weaviate-logo-light-transparent-200.png")
title_cols = st.columns([0.15, 0.85])
with title_cols[0]:
    st.write("")
    st.image(logo_path.read_bytes(), width=75)
with title_cols[1]:
    st.title("Multi-Modality with Weaviate")

st.subheader("Instructions")
st.write(
    """
    Search the dataset by uploading an image or entering free text.
    The model is multi-lingual as well - try searching in different languages!

    (Note: If you enter both, only the image will be used.)
    """
)

st.subheader("Search the dataset")

srch_cols = st.columns(2)
with srch_cols[0]:
    search_text = st.text_area(label="Search by text")
with srch_cols[1]:
    img = st.file_uploader(label="Search by image")


if search_text != "" or img is not None:
    mm_coll = client.collections.get(COLLECTION_NAME)

    if img is not None:
        st.image(img, caption="Uploaded Image", use_column_width=True)
        imgb64 = base64.b64encode(img.read()).decode()

        response = mm_coll.query.near_image(
            near_image=imgb64,
            return_properties=[
                "filename",
                # "image"
            ],
            return_metadata=wvc.query.MetadataQuery(distance=True),
            limit=6,
        )

    else:
        response = mm_coll.query.near_text(
            query=search_text,
            return_properties=[
                "filename",
                # "image"
            ],
            return_metadata=wvc.query.MetadataQuery(distance=True),
            limit=6,
        )

    st.subheader("Results found:")
    for i, r in enumerate(response.objects):
        if i % 3 == 0:
            with st.container():
                columns = st.columns(3)
                st.divider()
        with columns[i % 3]:
            st.write(r.properties["filename"])
            # st.write(type(base64.b64decode(r.properties["image"])))

            # Temporary solution to show image
            imgpath = Path("data/images") / r.properties["filename"]
            img = imgpath.read_bytes()
            st.image(img)
            st.write(f"Distance: {r.metadata.distance:.3f}")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)