import os
os.environ["MESA_LOADER_DRIVER_OVERRIDE"] = "llvmpipe"
import streamlit as st
from pricecomparison import object_recognition, get_google_shopping_prices
from PIL import Image
import pandas as pd

# Function to detect objects in the uploaded image
def detect_objects(image):
    image = Image.open(image)
    print("EEeeeeeeeeeee", type(image))
    detected_objects = object_recognition(image)
    return detected_objects

# Function to find prices of objects on online retailers
def find_prices(object_name):
    prices_info = get_google_shopping_prices(object_name)
    return prices_info

# Streamlit app
def main():
    st.title("Object Detection and Price Finder App")

    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None

    if 'object_names' not in st.session_state:
        st.session_state.object_names = []

    if 'selected_objects' not in st.session_state:
        st.session_state.selected_objects = []

    uploaded_image = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])

    if uploaded_image is not None:
        st.session_state.uploaded_image = uploaded_image
        st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

        if st.button('Detect Objects'):
            st.session_state.object_names = detect_objects(st.session_state.uploaded_image)

    if st.session_state.object_names:
        st.write("Detected Objects:")
        columns = st.columns(len(st.session_state.object_names))
        for i, object_name in enumerate(st.session_state.object_names):
            if columns[i].button(object_name.upper()):
                if 'selected_object' in st.session_state:
                    del st.session_state.selected_object
                    # del st.session_state.prices_table

                st.session_state.selected_object = object_name
                st.write("Prices for", object_name.upper())
                prices = find_prices(object_name)
                df = pd.DataFrame(prices)
                st.session_state.editor = st.data_editor(
                        df,
                        column_config={
                        "column 1": "PRODUCT",
                        "column 2": "PRICE",
                        "column 3": "WEBSITE",
                        },
                    )

    if st.button('Clear Results'):
        st.session_state.clear()  # Clear all session state variables
        st.rerun()

if __name__ == "__main__":
    main()
