import streamlit as st

# Function to detect objects in the uploaded image
def detect_objects(image):
    # Your object detection code here
    # This function should return a list of detected object names
    return ['cat', 'dog', 'car']

# Function to find prices of objects on online retailers
def find_prices(object_name):
    # Your price finder code here
    # This function should return a dictionary with keys as the retailer name
    # and values as the price and link
    return {
        'Amazon': {'price': '$100', 'link': 'https://www.amazon.com'},
        'eBay': {'price': '$90', 'link': 'https://www.ebay.com'},
        'Walmart': {'price': '$95', 'link': 'https://www.walmart.com'}
    }

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
            if columns[i].button(object_name):
                if 'selected_object' in st.session_state:
                    del st.session_state.selected_object
                    del st.session_state.prices_table

                st.session_state.selected_object = object_name
                st.write("Prices for", object_name)
                prices = find_prices(object_name)
                table = []
                for retailer, info in prices.items():
                    table.append([retailer, info['price'], info['link']])
                st.session_state.prices_table = st.table(table)

    if st.button('Clear Results'):
        st.session_state.clear()  # Clear all session state variables
        st.rerun()

if __name__ == "__main__":
    main()
