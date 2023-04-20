from config import *
from setting import *
from selenium.webdriver.common.by import By
import time
import pandas as pd
import urllib.request
import cv2
import pytesseract
from PIL import Image
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

profile_id = fnGetUUID()
port = get_debug_port(profile_id)
driver = get_webdriver(port)
driver.maximize_window()
time.sleep(5)

name_publications = []
prices = []
sqr_meters = []
number_bedrooms = []
number_bathrooms = []
addresses = []
parkings = []
descriptions = []
contact_names = []
phone_numbers = []
date_publications = []

name_publication_path = "/html/body/app-root/adview-index/div/div[2]/div/div[1]/div[1]/adview-price-info/div/h1"
price_path = "/html/body/app-root/adview-index/div/div[2]/div/div[1]/div[1]/adview-price-info/div/div[1]/p[1]"
sqr_meter_path = "/html/body/app-root/adview-index/div/div[2]/div/div[1]/adview-features/div/div/div[6]/p[2]"
number_bedroom_path = "/html/body/app-root/adview-index/div/div[2]/div/div[1]/adview-features/div/div/div[4]/p[2]"
number_bathroom_path = "/html/body/app-root/adview-index/div/div[2]/div/div[1]/adview-features/div/div/div[5]/p[2]"
address_path = "/html/body/app-root/adview-index/div/div[2]/div/div[1]/div[1]/adview-price-info/div/div[2]/div[1]/p"
parking_path = "/html/body/app-root/adview-index/div/div[2]/div/div[1]/adview-features/div/div/div[7]/p[2]"
description_path = "/html/body/app-root/adview-index/div/div[2]/div/div[1]/adview-description/div/p"
contact_name_path = "/html/body/app-root/adview-index/div/div[2]/div/div[2]/div/adview-publisher/div/adview-user-avatar/div/div[2]/p"
phone_btn_path = "/html/body/app-root/adview-index/div/div[2]/div/div[2]/div/adview-publisher/div/div[1]/adview-publisher-button/adview-phone-button/button"
phone_num_path = "/html/body/app-root/adview-index/div/div[2]/div/div[2]/div/adview-publisher/div/div[1]/adview-publisher-button/adview-phone-button/div/img[2]"
date_publication_path = "/html/body/app-root/adview-index/div/div[2]/div/div[1]/div[1]/adview-price-info/div/div[2]/div[2]/p"

def start():
    driver = get_webdriver(port)
    driver.maximize_window()

def log_in():
    driver.get(LOGIN_URL)
    time.sleep(10)
    email_field = driver.find_element(By.ID, 'email_input')
    password_field = driver.find_element(By.ID, 'password_input')
    
    email = "tomasdd20052005@gmail.com"
    password = "tomas2005"
    
    email_field.send_keys(email)
    password_field.send_keys(password)
    
    login_btn = driver.find_element(By.XPATH, '//*[@id="submit_button"]')
    login_btn.click()
    time.sleep(10)
    
def scrape_eachlink(link):
    print(link)
    
    name_publication = ""
    price = ""
    sqr_meter = ""
    number_bedroom = ""
    number_bathroom = ""
    address = ""
    parking = ""
    description = ""
    contact_name = ""
    phone_number = ""
    date_publication = ""
               
    try:
        driver.get(link)
        time.sleep(20)
        
        try:
            name_publication = driver.find_element(By.XPATH, name_publication_path).get_attribute('innerHTML')
        except:
            print("No such name_publication element")

        try:
            price = driver.find_element(By.XPATH, price_path).get_attribute('innerHTML')
        except:
            print("No such price element")

        try:
            sqr_meter = driver.find_element(By.XPATH, sqr_meter_path).get_attribute('innerHTML')
        except:
            print("No such sqr_meter element")

        try:
            number_bedroom = driver.find_element(By.XPATH, number_bedroom_path).get_attribute('innerHTML')
        except:
            print("No such number_bedroom element")

        try:
            number_bathroom = driver.find_element(By.XPATH, number_bathroom_path).get_attribute('innerHTML')
        except:
            print("No such number_bathroom element")

        try:
            address = driver.find_element(By.XPATH, address_path).get_attribute('innerHTML')
        except:
            print("No such address element")

        try:
            parking = driver.find_element(By.XPATH, parking_path).get_attribute('innerHTML')
        except:
            print("No such parking element")

        try:
            description = driver.find_element(By.XPATH, description_path).get_attribute('innerHTML')
        except:
            print("No such description element")

        try:
            contact_name = driver.find_element(By.XPATH, contact_name_path).get_attribute('innerHTML')
        except:
            print("No such contact_name element")

        try:
            date_publication = driver.find_element(By.XPATH, date_publication_path).get_attribute('innerHTML')
        except:
            print("No such date_publication element")

        try:
            phone_btn = driver.find_element(By.XPATH, phone_btn_path)
            phone_btn.click()
            time.sleep(10)
            phone_num_img = driver.find_element(By.XPATH, phone_num_path)
            phone_number = get_str_from_img(phone_num_img)
        except:
            print("Phone Number Error")
        
        print(phone_number)
        
        name_publications.append(name_publication)
        prices.append(price)
        sqr_meters.append(sqr_meter)
        number_bedrooms.append(number_bedroom)
        number_bathrooms.append(number_bathroom)
        addresses.append(address)
        parkings.append(parking)
        descriptions.append(description)
        contact_names.append(contact_name)
        phone_numbers.append(phone_number)
        date_publications.append(date_publication)
        
        time.sleep(10)
    except:
        print("cannot reach this url")

def get_str_from_img(img_element):
    # Get the location and size of the image element
    location = img_element.location
    size = img_element.size

    # Take a screenshot of the entire page
    screenshot = driver.get_screenshot_as_png()

    # Open the screenshot as an image using PIL
    img = Image.open(BytesIO(screenshot))

    # Crop the image to only include the image element
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    img = img.crop((left, top, right, bottom))

    # Save the cropped image to a file
    img.save("example.png")
    
    # Use Tesseract OCR to extract the letters from the image
    letters = pytesseract.image_to_string(img)

    # Print the extracted letters
    return letters
    
def main():
    log_in()
    last_page_num = 2
    count = 0

    for page_num in range(1, last_page_num):
        print(page_num)
        links_array = []
        page_url = TARGET_URL + "&pagina=" + str(page_num)
        driver.get(page_url)
        time.sleep(10)

        # Scrape the data from the current page
    
        list = driver.find_element(By.XPATH, '/html/body/app-root/listing-index/listing-main/div[2]/div/div[2]/listing-result-list/listing-result-list-content/div/div/div')
        lists = list.find_elements(By.TAG_NAME, 'listing-result-ad')
        
        for i in range(len(lists)):
            list_item = lists[i]
            link = list_item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            links_array.append(link)
            
        for j in range(len(links_array)):
            link = links_array[j]
            count += 1
            scrape_eachlink(link)
            if(count == 8):
                count = 0
                print(count)
                continue
            else:
                continue

        df = pd.DataFrame({'Name publication': name_publications, 'prices': prices,
                           'sqr meters': sqr_meters, 'number of bedrooms': number_bedrooms, 'number of bathrooms': number_bathrooms, 'address': addresses, 'parking': parkings, 'description': descriptions, 'contact name': contact_names, 'phone number': phone_numbers, 'date of publication': date_publications})  # Create a DF with the lists

        with pd.ExcelWriter('result.xlsx') as writer:
            df.to_excel(writer, sheet_name='Sheet1')
        
if __name__ == '__main__':
    main()

