#!/usr/bin/env python
# coding: utf-8

# In[53]:


## Importing Libraries


# In[51]:


from ultralytics import YOLO
from PIL import Image
import requests
from bs4 import BeautifulSoup


# In[5]:


## BASIC OBJECT RECOGNITION USING PRE-TRAINED MODEL YOLO


# In[50]:


def object_recognition(img):
    model = YOLO("yolov8l.pt")
    allowed_objects = [24,25,26,28,29,39,40,41,42,67]
    
    results = model.predict(source=img, conf=0.8, max_det=3, classes= allowed_objects, show=False, save=True)  # save plotted images

    objects = []
    for r in results:

        boxes = r.boxes
        for box in boxes:

            c = box.cls
#             print(model.names[int(c)])
            objects.append(model.names[int(c)])

    objects = set(objects)
#     print("objects detected in the image are:", objects)
    
    return list(objects)


# In[7]:


## WEB SCAPPER TO GET THE PRICES OF THESE OBJECTS FROM DIFFEREN ONLINE RETAILERS:


# In[40]:


def get_google_shopping_prices(query):
    url = f"https://www.google.com/search?q={query}&tbm=shop"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    items = soup.find_all('div', class_='P8xhZc')
    products = []
    for item in items:
        name = item.find('a').text
        price = item.find('span', class_='HRLxBb').text
        url = item.find('a')['href'][9:]
        try:
            website = item.find('div', class_='dD8iuc').contents[-1].split()[1]
        except:
            website = url
        
        article = {'PRODUCT NAME': name.strip(), 'PRICE': price, 'WEBSITE/URL': website}
        products.append(article)
        
#         print("name:", name.strip())
#         print("price:", price)
#         print("URL:", website)
#         print()
        
    return products


# In[9]:


## ALGORITHM TO COMPARE PRICES AND LIST THEM FROM LOWER TO HIGHER


# In[43]:


def sort_items_by_price(items, order='ascending'):
    
    # Define a lambda function to extract the price from each item
    get_price = lambda item: float(item['PRICE'].replace('$', '').replace('+', '').replace(' shipping', ''))
        
    # Sort the items based on price
    sorted_items = sorted(items, key=get_price, reverse=(order == 'descending'))
    
    return sorted_items


# In[11]:


## EXAMPLE USAGE


# In[54]:


"""
1. Image upload and storage

currently we are providing the sample images manually, it will be replaced later by a UI will let users to 
select and upload images or click and upload real-time images.
Images with object detections are stored in local storage, it will be replaced by a secure database later
"""
img = Image.open("../Downloads/sample_image.png")



"""
2. Object Recognition
"""
objects = object_recognition(img)
print("\nItems detected:", objects)



"""
3. WEB SCRAPPING
"""
all_products = []
for item_name in objects:
    product = get_google_shopping_prices(item_name)
    all_products.append(product)


"""
4. SORTING PRICES FROM LOW TO HIGH
"""
for product in all_products:
    sorted_items_asc = sort_items_by_price(product, order='ascending')
    print("\nItems sorted by price(LOW TO HIGH) from different retailers:\n")
    for item in sorted_items_asc:
        for key, value in item.items():
            print(key,": ", value)
        print()

