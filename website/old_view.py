from django.shortcuts import render,redirect
from django.http import HttpResponse, request, JsonResponse
from django.db.models import Q
import datetime
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
import time
import json
from collections import OrderedDict
from django.contrib import messages  # Import the messages module
from django.http import JsonResponse
import json
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.views import View
import pandas as pd 
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import requests
import re
import os
import pandas as pd
from urllib.parse import urlparse
# ================== Miain Functionality =========================
from pytrends.request import TrendReq
import numpy as np
import matplotlib.pyplot as plt
import httpx
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image 

def Get_Store_ID(url):
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        try:
            # Attempt to parse the JSON content
            shop_data = response.text
            # print(shop_data)
            # shop_id = shop_data.get("shopID")
            # pattern = re.compile(r'shopId:')
            pattern = re.compile(r'shopId:\s*\d+')

            # Search for the pattern in the text
            match = pattern.search(shop_data)

            if match:
                # Extract the matched portion
                shop_id = match.group(0)
                sid = shop_id.split(":")[-1][1:]
                return (sid)
            else:
                return 'No ID'

            # if shop_id:
            #     print(f"The shopId is: {shop_id}")
            # else:
            #     print("No 'shopId' found in the JSON data.")
        except Exception as e:
            return 'No ID'
            # print(response.text)
    else:
        return 'No ID'

# store_link = str(input('Enter store link: '))
def main_run(store_link):
    
    store_name = store_link
    print(store_link)
    
    # Set up Chrome options if needed
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
    # Add options as necessary, e.g., headless mode
    # chrome_options.add_argument('--headless')

    # Set up Chrome driver using ChromeDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Maximize the browser window
    # driver.maximize_window()

    # Navigate to the website
    website_url = 'https://app.shophunter.io/login'
    driver.get(website_url)


    # Define a timeout in seconds
    timeout = 10

    # Wait until the input box with the specified placeholder is present on the page
    email_input = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, '//input[contains(@placeholder, "Email Address")]'))
    )

    email_input.send_keys('mr8.pvt@gmail.com')

    # Wait until the input box with the specified placeholder is present on the page
    email_input = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, '//input[contains(@placeholder, "Password")]'))
    )

    email_input.send_keys('Lovezainab1234')

    # Wait until the button with the specified HTML structure is present on the page
    login_button = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, '//button[@class="btn-default w-full flex items-center justify-center gap-x-2"]'))
    )
    time.sleep(4)
    # Click the login button
    login_button.click()
    store_id_link = store_link+"/shop.json"

    ss_id = Get_Store_ID(store_id_link)
    if ss_id != "No ID":
        driver.get(f'https://app.shophunter.io/shops/view?shop_id={ss_id}')
        try:
            track_store = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), " Track Store ")]')))
            track_store.click()
        except:
            print('Store has been added...')
        time.sleep(3)
    else:
        driver.get('https://app.shophunter.io/shops/add')
        add_store = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/main/div/div/div/div/input')))
        add_store.clear()
        add_store.send_keys(store_link)
        time.sleep(2)
        add_store_button = driver.find_element(By.XPATH,'//*[@id="app"]/div/div[2]/main/div/div/div/div/button')
        add_store_button.click()
        time.sleep(3)


    # ========= Get THe Details ============
    # Create a folder for the store
    
    parsed_url = urlparse(store_link)
    store_name = parsed_url.netloc

    folder_path = os.path.join(os.getcwd(), store_name)
    os.makedirs(folder_path, exist_ok=True)
    
    
    
    # Locate the button by its class name
    day_graph_lst = []
    week_graph_lst = []
    month_graph_lst = []
    day_data_lst = []
    week_data_lst = []
    month_data_lst = []

    time.sleep(4)
    buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))
    print(len(buttons))

    day_no = 0
    week_no = 0
    month_no = 0

    for btn in range(len(buttons)):
        if buttons[btn].text == 'Day' and day_no == 0:
            day_no = btn

        if buttons[btn].text == 'Week' and week_no == 0:
            week_no = btn

        if buttons[btn].text == 'Month' and month_no == 0:
            month_no = btn


    buttons[day_no].click()

    # Wait until the input box with the specified placeholder is present on the page
    elems = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.ID, "gridCards"))
    )

    #.split('\n')[-1].replace('(','').replace(')','')
    # total_sales.text
    total_sales=elems[0].text.split('\n')[2].strip()
    growth_rate = elems[0].text.split('\n')[-2]
    total_orders=elems[1].text.split('\n')[2].strip()
    order_growth_rate = elems[1].text.split('\n')[-2]
    aov = elems[2].text.split('\n')[1]
    skus = elems[3].text.split('\n')[1]

    # Wait for the graph element to be present
    gp = driver.find_element(By.TAG_NAME,'canvas')

    # Specify the filename and path for the screenshot
    # screenshot_filename = "Day.png"
    # screenshot_path = os.path.join(settings.STATIC_URL, 'website', 'images', 'graph_images', screenshot_filename)

    # Take a screenshot using Selenium and save it directly to 'static/images/graph_images'
    # gp.screenshot(screenshot_path)

    # Get the URL path of the saved image using the {% static %} template tag
    # screenshot_url = os.path.join(settings.STATIC_URL, 'website', 'images', 'graph_images', screenshot_filename)
    # day_graph_lst.append(screenshot_url)

    screenshot = gp.screenshot_as_png

    # Create a PIL Image object from the screenshot
    pil_image = Image.open(BytesIO(screenshot))

    # Convert the PIL Image to a Django ContentFile
    image_content = BytesIO()
    pil_image.save(image_content, format='PNG')
    content_file = ContentFile(image_content.getvalue())

    #append data into the lst...
    # day_data_lst.append(total_sales)
    # day_data_lst.append(growth_rate)
    # day_data_lst.append(total_orders)
    # day_data_lst.append(order_growth_rate)
    # day_data_lst.append(aov)
    # day_data_lst.append(skus)
    #end code of the appending data into the list...

    store_detail_obj = store_detail.objects.create(total_sales=total_sales, sale_growth_rate=growth_rate
                                                   , total_order=total_orders,order_growth_rate=order_growth_rate,
                                                   aov=aov, skus=skus,image_file=ImageFile(content_file, name='Day.png')
                                                   )
    store_detail_obj.save()
    
    # print('Store Link:',store_link)
    print('---------------Day------------')
    print('Total Sales:',total_sales)
    print('Sales Growth Rate:', growth_rate)
    print('Total Orders:',total_orders)
    print('Orders Growth Rate:', order_growth_rate)
    print('AOV:',aov)
    print('SKUs:',skus)

    buttons[week_no].click()


    total_sales1=elems[0].text.split('\n')[2].strip()
    growth_rate1 = elems[0].text.split('\n')[-2]
    total_orders1=elems[1].text.split('\n')[2].strip()
    order_growth_rate1 = elems[1].text.split('\n')[-2]
    aov1 = elems[2].text.split('\n')[1]
    skus1 = elems[3].text.split('\n')[1]

    # Wait for the graph element to be present
    gp = driver.find_element(By.TAG_NAME,'canvas')

    # Specify the filename and path for the screenshot
    screenshot_filename = "Week.png"
    screenshot_path = os.path.join(settings.STATIC_URL, 'website', 'images', 'graph_images', screenshot_filename)

    # Take a screenshot using Selenium and save it directly to 'static/images/graph_images'
    gp.screenshot(screenshot_path)

    # Get the URL path of the saved image using the {% static %} template tag
    screenshot_url = os.path.join(settings.STATIC_URL, 'website', 'images', 'graph_images', screenshot_filename)
    week_graph_lst.append(screenshot_url)

    # Capture a screenshot of the graph element
    # gp.screenshot('graph_screenshot1.png')

    #append week data into the lst...
    week_data_lst.append(total_sales1)
    week_data_lst.append(growth_rate1)
    week_data_lst.append(total_orders1)
    week_data_lst.append(order_growth_rate1)
    week_data_lst.append(aov1)
    week_data_lst.append(skus1)
    #end code of the appending data into the list...

    print('---------------Week------------')
    print('Total Sales:',total_sales1)
    print('Sales Growth Rate:', growth_rate1)
    print('Total Orders:',total_orders1)
    print('Orders Growth Rate:', order_growth_rate1)
    print('AOV:',aov1)
    print('SKUs:',skus1)


    buttons[month_no].click()

    total_sales2 =elems[0].text.split('\n')[2].strip()
    growth_rate2 = elems[0].text.split('\n')[-2]
    total_orders2 =elems[1].text.split('\n')[2].strip()
    order_growth_rate2 = elems[1].text.split('\n')[-2]
    aov2 = elems[2].text.split('\n')[1]
    skus2 = elems[3].text.split('\n')[1]

    # Wait for the graph element to be present
    gp = driver.find_element(By.TAG_NAME,'canvas')

    # Specify the filename and path for the screenshot
    screenshot_filename = "Month.png"
    screenshot_path = os.path.join(settings.STATIC_URL, 'website','images', 'graph_images', screenshot_filename)
    # screenshot_path.replace("\\", "/")
    print('main yahan hun...',screenshot_path)
    # Take a screenshot using Selenium and save it directly to 'static/images/graph_images'
    gp.screenshot(screenshot_path)

    # Get the URL path of the saved image using the {% static %} template tag
    screenshot_url = os.path.join(settings.STATIC_URL, 'website' 'images', 'graph_images', screenshot_filename)
    print('main kuta hn..',screenshot_url)
    month_graph_lst.append(screenshot_url)
    # Capture a screenshot of the graph element
    # gp.screenshot('graph_screenshot2.png')

    #append week data into the lst...
    month_data_lst.append(total_sales2)
    month_data_lst.append(growth_rate2)
    month_data_lst.append(total_orders2)
    month_data_lst.append(order_growth_rate2)
    month_data_lst.append(aov2)
    month_data_lst.append(skus2)
    #end code of the appending data into the list...

    print('---------------Month------------')
    print('Total Sales:',total_sales2)
    print('Sales Growth Rate:', growth_rate2)
    print('Total Orders:',total_orders2)
    print('Orders Growth Rate:', order_growth_rate2)
    print('AOV:',aov2)
    print('SKUs:',skus2)


    # Create a DataFrame with headers and linked rows
    data = {
        'Total Sales': [total_sales, total_sales1, total_sales2],
        'Sales Growth Rate': [growth_rate, growth_rate1, growth_rate2],
        'Total Orders': [total_orders, total_orders1, total_orders2],
        'Orders Growth Rate': [order_growth_rate, order_growth_rate1, order_growth_rate2],
        'AOV': [aov, aov1, aov2],
        'SUVs': [skus, skus1, skus2]
    }

    df = pd.DataFrame(data, index=['Day', 'Weekly', 'Monthly'])

    # Create Excel file and save DataFrame to it
    excel_path = os.path.join(folder_path, f"{store_name}.xlsx")
    df.to_excel(excel_path, index=True, header=True)

    print(f"Folder '{store_name}' and Excel file '{store_name}.xlsx' created successfully.")


    #code to click day button of the product and then fetch the data of all products...

    title_lst = []
    price_lst = []
    ads_lst = []
    revenue_lst = []
    rank_lst = []
    velocity_lst = []
    created_lst = []
    link_lst = []
    status_lst = []
    image_path_lst = []

    for i in range(0,4):
        # Scroll down the page
        driver.execute_script("window.scrollBy(0, 200);")  # Adjust the value (500 in this case) based on how much you want to scroll

    day_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/main/div/div/div/div/div/div[4]/div/div/div/div/div/div/div[1]/span/button[1]'))
    ).click()

    # Wait for the div element to be present on the page
    div_element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="relative grow flex flex-col sm:w-[80%] sm:max-w-[80%] md:w-[49%] md:max-w-[49%] lg:w-[49%] lg:max-w-[49%] xl:w-[32%] xl:max-w-[32%] bg-white p-3 overflow-hidden rounded-md border"]'))
    )

    for p in range(len(div_element)):

        # Wait for the div element to be present on the page
        div_element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="relative grow flex flex-col sm:w-[80%] sm:max-w-[80%] md:w-[49%] md:max-w-[49%] lg:w-[49%] lg:max-w-[49%] xl:w-[32%] xl:max-w-[32%] bg-white p-3 overflow-hidden rounded-md border"]'))
        )

        p_link = div_element[p].find_element(By.TAG_NAME,'a').get_attribute('href')

        #----------------code if save image......
        # Get the source URL of the image
        image_url = div_element[p].find_element(By.TAG_NAME,'img').get_attribute("src")

        # Use the requests library to download the image content
        response = requests.get(image_url)
        image_content = BytesIO(response.content)

        # Use Pillow to open the image content
        image = Image.open(image_content)

        # Specify the filename and path for the screenshot
        filename = "product"+str(p)+".jpg"
        image_path = os.path.join(settings.STATIC_ROOT, 'website','images', 'product_images', filename)

        # Save the image to a file (adjust the filename as needed)
        image.save(image_path)

        # Get the URL path of the saved image using the {% static %} template tag
        img_url = os.path.join(settings.STATIC_URL, 'images', 'product_images', filename)
        image_path_lst.append(img_url)
        #----------------end code of save image.......

        pro_title = div_element[p].text.split('\n')[0]
        price = div_element[p].text.split('\n')[2]
        ads = div_element[p].text.split('\n')[4]
        revenue = div_element[p].text.split('\n')[6]
        rank = div_element[p].text.split('\n')[8]
        velocity = div_element[p].text.split('\n')[10]
        created = div_element[p].text.split('\n')[12]

        driver.get(p_link)

        # Wait for the graph element to be present
        product_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="flex flex-col gap-y-1"]'))  # Replace with your actual XPath
        )

        product_link = product_link.find_elements(By.TAG_NAME,'a')[0].get_attribute('href')

        driver.back()

        title_lst.append(pro_title)
        price_lst.append(price)
        ads_lst.append(ads)
        revenue_lst.append(revenue)
        rank_lst.append(rank)
        velocity_lst.append(velocity)
        created_lst.append(created)
        link_lst.append(product_link)
        status_lst.append('Day')

        #print(product_link, pro_title, price, ads, revenue, rank, velocity, created)
    #---------------------end code---------------------------------


    #code to click day button of the product and then fetch the data of all products...
    for i in range(0,4):
        # Scroll down the page
        driver.execute_script("window.scrollBy(0, 200);")  # Adjust the value (500 in this case) based on how much you want to scroll

    week_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/main/div/div/div/div/div/div[4]/div/div/div/div/div/div/div[1]/span/button[2]'))
    ).click()

    # Wait for the div element to be present on the page
    div_element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="relative grow flex flex-col sm:w-[80%] sm:max-w-[80%] md:w-[49%] md:max-w-[49%] lg:w-[49%] lg:max-w-[49%] xl:w-[32%] xl:max-w-[32%] bg-white p-3 overflow-hidden rounded-md border"]'))
    )

    for p in range(len(div_element)):

        # Wait for the div element to be present on the page
        div_element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="relative grow flex flex-col sm:w-[80%] sm:max-w-[80%] md:w-[49%] md:max-w-[49%] lg:w-[49%] lg:max-w-[49%] xl:w-[32%] xl:max-w-[32%] bg-white p-3 overflow-hidden rounded-md border"]'))
        )

        p_link = div_element[p].find_element(By.TAG_NAME,'a').get_attribute('href')

        #----------------code if save image......
        # Get the source URL of the image
        image_url = div_element[p].find_element(By.TAG_NAME,'img').get_attribute("src")

        # Use the requests library to download the image content
        response = requests.get(image_url)
        image_content = BytesIO(response.content)

        # Use Pillow to open the image content
        image = Image.open(image_content)

        # Specify the filename and path for the screenshot
        filename = "product"+str(p)+".jpg"
        image_path = os.path.join(settings.STATIC_ROOT, 'images', 'product_images', filename)

        # Save the image to a file (adjust the filename as needed)
        image.save(image_path)

        # Get the URL path of the saved image using the {% static %} template tag
        img_url = os.path.join(settings.STATIC_URL, 'images', 'product_images', filename)
        image_path_lst.append(img_url)
        #----------------end code of save image.......

        pro_title = div_element[p].text.split('\n')[0]
        price = div_element[p].text.split('\n')[2]
        ads = div_element[p].text.split('\n')[4]
        revenue = div_element[p].text.split('\n')[6]
        rank = div_element[p].text.split('\n')[8]
        velocity = div_element[p].text.split('\n')[10]
        created = div_element[p].text.split('\n')[12]

        driver.get(p_link)

        # Wait for the graph element to be present
        product_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="flex flex-col gap-y-1"]'))  # Replace with your actual XPath
        )

        product_link = product_link.find_elements(By.TAG_NAME,'a')[0].get_attribute('href')

        driver.back()

        title_lst.append(pro_title)
        price_lst.append(price)
        ads_lst.append(ads)
        revenue_lst.append(revenue)
        rank_lst.append(rank)
        velocity_lst.append(velocity)
        created_lst.append(created)
        link_lst.append(product_link)
        status_lst.append('Week')

        #print(product_link, pro_title, price, ads, revenue, rank, velocity, created)
    #---------------------end code---------------------------------


    #code to click day button of the product and then fetch the data of all products...
    for i in range(0,4):
        # Scroll down the page
        driver.execute_script("window.scrollBy(0, 200);")  # Adjust the value (500 in this case) based on how much you want to scroll

    month_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/main/div/div/div/div/div/div[4]/div/div/div/div/div/div/div[1]/span/button[3]'))
    ).click()

    # Wait for the div element to be present on the page
    div_element = WebDriverWait(driver, 11).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="relative grow flex flex-col sm:w-[80%] sm:max-w-[80%] md:w-[49%] md:max-w-[49%] lg:w-[49%] lg:max-w-[49%] xl:w-[32%] xl:max-w-[32%] bg-white p-3 overflow-hidden rounded-md border"]'))
    )

    for p in range(len(div_element)):

        # Wait for the div element to be present on the page
        div_element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="relative grow flex flex-col sm:w-[80%] sm:max-w-[80%] md:w-[49%] md:max-w-[49%] lg:w-[49%] lg:max-w-[49%] xl:w-[32%] xl:max-w-[32%] bg-white p-3 overflow-hidden rounded-md border"]'))
        )

        p_link = div_element[p].find_element(By.TAG_NAME,'a').get_attribute('href')

        #----------------code if save image......
        # Get the source URL of the image
        image_url = div_element[p].find_element(By.TAG_NAME,'img').get_attribute("src")

        # Use the requests library to download the image content
        response = requests.get(image_url)
        image_content = BytesIO(response.content)

        # Use Pillow to open the image content
        image = Image.open(image_content)

        # Specify the filename and path for the screenshot
        filename = "product"+str(p)+".jpg"
        image_path = os.path.join(settings.STATIC_ROOT, 'images', 'product_images', filename)

        # Save the image to a file (adjust the filename as needed)
        image.save(image_path)

        # Get the URL path of the saved image using the {% static %} template tag
        img_url = os.path.join(settings.STATIC_URL, 'images', 'product_images', filename)
        image_path_lst.append(img_url)
        #----------------end code of save image.......


        pro_title = div_element[p].text.split('\n')[0]
        price = div_element[p].text.split('\n')[2]
        ads = div_element[p].text.split('\n')[4]
        revenue = div_element[p].text.split('\n')[6]
        rank = div_element[p].text.split('\n')[8]
        velocity = div_element[p].text.split('\n')[10]
        created = div_element[p].text.split('\n')[12]

        driver.get(p_link)

        # Wait for the graph element to be present
        product_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="flex flex-col gap-y-1"]'))  # Replace with your actual XPath
        )

        product_link = product_link.find_elements(By.TAG_NAME,'a')[0].get_attribute('href')

        driver.back()

        title_lst.append(pro_title)
        price_lst.append(price)
        ads_lst.append(ads)
        revenue_lst.append(revenue)
        rank_lst.append(rank)
        velocity_lst.append(velocity)
        created_lst.append(created)
        link_lst.append(product_link)
        status_lst.append('Month')

        #print(product_link, pro_title, price, ads, revenue, rank, velocity, created)
    #---------------------end code---------------------------------



    # Create a DataFrame for top performing products
    products_data = {
        'Title': title_lst,
        'Price': price_lst,
        'Ads': ads_lst,
        'Revenue': revenue_lst,
        'Rank': rank_lst,
        'Velocity': velocity_lst,
        'Created': created_lst,
        'link':link_lst,
        'Status':status_lst
    }


    products_df = pd.DataFrame(products_data)

    # Save top performing products to Excel file
    products_excel_path = os.path.join(folder_path, "top_performing_products.xlsx")
    products_df.to_excel(products_excel_path, index=False, header=True)

    print(f"Excel file 'top_performing_products.xlsx' created successfully.")

    #---------------------end code of top performing products fetching and saving code---------------------------------

    #--------endcode of the fetching sales and top product data and saving----------------
        
        
    #  =============== remove the store ==============
    driver.get(f'https://app.shophunter.io/shops/view?shop_id={ss_id}')
    time.sleep(4)
    buttons1 =  WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))
    
    untrack_btn = None

    for btn1 in range(len(buttons1)):
        #print(buttons1[btn1].text)
#         buttons1 =  WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))
        if buttons1[btn1].text == 'Untrack Store':
            untrack_btn = buttons1[btn1]

    if untrack_btn:
        untrack_btn.click()
        
    else:
        print('bttt not found')
        ubtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@type="default" and @class="w-full auth-button-alt text-center"]')))
        
        if ubtn:
            ubtn.click()
        else:
            print('again nt fund')
        


    buttons2 = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))

    remove_btn = None

    for btn2 in range(len(buttons2)):
        if buttons2[btn2].text == 'Remove Store':
            remove_btn = buttons2[btn2]

    remove_btn.click()

    return(day_graph_lst, week_graph_lst, month_graph_lst, day_data_lst, week_data_lst, month_data_lst,
            title_lst, price_lst, ads_lst, revenue_lst, rank_lst, velocity_lst, created_lst,
            link_lst, status_lst, image_path_lst
           )
    

# Function to get Google Trends data


# =================================================================



# Create your views here.
def index(request):

    return render(request,'website/index.html')


def get_report(request):

    store_link = json.loads(request.body)
    all_data = main_run(store_link['linkbox'])
    print(all_data)

    data = {'total_orders': store_link}
    return JsonResponse(data)