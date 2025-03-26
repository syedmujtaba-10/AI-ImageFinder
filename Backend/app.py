import streamlit as st
from PIL import Image
from search import search_captions, get_caption_for_image

st.set_page_config(layout="wide")
st.title("🔍 Local AI Image Search")

st.markdown("Describe the image you're looking for. The system uses AI-generated captions and semantic search to find the best matches.")

query = st.text_input("📝 What do you want to see?")
if st.button("🔍 Search") and query.strip():
    results = search_captions(query)

    if results:
        st.subheader(f"📸 Top {len(results)} Results for: *{query}*")
        cols = st.columns(len(results))

        for col, img_path in zip(cols, results):
            image = Image.open(img_path).convert("RGB")
            #caption = get_caption_for_image(img_path)
            col.image(image, caption=None, use_container_width=True)
    else:
        st.warning("No matching images found.")
